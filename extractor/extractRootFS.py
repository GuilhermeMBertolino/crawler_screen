import binwalk
import shutil
import tempfile
import os
from findRootFS import findRootFS

file_extensions = [".bin", ".trx", ".img", ".tar", ".tar.gz", ".tar.bz2", ".tar.xz", ".tar.lzma",
                    ".tar.lz", ".tar.lzo", ".tar.lz4", ".tar.Z", ".tar.zst", ".tar.sz", ".tar.z",
                    ".tar.lzop", ".tar.lz", ".tar.lz4", ".tar.xz", ".tar.bz2", ".tar.gz", ".tar",
                    ".tgz", ".tbz2", ".txz", ".tlz", ".tlzma", ".tlzo", ".tlzop", ".tlz4", ".tlz",
                    ".tzst", ".tsz", ".tz", ".tZ", ".zip", ".7z", ".rar", ".zst", ".sz", ".z",
                    ".lzop", ".lzma", ".lz4", ".lz"]

def extractRootFS(image, vendor, model, depth=0, max_depth=10):
    temp = tempfile.mkdtemp()
    output_dir = os.path.join("extracted", vendor, model)
    depth = depth + 1

    if depth > max_depth:
        print("Max depth reached, extraction failed")
        return False

    for module in binwalk.scan(image, "--run-as=root", "--preserve-symlinks",
                               "-e", "-r", "-C", temp, signature=True, quiet=True):
        for entry in module.results:
            desc = entry.description
            dirname = module.extractor.directory
            if "filesystem" in desc:
                print("Extracting filesystem")
                if dirname:
                    unix = findRootFS(dirname)
                    if unix[0]:
                        print("Unix fs found at", unix[1])
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        for root, dir, files in os.walk(unix[1]):
                            for name in dir + files:
                                path = os.path.join(root, name)
                                if not os.path.islink(path):
                                    new_path = os.path.join(output_dir, os.path.relpath(path, unix[1]))
                                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                                    shutil.move(path, new_path)
                        return True
                    else:
                        print("No unix fs found")
                break
            elif ("archive" in desc or "compressed" in desc) and any(ext in desc for ext in file_extensions):
                for root, dir, files in os.walk(dirname):
                    for filename in files:
                        if any(ext in filename for ext in file_extensions):
                            extractRootFS(os.path.join(root, filename), vendor, model, depth, max_depth)
                break

        return False   