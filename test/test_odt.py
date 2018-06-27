# -*- coding: utf-8 -*-
#
import os

import numpy

import meshio
import optimesh

from helpers import download_mesh


def test_simple1():
    X = numpy.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0],
        [0.4, 0.5],
        ])
    cells = numpy.array([
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        ])

    X, cells = optimesh.odt(X, cells, tol=1.0e-5)

    # Test if we're dealing with the mesh we expect.
    nc = X.flatten()
    norm1 = numpy.linalg.norm(nc, ord=1)
    norm2 = numpy.linalg.norm(nc, ord=2)
    normi = numpy.linalg.norm(nc, ord=numpy.inf)

    tol = 1.0e-12
    ref = 4.999994919473657
    assert abs(norm1 - ref) < tol * ref
    ref = 2.1213191460738456
    assert abs(norm2 - ref) < tol * ref
    ref = 1.0
    assert abs(normi - ref) < tol * ref

    return


def test_simple2():
    X = numpy.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0],
        [0.7, 0.5],
        [1.7, 0.5],
        ])
    cells = numpy.array([
        [0, 1, 4],
        [1, 5, 4],
        [2, 4, 5],
        [2, 3, 4],
        [3, 0, 4],
        ])

    X, cells = optimesh.odt(X, cells)

    # Test if we're dealing with the mesh we expect.
    nc = X.flatten()
    norm1 = numpy.linalg.norm(nc, ord=1)
    norm2 = numpy.linalg.norm(nc, ord=2)
    normi = numpy.linalg.norm(nc, ord=numpy.inf)

    tol = 1.0e-12
    ref = 7.374076666666667
    assert abs(norm1 - ref) < tol * ref
    ref = 2.8007819180622477
    assert abs(norm2 - ref) < tol * ref
    ref = 1.7
    assert abs(normi - ref) < tol * ref

    return


def test_simple3():
    X = numpy.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [2.0, 0.0],
        [2.0, 1.0],
        [1.0, 1.0],
        [0.0, 1.0],
        [0.7, 0.5],
        [1.7, 0.5],
        ])
    cells = numpy.array([
        [0, 1, 6],
        [1, 7, 6],
        [1, 2, 7],
        [2, 3, 7],
        [3, 4, 7],
        [4, 6, 7],
        [4, 5, 6],
        [5, 0, 6],
        ])

    X, cells = optimesh.odt(X, cells)

    # Test if we're dealing with the mesh we expect.
    nc = X.flatten()
    norm1 = numpy.linalg.norm(nc, ord=1)
    norm2 = numpy.linalg.norm(nc, ord=2)
    normi = numpy.linalg.norm(nc, ord=numpy.inf)

    tol = 1.0e-12
    ref = 12.000000734595783
    assert abs(norm1 - ref) < tol * ref
    ref = 3.9828838201616144
    assert abs(norm2 - ref) < tol * ref
    ref = 2.0
    assert abs(normi - ref) < tol * ref

    return


def test_pacman():
    filename = download_mesh(
        'pacman.msh',
        '601a51e53d573ff58bfec96aef790f0bb6c531a221fd7841693eaa20'
        )
    mesh = meshio.read(filename)
    assert numpy.all(numpy.abs(mesh.points[:, 2]) < 1.0e-15)
    X = mesh.points[:, :2]

    X, cells = optimesh.odt(
        X, mesh.cells['triangle'],
        verbose=True,
        tol=1.0e-5
        )

    # Test if we're dealing with the mesh we expect.
    nc = X.flatten()
    norm1 = numpy.linalg.norm(nc, ord=1)
    norm2 = numpy.linalg.norm(nc, ord=2)
    normi = numpy.linalg.norm(nc, ord=numpy.inf)

    tol = 1.0e-8
    ref = 1919.249752617539
    assert abs(norm1 - ref) < tol * ref
    ref = 75.22699025430875
    assert abs(norm2 - ref) < tol * ref
    ref = 5.0
    assert abs(normi - ref) < tol * ref

    return


def circle():
    filename = 'circle.vtk'
    if not os.path.isfile(filename):
        import pygmsh
        geom = pygmsh.built_in.Geometry()
        geom.add_circle(
            [0.0, 0.0, 0.0],
            1.0,
            5.0e-3,
            # 1.0e-2,
            num_sections=4,
            # If compound==False, the section borders have to be points of the
            # discretization. If using a compound circle, they don't; gmsh can
            # choose by itself where to point the circle points.
            compound=True
            )
        X, cells, _, _, _ = pygmsh.generate_mesh(
            geom, fast_conversion=True,
            remove_faces=True
            )
        meshio.write(filename, X, cells)

    mesh = meshio.read(filename)

    # TODO remove this
    X = mesh.points[:, :2]

    c = mesh.cells['triangle'].astype(numpy.int)

    X, cells = optimesh.odt(
        X, c,
        verbose=True,
        # tol=3.0e-8
        tol=2.0e-8
        )
    return


if __name__ == '__main__':
    # test_simple1()
    # test_simple2()
    # test_simple3()
    # test_pacman()
    circle()
