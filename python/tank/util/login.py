# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Helper methods that extracts information about the current user.

"""

import os
from .platforms import is_windows


def get_login_name():
    """
    Retrieves the login name of the current user.
    Returns None if no login name was found
    """
    if is_windows():
        # http://stackoverflow.com/questions/117014/how-to-retrieve-name-of-current-windows-user-ad-or-local-using-python
        return os.environ.get("USERNAME", None)
    else:
        try:
            import pwd

            pwd_entry = pwd.getpwuid(os.geteuid())
            return pwd_entry[0]
        except:
            return None


# note! Because the shotgun caching method can return None, to indicate that no
# user was found, we cannot use a None value to indicate that the cache has not been
# populated.
g_shotgun_user_cache = "unknown"
g_shotgun_current_user_cache = "unknown"


