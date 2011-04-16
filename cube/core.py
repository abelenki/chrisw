#!/usr/bin/env python
# encoding: utf-8
"""
core.py

The ThingConfig

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

__all__ = ['ThingMeta']

_all_thing_metas = []

class _ThingMetaMeta(type):
  """docstring for _ThingMetaMeta"""
  def __new__(cls, name, bases, attrs):

    new_thing_meta = super(_ThingMetaMeta, cls).new(name, bases, attrs)
    global _all_thing_metas
    _all_thing_metas[name] = new_thing_meta

    return new_thing_meta

def lazy_property(func):
  """docstring for lazy_property"""
  attr_name = func.__name__

  def wrapper(self):
    """docstring for wrapper"""
    lazy_attr_name = '_' + attr_name

    value = hasattr(self, lazy_attr_name) and getattr(self, lazy_attr_name)

    if not value:
      init_func = getattr(self, '_init_' + attr_name)
      value = init_func()
      setattr(self, lazy_attr_name, value)

    return value

  return wrapper

class ThingMeta(object):
  """docstring for ThingConfig"""
  __metaclass__ = _ThingMetaMeta

  class_prefix = 'Thing'
  url_prefix = 'thing'

  title = 'Thing'

  _thing_class = None
  _thing_form_class = None
  _thing_ui_class = None
  _thing_handler_class = None

  _thing_site_class = None
  _thing_site_ui_class = None
  _thing_site_handler_class = None

  def _init_thing_class(self):
    pass

  @property
  @lazy_property
  def thing_class(self):
    """Return the class for the thing"""
    pass

  def _init_thing_form_class(self):
    pass


  @property
  @lazy_property
  def thing_form_class(self):
    """docstring for thing_form_class"""
    pass

  def _init_thing_ui_class(self):
    pass

  @property
  @lazy_property
  def thing_ui_class(self):
    """docstring for thing_ui_class"""
    pass


  def _init_thing_handler_class(self):
    """docstring for _init_thing_handler_class"""
    pass

  @property
  @lazy_property
  def thing_handler_class(self):
    """docstring for thing_handler_class"""
    pass


  def _init_thing_site_class(self):
    pass

  @property
  @lazy_property
  def thing_site_class(self):
    """docstring for thing_site_model"""
    pass


  def _init_thing_site_ui_class(self):
    pass

  @property
  @lazy_property
  def thing_site_ui_class(self):
    """docstring for thing_site_ui_class"""
    pass


  def _init_thing_site_handler_class(self):
    """docstring for _init_thing_site_handler_class"""
    pass

  @property
  @lazy_property
  def thing_site_handler_class(self):
    """docstring for thing_site_handler_class"""
    pass

  @property
  @lazy_property
  def apps(self):
    """docstring for url_bindings"""
    apps = []

    # init thing apps
    from views.thingui import abstract_apps as thing_apps

    for (url_parttern, handler_class) in thing_apps:
      url = url_parttern % {'thing_url':self.url_prefix}

      new_handler_class_name = handler_class.__name__.replace('Thing',\
        self.class_prefix)

      new_handler_class = type(new_handler_class_name, \
        (self.thing_handler_class, handler_class), {})

      apps.append((url, new_handler_class))

    # init thing site apps
    from views.thingsite import abstract_apps as thingsite_apps:

    for (url_parttern, handler_class) in thingsite_apps:
      url = url_parttern % {'thing_url':self.url_prefix}

      new_handler_class_name = handler_class.__name__.replace('Thing',\
        self.class_prefix)

      new_handler_class = type(new_handler_class_name, \
        (self.thing_site_handler_class, handler_class), {})

      apps.append(url, new_handler_class)

    return apps