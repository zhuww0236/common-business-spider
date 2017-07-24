#!/bin/sh

cd "$(dirname "$0")"
nohup python goodSpider.py >> log/myout.out 2>&1 &
