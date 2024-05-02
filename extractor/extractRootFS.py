import binwalk
import shutil
import tempfile
import os
from findRootFS import findRootFS

def extractRootFS(image, vendor, model, depth=0, max_depth=10):
    temp = tempfile.mkdtemp()
    output_dir = os.path.join(vendor, model)
    depth = depth + 1

    if depth > max_depth:
        print("Max depth reached, extraction failed")
        return

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
                        shutil.make_archive(os.path.abspath(output_dir), "zip", root_dir=unix[1])
                    else:
                        print("No unix fs found")
                break
            elif ("archive" in desc or "compressed" in desc) and ".bin" in desc:
                print(dirname)
                for root, dir, files in os.walk(dirname):
                    for filename in files:
                        if filename.endswith(".bin"):
                            print("Extracting", filename)
                            print(depth)
                            extractRootFS(os.path.join(root, filename), vendor, model, depth, max_depth)
                