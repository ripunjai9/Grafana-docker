#!/bin/bash


if ! test $UID -eq 0
then
    echo "Only root Can execute this" 1>&2
    exit 1
fi

DIR=/var/www/grafana-flask-service/saved_xls/

if test -d $DIR
then
    find $DIR  -type f -mmin +60 | xargs -i rm -f {}
fi

DIR=/var/www/grafana-flask-service/reports/saved_reports/

if test -d $DIR
then
    find $DIR  -type f -mmin +60 | xargs -i rm -f {}
fi