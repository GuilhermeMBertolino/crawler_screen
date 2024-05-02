import os

UNIX_DIRS = ["bin", "etc", "dev", "home", "lib", "mnt", "opt", "root", "run", "sbin", "tmp", "usr", "var"]
UNIX_THRESHOLD = 4

def findRootFS(start, max_depth=10):
    max_dir = start
    max_subdirs = 0

    queue = [(start, 0)]

    while queue:
        path, depth = queue.pop(0)

        if depth > max_depth:
            if max_subdirs >= UNIX_THRESHOLD:
                return (True, max_dir)
            return (False, max_dir)

        count = 0
        for subdir in os.listdir(path):
            if os.path.isdir(os.path.join(path, subdir)):
                queue.append((os.path.join(path, subdir), depth + 1))
                if subdir in UNIX_DIRS and len(os.listdir(os.path.join(path, subdir))) > 0:
                    count += 1

        if count > max_subdirs:
            max_subdirs = count
            max_dir = path