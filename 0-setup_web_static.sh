#!/usr/bin/env bash
# Script to set up Nginx on web servers

# update 
sudo apt-get update
# install Nginx
sudo apt-get -y install nginx
sudo service nginx start
# create folders
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
# create fake HTMl file
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html
# create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# update permissions
chown -R ubuntu:ubuntu /data/
# update Nginx config
sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default
# restart Nginx
service nginx restart
