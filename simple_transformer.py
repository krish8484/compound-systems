import numpy as np
import os
import time
import psutil
import argparse
from retrieval_module import retrieve_documents  

class SimpleTransformer:
    def __init__(self, vocab_size, d_model, seed_val=48):
        self.vocab_size = vocab_size
        self.d_model = d_model
        np.random.seed(seed_val)
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

def rag(knowledge, embedding, model, steps=5):
    retrieved_output = retrieve_documents(knowledge, embedding, top_k=1) 
    matrix1 = np.array(retrieved_output).reshape(2, 2)
    generation_output = model.gen(matrix1) 
    return generation_output

def measure_performance(vocab_size, d_model, batch_size, seq_length, n):
    documents = [[1, 2], [3, 4]]
    embeddings = [[5, 6], [7, 8]]
    generations = []
    model = SimpleTransformer(vocab_size, d_model)

    start_time = time.time()
    for i in range(n):
        generation_output = rag(documents, embeddings, model)
        generations.append(generation_output)
    end_time = time.time()

    elapsed_time = end_time - start_time
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss  

    return elapsed_time, memory_usage

def main():
    parser = argparse.ArgumentParser(description="run RAG with varying parameters")
    parser.add_argument("-n", type=int, default=5, help="number of iterations")
    args = parser.parse_args()
    n = args.n

    vocab_sizes = [100, 1000, 5000, 10000, 100000]
    d_models = [20, 80, 200, 500, 10000]
    batch_sizes = [10, 100, 500, 1000, 50000]
    seq_length = 100  

    # run sim varying gen model params and track space-time (memory, latency)
    with open("performance_log.txt", "w") as f:
        f.write("vocab_size, d_model, batch_size, elapsed_time, memory_usage\n")
        for vocab_size in vocab_sizes:
            for d_model in d_models:
                for batch_size in batch_sizes:
                    elapsed_time, memory_usage = measure_performance(vocab_size, d_model, batch_size, seq_length, n)
                    f.write(f"{vocab_size},{d_model},{batch_size},{elapsed_time:.4f},{memory_usage / 1e6:.2f}\n")
    
    print("simulation complete")

if __name__ == "__main__":
    main()
