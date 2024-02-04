#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from datetime import datetime
from fabric.api import local
from os import makedirs

def do_pack():
    """Generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        makedirs("versions", exist_ok=True)
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        print("web_static packed: {}".format(file_name))
        return file_name
    except Exception as e:
        print("Error:", e)
        return None

# Uncomment the line below for testing the function
# do_pack()

