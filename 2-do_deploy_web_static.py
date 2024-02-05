#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["100.26.159.155", "100.26.122.170"]

def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False

    # Extracting relevant information from the archive_path
    file_name = os.path.basename(archive_path)
    # Using a timestamp for a unique version name
    timestamp = run("date +'%Y%m%d%H%M%S'").stdout.strip()
    name = "web_static_{}".format(timestamp)

    # Remote paths
    remote_tmp_path = "/tmp/{}".format(file_name)
    remote_release_path = "/data/web_static/releases/{}".format(name)

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, remote_tmp_path)

        # Create the release directory
        run("mkdir -p {}".format(remote_release_path))

        # Extract the archive to the release directory
        run("tar -xzf {} -C {}/".format(remote_tmp_path, remote_release_path))

        # Remove the archive from the /tmp/ directory
        run("rm {}".format(remote_tmp_path))

        # Move contents to the correct path
        run("mv {}/web_static/* {}/".format(remote_release_path, remote_release_path))

        # Remove the web_static directory
        run("rm -rf {}/web_static".format(remote_release_path))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(remote_release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(str(e)))
        return False

