#!/usr/bin/python3
from fabric.api import *

env.user = 'ubuntu'
env.hosts = ['18.232.150.46', '18.208.140.214']
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    # Check if archive exists
    if not os.path.exists(archive_path):
        return False

    # Get the filename of the archive
    filename = os.path.basename(archive_path)
    # Get the name of the file without extension
    name = os.path.splitext(filename)[0]

    try:
        # Upload the archive to /tmp/ directory of web server
        put(archive_path, '/tmp/')

        # Create the directory to uncompress the archive
        run('mkdir -p /data/web_static/releases/{}/'.format(name))

        # Uncompress the archive to the directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, name))

        # Delete the archive from web server
        run('rm /tmp/{}'.format(filename))

        # Move files to the web root
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(name, name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(name))

        # Delete the old symbolic link
        run('rm -f /data/web_static/current')

        # Create a new symbolic link to the new version of your code
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(name))

        print("New version deployed!")
        return True
    except:
        return False
