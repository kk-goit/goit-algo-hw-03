import argparse
import shutil
from pathlib import Path

def file_error(preffix):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except (Exception) as err:
                print(f"{preffix} because {err}")

        return inner
    
    return decorator

@file_error("Can't copy file")
def do_copy(file: Path, dir_to: str):
    """Try to copy file to distination"""
    ext = file.suffix[1:] if len(file.suffix) > 0 else 'unknown'
    dst = Path(dir_to + "/" + ext)
    dst.mkdir(exist_ok = True)
    shutil.copy(file, dst)
    print(f"Copied file {file.name} to {dir_to}/{ext}")

@file_error("Can't open dir")
def find_and_copy(root: Path, dir_to: str, pref_path = ''):
    """Search files in folder and copy it"""
    if root.is_dir():
        print(f"Search files in folder {pref_path}{root.name}")
        for item in root.iterdir():
            find_and_copy(item, dir_to, pref_path + root.name + "/")
    elif root.is_file():
        do_copy(root, dir_to)
    else:
        print(f"{root.name} is not a file or folder")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog =        'HomeWork3Task1',
        description = 'Collect files by extensions',
        epilog =      'GoIT Tier-1 Algorithms'
    )
    parser.add_argument('dir_from', help="source dir")
    parser.add_argument('dir_to', default="dist", nargs='?', help="distination folder")

    args = parser.parse_args()
    dist = Path(args.dir_to)
    if not dist.exists():
        print(f"Destination '{args.dir_to}' does not exists")
    elif not dist.is_dir():
        print(f"Destination '{args.dir_to}' is not a folder")
    else:
        find_and_copy(Path(args.dir_from), args.dir_to)
