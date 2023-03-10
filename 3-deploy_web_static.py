#!/usr/bin/python3
from fabric.api import *
from os.path import exists
from datetime import datetime

import os

env.hosts = ['18.232.150.46', '18.208.140.214']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """

    try:
        if not os.path.exists("versions"):
            local("mkdir versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


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
        run("mv /data/web_static/current/index.html /data/web_static/current/0-index.html")
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers
    """

    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
