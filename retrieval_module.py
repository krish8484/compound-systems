import numpy as np

class SimpleRetrieval:
    def __init__(self, matrix1, matrix2, top_k):
        self.matrix1 = np.array(matrix1)
        self.matrix2 = np.array(matrix2)
        self.top_k = top_k

    def retrieval(self, matrix1, matrix2, top_k=1):
        matrix1 = np.array(matrix1)
        matrix2 = np.array(matrix2)
        dot_prod = np.dot(matrix1, matrix2.T)  # Adjusted for correct matrix multiplication
        mag_1 = np.linalg.norm(matrix1, axis=1)[:, None]  # Adjusted for correct norm calculation
        mag_2 = np.linalg.norm(matrix2, axis=1)[None, :]  # Adjusted for correct norm calculation
        sim = dot_prod / (mag_1 * mag_2)
        top_indices = np.argsort(sim, axis=1)[:, -top_k:][:, ::-1]
        result = [[matrix2[j].tolist() for j in indices] for indices in top_indices]
        return result

def retrieve_documents(documents, embeddings, top_k):
    model = SimpleRetrieval(documents, embeddings, top_k)
    return model.retrieval(documents, embeddings)
