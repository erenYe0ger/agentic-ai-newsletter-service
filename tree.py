import os

IGNORED_DIRS = {
    ".venv", "__pycache__", ".git", ".idea", ".vscode", "dist", "build"
}

IGNORED_FILES = {
    ".DS_Store"
}

def print_tree(start_path, prefix=""):
    items = sorted(os.listdir(start_path))
    items = [i for i in items if i not in IGNORED_FILES]

    for idx, item in enumerate(items):
        path = os.path.join(start_path, item)
        connector = "└── " if idx == len(items) - 1 else "├── "

        # Skip ignored directories
        if os.path.isdir(path) and item in IGNORED_DIRS:
            continue

        print(prefix + connector + item)

        # If directory, recurse
        if os.path.isdir(path):
            extension = "    " if idx == len(items) - 1 else "│   "
            print_tree(path, prefix + extension)


if __name__ == "__main__":
    print("Project Structure:\n")
    print_tree(".")