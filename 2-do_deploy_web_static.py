#!/usr/bin/python3
from fabric.api import *
from os.path import exists
from datetime import datetime
import os

env.hosts = ['18.232.150.46', '18.208.140.214']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False
    
    try:
        # get archive file name without extension
        filename_ext = os.path.basename(archive_path)
        filename = os.path.splitext(filename_ext)[0]

        # create paths
        releases_path = "/data/web_static/releases/{}/".format(filename)
        tmp_path = "/tmp/{}".format(filename_ext)

        # upload archive to the /tmp/ directory of the web server
        put(archive_path, tmp_path)

        # create directory to uncompress archive
        run("mkdir -p {}".format(releases_path))

        # uncompress archive to directory
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))

        # delete archive file from web server
        run("rm {}".format(tmp_path))

        # move files to web root
        run("mv {}web_static/* {}".format(releases_path, releases_path))

        # remove web_static directory
        run("rm -rf {}web_static".format(releases_path))

        # create missing directories
        run("mkdir -p /data/web_static/releases/{}/public".format(filename))
        run("mkdir -p /data/web_static/releases/{}/data".format(filename))

        # create missing index.html file
        run("echo 'Holberton School' | sudo tee /data/web_static/releases/{}/public/index.html".format(filename))

        # delete symbolic link
        run("rm -rf /data/web_static/current")

        # create new symbolic link to new version of code
        run("ln -s {} /data/web_static/current".format(releases_path))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False
