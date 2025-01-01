"""
Script to create and upload a dataset to Hugging Face under the user 'masoudc'.

Usage:
1. Install requirements: pip install huggingface_hub
2. Obtain a valid Hugging Face token with write access.
3. Set your HF_TOKEN environment variable or replace HF_TOKEN below with your token.
4. Prepare your local dataset files in a folder (e.g., ./my_dataset).
5. Run this script to create/upload the dataset repo, README, and files.
"""

import os
from huggingface_hub import HfApi, Repository

HF_TOKEN = os.getenv("HF_TOKEN") or "hf_your_write_access_token_here"
HF_USERNAME = "masoudc"
META_TOPIC = "distribution-parallelism"
REPO_NAME = "mmlu-college-computer-science-" + META_TOPIC

# Local path to your dataset folder
LOCAL_DATASET_FOLDER = "./mmlu-" + META_TOPIC

README_CONTENT = """---
datasets:
- name: mmlu-college-computer-science-{META_TOPIC}
- licenses: ["MIT"]
- language: ["en"]
---
# extensions to the mmlu computer science datasets for specialization in {META_TOPIC}.

This is a sample dataset uploaded via `huggingface_hub`. It includes:
- A README file with metadata
- CSV or JSON data stored in this repository

## Usage
You can use `datasets.load_dataset()` to load this dataset.
"""

def create_and_upload_dataset():
    api = HfApi(token=HF_TOKEN)
    
    full_repo_name = f"{HF_USERNAME}/{REPO_NAME}"

    # Create a new dataset repository (or skip if it already exists)
    try:
        api.create_repo(repo_id=full_repo_name, repo_type="dataset", exist_ok=False)
        print(f"Created new repo: {full_repo_name}")
    except Exception as e:
        if "Conflict" in str(e):
            print(f"Repository '{full_repo_name}' already exists. Proceeding...")
        else:
            raise e

    # Clone the repository locally
    repo_local_path = f"./{REPO_NAME}_repo"
    repo = Repository(local_dir=repo_local_path, clone_from=full_repo_name, repo_type="dataset")
    
    # Write the README with metadata
    readme_path = os.path.join(repo_local_path, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(README_CONTENT)

    # Copy dataset files from LOCAL_DATASET_FOLDER to the cloned repo
    for filename in os.listdir(LOCAL_DATASET_FOLDER):
        src_path = os.path.join(LOCAL_DATASET_FOLDER, filename)
        dst_path = os.path.join(repo_local_path, filename)
        if os.path.isfile(src_path):
            with open(src_path, "rb") as src, open(dst_path, "wb") as dst:
                dst.write(src.read())
            print(f"Copied {filename} into the repo.")

    # Publish the changes to the remote repository
    repo.git_add(auto_lfs_track=True)
    repo.git_commit("Add dataset files and README with metadata")
    repo.git_push()
    print(f"Dataset successfully pushed to https://huggingface.co/datasets/{full_repo_name}")

if __name__ == "__main__":
    create_and_upload_dataset()
