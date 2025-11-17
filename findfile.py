import os
from pathlib import Path
import fnmatch
import sys

def find_files_by_name(root, name):
    """Mengembalikan list path file yang namanya tepat sama dengan `name` (rekursif)."""
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            if f == name:
                matches.append(os.path.join(dirpath, f))
    return matches

# contoh
# hasil = find_files_by_name("/home/user", "catatan.txt")
# print(*hasil, sep="\n")

def find_files_by_pattern(root, pattern):
    """pattern contoh: '*.py', 'data_*.csv'"""
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            if fnmatch.fnmatch(f, pattern):
                matches.append(os.path.join(dirpath, f))
    return matches

# contoh: find_files_by_pattern(".", "*.py")


def find_with_pathlib(root, pattern="*"):
    p = Path(root)
    return [str(pth) for pth in p.rglob(pattern)]

# contoh: find_with_pathlib(".", "*.md")

def gen_find(root, pattern=None):
    """Generator: yield path. pattern optional: fnmatch style."""
    import fnmatch
    for entry in os.scandir(root):
        if entry.is_file():
            if pattern is None or fnmatch.fnmatch(entry.name, pattern):
                yield entry.path
        elif entry.is_dir():
            yield from gen_find(entry.path, pattern)

# contoh penggunaan:
# for p in gen_find("/home/user", "*.log"):
#     print(p)

def find_files_containing(root, text, encoding="utf-8"):
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            try:
                with open(path, "r", encoding=encoding, errors="ignore") as f:
                    for line in f:
                        if text in line:
                            matches.append(path)
                            break
            except (IsADirectoryError, PermissionError):
                continue
    return matches
print(find_files_containing("../", "nama"))
print(find_files_by_name("../sekolah", "AI"))
print(find_files_by_pattern("../AI","*.py"))
print()
print()
# contoh: find_files_containing(".", "TODO")
# simpan sebagai findfile.py lalu:
# python findfile.py /path/to/root "*.py"

def main(root, pattern):
    for p in Path(root).rglob(pattern):
        print(p)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python findfile.py ROOT PATTERN")
    else:
        main(sys.argv[1], sys.argv[2])
