# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Methods for connecting to Shotgun
"""

from __future__ import with_statement

import urllib.parse

from ...log import LogManager

log = LogManager.get_logger(__name__)


def __sanitize_url(server_url):
    """
    Parses a URL and makes sure it has a scheme and no extra / and path.

    ..note:: Calling this method only once might yield incorrect result. Always call
        the sanitize_url function instead.

    :param str server_url: URL to clean up.

    :returns: The cleaned up URL.
    """

    # The given url https://192.168.1.250:30/path?a=b is parsed such that
    # scheme => https
    # netloc => 192.168.1.250:30
    # path = /path
    # query = a=b

    # As such, when sanitizing a url, we want to keep only the scheme and
    # network location

    # Then break up the url into chunks
    tokens_parsed = urllib.parse.urlparse(server_url)

    # Then extract the good parts from the url
    clean_url_tokens = urllib.parse.ParseResult(
        # We want https when there is no specified scheme.
        scheme=tokens_parsed.scheme or "https",
        # If only a host has been provided, path will be set.
        # If a scheme was set, then use the netloc
        netloc=tokens_parsed.netloc or tokens_parsed.path,
        path="",
        params="",
        query="",
        fragment="",
    )

    return urllib.parse.urlunparse(clean_url_tokens)


def sanitize_url(server_url):
    """
    Cleans up a url to that only scheme, host and optional port number remains.

    For example::
        host.com => https://host.com
        host.com:8080 => https://host.com:8080
        https://host.com => https://host.com
        http://host.com => http://host.com
        https://host.com/ => https://host.com
        https://host.com/path => https://host.com

    :returns: The cleaned up URL.
    """

    # FIXME: Python 2.6.x has difficulty parsing a URL that doesn't start with a scheme when there
    # is already a port number. Python 2.7 doesn't have this issue. Ignore this bug for now since it
    # is very unlikely Shotgun will be running off a custom port.
    first_pass = __sanitize_url(server_url.strip())
    # We have to do two passes here. The reason is that if you use a slash in your URL but provide
    # no scheme, the urlparse/unparse calls will recreate the URL as is. Fortunately, when the
    # scheme is missing we're adding in https://. At that point the url is not ambiguous anymore for
    # urlparse/urlparse and it can split the url correctly into
    # - https (scheme)
    # - test.shogunstudio.com (network location)
    # - /... (path)
    #
    # We also lowercase the entire url. This will allow us to reliably compare site addresses
    # against each other elsewhere in the code and not have to worry about STUDIO.shotgunstudio.com
    # and studio.shotgunstudio.com not matching when they should be considered the same site.
    return __sanitize_url(first_pass).lower()
