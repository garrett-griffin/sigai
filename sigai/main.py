# sigai/main.py

import requests
from github import Github
import ast
import sys
import argparse

def fetch_files_from_github(repo_url, verbose=False):
    repo_name = repo_url.rstrip('/').split('/')[-1]
    user_name = repo_url.rstrip('/').split('/')[-2]
    g = Github()
    repo = g.get_repo(f"{user_name}/{repo_name}")
    contents = repo.get_contents("")
    files = []

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        elif file_content.path.endswith(".py"):
            if not verbose:
                if "__init__.py" in file_content.path or "tests/" in file_content.path:
                    continue
            files.append(file_content)

    return files

def parse_file(file_content):
    tree = ast.parse(file_content)
    summary = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            returns = node.returns.id if node.returns else "None"
            summary.append(f"{node.name}({', '.join(args)}) -> {returns}")
        elif isinstance(node, ast.ClassDef):
            class_summary = [f"{node.name}"]
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = [arg.arg for arg in item.args.args]
                    returns = item.returns.id if item.returns else "None"
                    class_summary.append(f"  {item.name}({', '.join(args)}) -> {returns}")
            summary.append("\n".join(class_summary))

    return summary

def generate_summary(repo_url, verbose=False):
    files = fetch_files_from_github(repo_url, verbose)
    summary = []

    for file in files:
        file_content = requests.get(file.download_url).text
        file_summary = parse_file(file_content)
        summary.append(f"{file.path}\n" + "\n".join(file_summary))

    return "\n\n".join(summary)

def main():
    parser = argparse.ArgumentParser(description="Generate a summary of function signatures and class methods from a given GitHub repository.")
    parser.add_argument("repo_url", help="The URL of the GitHub repository")
    parser.add_argument("--output", help="The output file to save the summary", default="summary.txt")
    parser.add_argument("--verbose", action="store_true", help="Include __init__.py files and files in tests/ folders")

    args = parser.parse_args()

    summary = generate_summary(args.repo_url, verbose=args.verbose)
    with open(args.output, "w") as f:
        f.write(summary)
    print(f"Summary generated and saved to {args.output}")

if __name__ == "__main__":
    main()
