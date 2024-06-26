import meshplex
import numpy as np
import scipy.sparse.linalg


# The density-preserving CPT is exactly Laplacian smoothing.
def get_new_points(mesh: meshplex.Mesh) -> np.ndarray:
    matrix = _build_graph_laplacian(mesh)

    n = mesh.points.shape[0]
    rhs = np.zeros((n, mesh.points.shape[1]))
    rhs[mesh.is_boundary_point] = mesh.points[mesh.is_boundary_point]

    out = scipy.sparse.linalg.spsolve(matrix, rhs)

    # PyAMG fails on circleci.
    # ml = pyamg.ruge_stuben_solver(matrix)
    # # Keep an eye on multiple rhs-solves in pyamg,
    # # <https://github.com/pyamg/pyamg/issues/215>.
    # out = np.column_stack(
    #     [ml.solve(rhs[:, 0], tol=tol), ml.solve(rhs[:, 1], tol=tol)]
    # )
    return out


def _build_graph_laplacian(mesh: meshplex.Mesh):
    i = mesh.idx[-1]
    row_idx = np.array([i[0], i[1], i[0], i[1]]).flat
    col_idx = np.array([i[0], i[1], i[1], i[0]]).flat
    a = np.ones(i.shape[1:], dtype=int)
    val = np.array([+a, +a, -a, -a]).flat

    # Create CSR matrix for efficiency
    n = mesh.points.shape[0]
    matrix = scipy.sparse.coo_matrix((val, (row_idx, col_idx)), shape=(n, n))
    matrix = matrix.tocsr()

    # Apply Dirichlet conditions.
    verts = np.where(mesh.is_boundary_point)[0]
    # Set all Dirichlet rows to 0.
    for i in verts:
        matrix.data[matrix.indptr[i] : matrix.indptr[i + 1]] = 0.0
    # Set the diagonal and RHS.
    d = matrix.diagonal()
    d[mesh.is_boundary_point] = 1.0
    matrix.setdiag(d)
    return matrix
