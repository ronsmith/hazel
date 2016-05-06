#!/usr/bin/env bash

echo "Installing OS-level packages..."
sudo apt-get update
sudo apt-get install -y build-essential python3-dev python3-setuptools python3-pip libxml2-dev libxslt1-dev
sudo apt-get install -y nginx
sudo apt-get install -y memcached libmemcached-dev

echo "Creat link to project dir in vagrant home..."
cd /home/vagrant
ln -d /vagrant hazel

echo "Setup virtualenv..."
mkdir run
chown vagrant run
mkdir env
chown vagrant env
virtualenv -p python3 env
source env/bin/activate
pip3 install -r /vagrant/src/requirements.txt

#echo "Configuring NGINX and Gunicorn..."
#cp /vagrant/scripts/config/vagrant/nginx.conf /etc/nginx/sites-available
#mv /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-available/mothra
#ln -s /etc/nginx/sites-available/mothra /etc/nginx/sites-enabled/mothra
#rm /etc/nginx/sites-enabled/default
#cp /vagrant/scripts/config/vagrant/gunicorn.conf /etc/init

#echo "Restarting NGINX..."
#service nginx restart

#echo "Starting Gunicorn..."
#start gunicorn
