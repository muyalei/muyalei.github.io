#!/usr/bin/env bash

USAGE="Usage: ./startup.sh [dohko|www]"

if [ "$#" -ne 1 ];then
echo $USAGE
exit 1
fi

if [[ "$1" != "dohko" && "$1" != "www" ]];then
echo $USAGE
exit 2
fi

settings_dir=$(dirname $0)/dianping

if [ "$1" = "dohko" ];then
cat $settings_dir/config_dohko >$settings_dir/config.py

else
cat $settings_dir/config_www >$settings_dir/config.py
fi

python manage.py runserver 0:8000
