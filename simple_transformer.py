import numpy as np

class SimpleTransformer:
    def __init__(self, vocab_size, d_model):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.embedding = np.random.randn(vocab_size, d_model)

    def forward(self, x, transpose_axes=(0, 2, 1)):
        x_embedded = self.embedding[x]  # Shape: (batch_size, sequence_length, d_model)
        Q = K = V = x_embedded
        attention_scores = np.matmul(Q, K.transpose(transpose_axes)) / np.sqrt(K.shape[-1])
        attention_weights = self.softmax(attention_scores, axis=-1)
        output = np.matmul(attention_weights, V)
        return output

    def softmax(self, x, axis=None):
        x_max = np.max(x, axis=axis, keepdims=True)
        e_x = np.exp(x - x_max)
        return e_x / np.sum(e_x, axis=axis, keepdims=True)

    def gen(self, input_indices, transpose_axes=(0, 2, 1)):
        input_indices = np.array(input_indices, dtype=np.int32)
        output = self.forward(input_indices, transpose_axes=transpose_axes)
        return output

def main():
    
    model = SimpleTransformer(vocab_size=10, d_model=2)
    matrix1 = [[1,2], [3,4]]
    output = model.gen(matrix1)

    expected_result = np.array([
        [[-1.07381302, -0.35631778], [-0.0082236, -0.33212289]],
        [[1.18010406, 0.64358659], [0.58773279, -0.32573123]]
    ])

    print("type: ", type(output))
    print("shape: ", output.shape)
    # assert output == documents, f"Expected: {documents}, Actual: {output}"

    print("input:\n", matrix1)
    print("output:\n", output)

if __name__ == "__main__":
    main()
