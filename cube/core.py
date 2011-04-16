#!/usr/bin/env python
# encoding: utf-8
"""
core.py

The ThingConfig

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


_all_thing_metas = []

class _ThingMetaMeta(type):
  """docstring for _ThingMetaMeta"""
  def __new__(cls, name, bases, attrs):

    new_thing_meta = super(_ThingMetaMeta, cls).new(name, bases, attrs)
    return new_thing_meta

class ThingMeta(object):
  """docstring for ThingConfig"""
  __metaclass__ = _ThingMetaMeta

  class_prefix = 'Thing'

  url = 'thing'
  title = 'Thing'

  _thing_class = None
  _thing_ui_class = None
  _thing_form_class = None

  _thing_site_class = None
  _thing_site_ui_class = None

  @property
  def thing_class(self):
    """docstring for thing_class"""
    pass

  @property
  def thing_form_class(self):
    """docstring for thing_form_class"""
    pass

  @property
  def thing_ui_class(self):
    """docstring for thing_ui_class"""
    pass

  @property
  def thing_site_class(self):
    """docstring for thing_site_model"""
    pass

  @property
  def thing_site_ui_class(self):
    """docstring for thing_site_ui_class"""
    pass

  def url_bindings(self):
    """docstring for url_bindings"""
    pass
