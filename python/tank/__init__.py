# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

# Toolkit core API version
__version__ = "HEAD"

########################################################################
# Establish pipeline configuration context if needed
#
# When the tank command executes, or when the python API is imported
# via the API proxy that is available with every non-localized pipeline config,
# an environment variable TANK_CURRENT_PC, is set, pointing at the configuration
# associated with the currently running config. This is to ensure that the right
# version of the code is associated with the currently running project
# configuration.
#
# However, in the case when a cloned configuration has been localized,
# the API proxy has been replaced by the actual core API code.
# In this case, we will set the TANK_CURRENT_PC explicitly.
#
# The logic below is fundamentally to avoid the issue that when a cloned localized
# configuration has its python sgtk/tank module imported directly, it will associate
# itself with the primary config rather than with the config where the code is located.

import sys

if sys.version_info < (3, 7):
    raise Exception("This module requires Python version 3.7 or higher.")

########################################################################

# first import the log manager since a lot of modules require this.
from .log import LogManager

