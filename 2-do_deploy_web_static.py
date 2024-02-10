#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists
env.hosts = ['100.26.159.155', '100.26.122.170']

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the folder /data/web_static/releases/<archive filename without extension>
        archive_filename = archive_path.split('/')[-1]
        release_path = '/data/web_static/releases/{}'.format(archive_filename[:-4])
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted folder to the proper location
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the now-empty web_static folder
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")

        return True

    except Exception as e:
        print(e)
        return False

