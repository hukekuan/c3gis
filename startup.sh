#!/bin/bash

source ../../envs/c3gis_py3/bin/activate

portnum=`lsof -i:5000| awk 'NR > 1' | wc -l`

if [ $portnum -gt 0 ]
then
kill -s 9 `sudo lsof -i:5000| awk 'NR > 1 {print $2}'`
fi

gunicorn -k gevent -c ./gun.conf app:app
