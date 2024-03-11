#!/bin/bash

OPTIND=1
while getopts ":h" opt; do
    case $opt in
        h)
            echo "Command usage: ./crawl [options] [arguments]"
            echo "Options:"
            echo "  -h      Show command usage"
            echo "Arguments:"
            echo "  First argument is the vendor whose website to crawl, by default, the command will crawl every vendor in the spiders folder"
            exit 0
            ;;
    esac
done

if [ -n "$1" ] && [ -e "./spiders/$1.py" ]; then
    echo "Crawling $1 website ..."
    scrapy runspider spiders/$1.py --nolog
    echo "Done"
    exit 0
elif [ -n "$1" ]; then
    echo "Bad argument, use crawl -h to see command usage"
    exit 0
fi

for file in ./spiders/*.py; do
    vendor=$(basename ${file%.*})
    echo "$vendor"
    if [ ! -d "firmwares/$(basename "$file")" ]; then
        mkdir firmwares/$(basename "$file")
    fi
    echo "Crawling $(basename "$file") website ..."
    scrapy runspider $file --nolog
done

echo "Done"
