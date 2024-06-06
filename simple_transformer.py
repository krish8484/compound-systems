import numpy as np

class SimpleTransformer:
    def __init__(self, vocab_size, d_model):
        self.vocab_size = vocab_size
        self.d_model = d_model
        np.random.seed(42)
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
        [[0.5671, 1.3624], [0.112, 0.4556]],
        [[1.4104, 0.7489], [0.2594, 0.6226]]
    ])

    print("type: ", type(output))
    print("shape: ", output.shape)
    print("type: ", type(expected_result))
    print("shape: ", expected_result.shape)
    
    output = np.ceil(output * 10000) / 10000    

    print("\n output: ", output)
    print("\n expected: ", expected_result, "\n")

    assert np.array_equal(output, expected_result), "Expected is not Actual"

    print("input:\n", matrix1)
    print("output:\n", output)

if __name__ == "__main__":
    main()
