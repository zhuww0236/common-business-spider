#!/bin/sh

cd "$(dirname "$0")"
nohup python goodsItemSpiderWhole.py >> log/myout.out 2>&1 &
