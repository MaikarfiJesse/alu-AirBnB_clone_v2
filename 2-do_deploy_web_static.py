#!/usr/bin/python3
from fabric.api import *
from os.path import exists
from datetime import datetime

env.hosts = ['18.232.150.46', '18.208.140.214']


def do_pack():
    try:
        if not os.path.exists("versions"):
            local("mkdir versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        filename = archive_path.split("/")[-1].split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(filename))
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}\
            /".format(filename, filename))
        run("rm /tmp/{}.tgz".format(filename))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(filename, filename))
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ \
            /data/web_static/current".format(filename))
        run("echo '<html><head></head><body>0-index.html</body></html>' > /data/web_static/releases/{}/index.html".format(filename))
        return True

    except:
        return False
