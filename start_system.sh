#!/bin/sh

./restart.sh
sudo service nginx restart
uwsgi --ini devices_mgmt_uwsgi.ini &