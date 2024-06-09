# sigai/main.py

import requests
from github import Github
import ast

# Function to fetch files from a GitHub repository
def fetch_files_from_github(repo_url):
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
            files.append(file_content)

    return files

# Function to parse Python files and extract function signatures
def parse_file(file_content):
    tree = ast.parse(file_content)
    summary = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            returns = node.returns.id if node.returns else "None"
            summary.append(f"Function: {node.name}({', '.join(args)}) -> {returns}")
        elif isinstance(node, ast.ClassDef):
            class_summary = [f"Class: {node.name}"]
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = [arg.arg for arg in item.args.args]
                    returns = item.returns.id if item.returns else "None"
                    class_summary.append(f"  Method: {item.name}({', '.join(args)}) -> {returns}")
            summary.append("\n".join(class_summary))

    return summary

# Function to generate the summary for a GitHub repository
def generate_summary(repo_url):
    files = fetch_files_from_github(repo_url)
    summary = []

    for file in files:
        file_content = requests.get(file.download_url).text
        file_summary = parse_file(file_content)
        summary.append(f"File: {file.path}\n" + "\n".join(file_summary))

    return "\n\n".join(summary)

# Example usage
if __name__ == "__main__":
    repo_url = "https://github.com/your_username/your_repository"
    summary = generate_summary(repo_url)
    with open("summary.txt", "w") as f:
        f.write(summary)
    print("Summary generated and saved to summary.txt")
