#!/bin/sh

# 京东蜘蛛监控和交互
# xiangcy 2017-04-17

cd "$(dirname "$0")"

while [ $# -ne 0 ]
do
  while getopts :b:e:c:d:o:y:s: optname
  do
    case $optname in
    b)
      btime=$OPTARG
      ;;
    e)
      etime=$OPTARG
      ;;
    c)
      # 启动按分类爬取脚本
      # echo '启动按分类爬取脚本'
      pythonJobList=$(ps -ef | grep 'goodsItemSpiderWhole.py' | wc -l )
      if [ "x${pythonJobList}" == "x1" ]
      then
        `nohup python goodsItemSpiderWhole.py >> js_daemon.out 2>&1 &`
      fi
      ;;
    i)
      # 启动按ID爬取脚本
      # echo '启动按ID爬取脚本'
      pythonJobList=$(ps -ef | grep 'goodsSpider.py' | wc -l )
      if [ "x${pythonJobList}" == "x1" ]
      then
        `nohup python goodsSpider.py >> js_daemon.out 2>&1 &`
      fi
      ;;
    s)
      # 检查已经启动的脚本
      # echo '检查已经启动的脚本'
      pythonJobList=$(ps -ef | grep 'goodsSpider.py' | wc -l )
      if [ "x${pythonJobList}" == "x2" ]
      then
        echo 'running goodsSpider.py'
      else
        echo 'stop goodsSpider.py'
      fi
      pythonJobList=$(ps -ef | grep 'goodsItemSpiderWhole.py' | wc -l )
      if [ "x${pythonJobList}" == "x2" ]
      then
        echo 'running goodsItemSpiderWhole.py'
      else
        echo 'stop goodsItemSpiderWhole.py'
      fi
      ;;
    p)
      province_id=`echo ${OPTARG} | tr A-Z a-z`
      ;;
    esac
  done
  shift
done

pythonJobList=$(ps -ef | grep 'goodsItemSpiderWhole.py' | wc -l )
if [ "x${pythonJobList}" == "x1" ]
then
  `nohup python goodsItemSpiderWhole.py >> js_daemon.out 2>&1 &`
fi


