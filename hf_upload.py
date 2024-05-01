from fire import Fire
from datasets import load_dataset
from gzip import GzipFile
from huggingface_hub import create_tag, list_repo_refs, delete_tag

REPO_ID = "evalplus/humanevalplus"


def main(version: str, overwrite=False):
    # read HumanEvalPlus-OriginFmt.jsonl.gz to test.jsonl
    with GzipFile("HumanEvalPlus-OriginFmt.jsonl.gz", "rb") as f:
        with open("test.jsonl", "wb") as f_out:
            f_out.write(f.read())

    repo = list_repo_refs(REPO_ID, repo_type="dataset")
    tags = [tag.name for tag in repo.tags]
    print(REPO_ID, "has tags:", tags)

    dataset = load_dataset("json", data_files={"test": "test.jsonl"}, split="test")
    print(dataset)
    print(f"Uploading dataset with tag {version} to Hub... Please enter to confirm:")
    input()

    if version in tags and overwrite:
        print(f"Tag {version} already exists, overwriting...")
        delete_tag(REPO_ID, repo_type="dataset", tag=version)

    dataset.push_to_hub(REPO_ID, branch="main")
    create_tag(REPO_ID, repo_type="dataset", tag=version)


if __name__ == "__main__":
    Fire(main)
