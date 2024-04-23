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
    if [ ! -d "firmwares/$1" ]; then
        mkdir firmwares/$1
    fi
    echo "Crawling $1 website ..."
    scrapy runspider spiders/$1.py
    echo "Done"
    exit 0
elif [ -n "$1" ]; then
    echo "Bad argument, use crawl -h to see command usage"
    exit 0
fi

crawler_pids=()

finish() {
    for pid in "${crawler_pids[@]}"; do
        kill $pid
        echo "Killed crawler with pid $pid"
    done
    exit 0
}

trap finish SIGINT SIGTERM SIGKILL

for file in ./spiders/*.py; do
    vendor=$(basename ${file%.*})
    if [ ! -d "firmwares/$(basename "$file" .py)" ]; then
        mkdir firmwares/$(basename "$file" .py)
    fi
    echo "Crawling $(basename "$file" .py) website ..."
    scrapy runspider $file --nolog &
done

while true; do
    for pid in $(pgrep -f "scrapy runspider"); do
        if ! ps -p $pid > /dev/null; then
            echo "Crawler with pid $pid has finished"
            crawler_pids=("${crawler_pids[@]}" $pid)
        fi
    done
    if [ ${#crawler_pids[@]} -eq $(ls ./spiders | wc -l) ]; then
        break
    fi
    sleep 1
done

echo "Done"
