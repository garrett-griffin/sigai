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
            if verbose:
                print(f"Verbose mode: Including file: {file_content.path}")
                files.append(file_content)
            else:
                if "__init__.py" in file_content.path or "tests/" in file_content.path:
                    print(f"Skipping file: {file_content.path}")
                else:
                    print(f"Including file: {file_content.path}")
                    files.append(file_content)

    print(f"Total files fetched: {len(files)}")
    return files

def get_return_annotation(node):
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return '.'.join([node.value.id, node.attr])
    elif isinstance(node, ast.Subscript):
        return get_return_annotation(node.value)
    return "None"

def extract_docstring(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        docstring = ast.get_docstring(node)
        return docstring.split('\n')[0] if docstring else None
    return None

def parse_file(file_content, include_descriptions=True):
    tree = ast.parse(file_content)
    summary = []
    has_content = False

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            returns = get_return_annotation(node.returns) if node.returns else "None"
            line = f"{node.name}({', '.join(args)}) -> {returns}"
            if include_descriptions:
                docstring = extract_docstring(node)
                if docstring:
                    line += f" - {docstring}"
            summary.append(line)
            has_content = True
        elif isinstance(node, ast.ClassDef):
            class_summary = [f"{node.name}"]
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    args = [arg.arg for arg in item.args.args]
                    returns = get_return_annotation(item.returns) if item.returns else "None"
                    line = f"  {item.name}({', '.join(args)}) -> {returns}"
                    if include_descriptions:
                        docstring = extract_docstring(item)
                        if docstring:
                            line += f" - {docstring}"
                    class_summary.append(line)
                    has_content = True
            summary.append("\n".join(class_summary))

    return summary if has_content else None

def generate_summary(repo_url, verbose=False, include_descriptions=True):
    files = fetch_files_from_github(repo_url, verbose)
    summary = []

    for file in files:
        file_content = requests.get(file.download_url).text
        file_summary = parse_file(file_content, include_descriptions)
        if file_summary is not None or verbose:
            summary.append(f"{file.path}\n" + "\n".join(file_summary or []))

    return "\n\n".join(summary)

def main():
    parser = argparse.ArgumentParser(description="Generate a summary of function signatures and class methods from a given GitHub repository.")
    parser.add_argument("repo_url", help="The URL of the GitHub repository")
    parser.add_argument("--output", help="The output file to save the summary", default="summary.txt")
    parser.add_argument("--verbose", action="store_true", help="Include __init__.py files and files in tests/ folders and empty files")
    parser.add_argument("--include_descriptions", action="store_true", default=True, help="Include function descriptions if available")

    args = parser.parse_args()

    summary = generate_summary(args.repo_url, verbose=args.verbose, include_descriptions=args.include_descriptions)
    with open(args.output, "w") as f:
        f.write(summary)
    print(f"Summary generated and saved to {args.output}")

if __name__ == "__main__":
    main()
