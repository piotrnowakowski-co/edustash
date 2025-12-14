import numpy as np

from snax.ml.models.base import ModelProtocol


class KMeans(ModelProtocol):
    """K-Means clustering algorithm implementation.

    :param n_clusters: Number of clusters to form.
    :param max_iter: Maximum number of iterations.
    :param tol: Tolerance to declare convergence.

    """

    def __init__(self, n_clusters=8, max_iter=300, tol=1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.centroids = None

    def fit(self, X):
        # Randomly initialize centroids
        X_ = X.reset_index()
        random_indices = np.random.choice(X_.shape[0], self.n_clusters, replace=False)
        self.centroids = X[random_indices]

        for _ in range(self.max_iter):
            # Assign clusters
            distances = np.linalg.norm(
                np.array(X)[:, np.newaxis] - self.centroids, axis=2
            )
            labels = np.argmin(distances, axis=1)

            # Compute new centroids
            new_centroids = np.array(
                [X[labels == k].mean(axis=0) for k in range(self.n_clusters)]
            )

            # Check for convergence
            if np.linalg.norm(new_centroids - self.centroids) < self.tol:
                break

            self.centroids = new_centroids

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)
