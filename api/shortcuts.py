#!/usr/bin/env python
# encoding: utf-8
"""
shortcuts.py

Created by Kang Zhang on 2010-09-27.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import sys
import os, logging

from django.template import loader

def render_to_string(*args, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    logging.debug(" args " + str(args))
    return loader.render_to_string(*args, **kwargs)

