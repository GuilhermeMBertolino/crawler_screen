import os
import warnings
from extractRootFS import extractRootFS

warnings.filterwarnings("ignore")

for subdir in os.listdir("../firmwares2"):
    if os.path.isdir(os.path.join("../firmwares2", subdir)):
        for file in os.listdir(os.path.join("../firmwares2", subdir)):
            print(f"Extracting {subdir}/{file}")
            if extractRootFS(os.path.join("../firmwares2", subdir, file), subdir, file.split(".")[0]):
                with open("extracted.txt", "a") as f:
                    f.write(f"{subdir}/{file} - Extraction successful\n")
            else:
                with open("extracted.txt", "a") as f:
                    f.write(f"{subdir}/{file} - Extraction failed\n")