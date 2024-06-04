import numpy as np

class SimpleRetrieval:
    def __init__(self, matrix1, matrix2, top_k):
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.top_k = top_k

    def retrieval(self, matrix1, matrix2, top_k=1):
        matrix1 = np.array(matrix1)
        matrix2 = np.array(matrix2)
        dot_prod = np.dot(matrix1, matrix2)
        mag_1 = np.linalg.norm(matrix1)
        mag_2 = np.linalg.norm(matrix2)
        sim = dot_prod / (mag_1 * mag_2)
        top_indices = np.argsort(sim)[-top_k:][::-1][0]
        result = [matrix1[i].tolist() for i in top_indices]
        return result

def main():
    
    documents = [[1,2], [3,4]]
    embeddings = [[5, 6], [7, 8]]
    model = SimpleRetrieval(documents, embeddings, top_k=1)
    output = model.retrieval(documents, embeddings)

    print("documents:\n", documents)
    print("embeddings:\n", embeddings)
    print("output:\n", output)    

    assert output == documents, f"Expected: {documents}, Actual: {output}"

if __name__ == "__main__":
    main()

