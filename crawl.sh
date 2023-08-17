#!/bin/sh

for file in ./spiders/*.py; do
    if [ ! -d "firmwares/$(basename "$file")" ]; then
        mkdir firmwares/$(basename "$file")
    fi
    echo "Crawling $(basename "$file") website ..."
    scrapy runspider $file > /dev/null 2>&1
done
