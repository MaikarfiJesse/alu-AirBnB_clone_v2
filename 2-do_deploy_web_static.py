#!/usr/bin/python3
from fabric.api import *
from os.path import exists
from datetime import datetime

import os

from fabric.api import *
import shlex
from datetime import datetime


env.hosts = ['18.232.150.46', '18.208.140.214']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """

    if not os.path.exists(archive_path):
        return False
    try:
        name = archive_path.replace('/', ' ')
        name = shlex.split(name)
        name = name[-1]

        wname = name.replace('.', ' ')
        wname = shlex.split(wname)
        wname = wname[0]

        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(releases_path))
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))
        run("rm {}".format(tmp_path))
        run("mv {}web_static/* {}".format(releases_path, releases_path))
        run("rm -rf {}web_static".format(releases_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(releases_path))

        # Add the required file with the correct content
        run("mkdir -p /data/web_static/releases/{}/{}".format(wname, "hbnb_static"))
        run("echo 'Holberton School' | sudo tee /data/web_static/releases/{}/hbnb_static/0-index.html".format(wname))

        print("New version deployed!")
        return True
    except:
        return False
