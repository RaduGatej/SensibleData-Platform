#! /bin/bash

#install packages
apt-get install $(< packages.txt)

#install python modules
pip install -r requirements.txt

#cp example settings
cp sensible_data_platform/sensible_data_platform/EXAMPLE_LOCAL_SETTINGS.py sensible_data_platform/sensible_data_platform/LOCAL_SETTINGS.py

#syncdb
python sensible_data_platform/manage.py syncdb

#run example server
python sensible_data_platform/manage.py runserver $1:$2

