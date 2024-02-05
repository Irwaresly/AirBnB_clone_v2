#!/usr/bin/python3
'''
fabric script to distribute an archive to web servers
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run


env.hosts = ['100.26.159.155',  '100.26.122.170']


def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    Returns:
        True if deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    # Extracting relevant information from the archive_path
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)

    try:
        print("Deploying {} to servers".format(file_name))
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        return True
    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False


def pack_web_static():
    """Packs web_static into a .tgz archive.
    Returns:
        The path to the created archive, or None if packing fails.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = os.path.join("versions", "web_static_{}{:02d}{:02d}{:02d}{:02d}{:02d}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    ))
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archive_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archive_size))
        return output
    except Exception as e:
        print("Packing failed: {}".format(str(e)))
        return None


# Usage example:
# archive_path = pack_web_static()
# if archive_path:
#     do_deploy(archive_path)

