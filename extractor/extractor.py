import os
from extractRootFS import extractRootFS

for subdir in os.listdir("../firmwares2"):
    if os.path.isdir(os.path.join("../firmwares2", subdir)):
        for file in os.listdir(os.path.join("../firmwares2", subdir)):
            extractRootFS(os.path.join("../firmwares2", subdir, file), subdir, file.split(".")[0])