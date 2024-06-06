from retrieval_module import retrieve_documents

def main():
    documents = [[1, 2], [3, 4]]
    embeddings = [[5, 6], [7, 8]]
    output = retrieve_documents(documents, embeddings, top_k=1)

    print("documents:\n", documents)
    print("embeddings:\n", embeddings)
    print("output:\n", output)    

if __name__ == "__main__":
    main()
