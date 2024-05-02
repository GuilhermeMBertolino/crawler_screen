import binwalk
import shutil
import tempfile
import os
from findRootFS import findRootFS

def extractRootFS(image, output_dir):
    temp = tempfile.mkdtemp()
    for module in binwalk.scan(image, "--run-as=root", "--preserve-symlinks",
                               "-e", "-r", "-C", temp, signature=True, quiet=True):
        for entry in module.results:
            desc = entry.description
            if "filesystem" in desc:
                if "filesystem" in desc or "archive" in desc or "compressed" in desc:
                    dirname = module.extractor.directory
                    if dirname:
                        unix = findRootFS(dirname)
                        if unix[0]:
                            shutil.make_archive(os.path.abspath(output_dir), "zip", root_dir=unix[1])
                    break

extractRootFS("AD7200.bin", "./fs")