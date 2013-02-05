# -*- coding: utf-8 -*-

import os

DEFAULT_VHOST_DIRECTORY_OPTIONS = \
"""    Options All
        AllowOverride All"""

DEFAULT_VHOST_IP = "192.168.2.111"

DEFAULT_USER_SHELL = "/sbin/nologin"

DEFAULT_GROUP_NAME = "apache"

DEFAULT_GROUP_ID = 48

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DEFAULT_OUTPUT_DIR = ROOT_PATH + r"\output"
