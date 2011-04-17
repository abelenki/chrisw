#!/usr/bin/env python
# encoding: utf-8
"""
thingsite.py

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


from chrisw.core import handlers
from chrisw.core.action import *
from chrisw.core.ui import ModelUI, check_permission
from chrisw.core.memcache import cache_action
from chrisw.i18n import _
from chrisw.helper import Page, djangoforms
from chrisw.helper.django_helper import fields, forms

from common.auth import get_current_user
from common.models import User
from conf import settings


class ThingSiteUI(ModelUI):
  """docstring for ThingSiteUI"""
  
  thing_meta = None
  
  def __init__(self, thing_site):
    super(ThingSiteUI, self).__init__(thing_site)
    self.thing_site = thing_site
    self.user = get_current_user()

  def view_front(self):
    """docstring for view"""
    
    thing_class = self.thing_meta.thing_class
    latest_thing = thing_class.latest()
    
    return template('page_thing_site_view_front.html', locals())

  def view_tags(self):
    """docstring for view_tags"""
    pass

  def search(self, request):
    """docstring for search"""
    return template('page_thing_site_search.html', locals())

  def search_post(self, request):
    """docstring for search_post"""
    pass

  @check_permission('create_thing', _('You are not allowed to create this type of item.'))
  def create(self):
    """docstring for create"""
    form = self.thing_meta.thing_form_class()
    return template('page_thing_site_create.html', locals())
  
  # TODO add dynamic fields for creating form
  def _get_dynamic_fields(self, data):
    """docstring for _get_dynamic_fields"""
    
    line_key_format = "opt_attr[optattr][%s][%s]"
    
    fields = []
    for i in range(0, 10):
      key = data[line_key_format % (i, 'key')]
      value = data[line_key_format % (i, 'value')]
      
      if key and value:
        fields.append(key, value)
        
    return fields

  @check_permission('create_thing', _('You are not allowed to create this type of item.'))
  def create_post(self, request):
    """docstring for create_post"""
    form = self.thing_meta.thing_form_class(data=request.POST)
    
    if form.is_valid():
      new_thing = form.save(commit=False)
      self.thing_site.create_thing(new_thing, self.user)
    
    return template('page_thing_site_create.html', locals())


class ThingSiteHandler(handlers.RequestHandler):
  """docstring for ThingSiteHandler"""

  thing_meta = None

  def get(self):
    """docstring for get"""
    thing_site = self.thing_meta.thing_site_class.get_instance()
    thing_site_ui = self.thing_meta.thing_site_ui_class(thing_site)

    return self.get_impl(thing_site_ui)

  def post(self):
    """docstring for post"""
    thing_site = self.thing_meta.thing_site_class.get_instance()
    thing_site_ui = self.thing_meta.thing_site_ui_class(thing_site)

    return self.post_impl(thing_site_ui)


class ThingSiteViewFrontHandler(handlers.PartialHandler):
  def get_impl(self, thing_site_ui):
    return thing_site_ui.view_front()

class ThingSiteSearchHandler(handlers.PartialHandler):
  def get_impl(self, thing_site_ui):
    return thing_site_ui.search(self.request)

  def post_impl(self, thing_site_ui):
    return thing_site_ui.search_post(self.request)

class ThingSiteCreateHandler(handlers.PartialHandler):
  def get_impl(self, thing_site_ui):
    return thing_site_ui.create()

  def post_impl(self, thing_site_ui):
    return thing_site_ui.create_post(self.request)


abstract_apps = [(r'/c/%(thing_url)s', ThingSiteViewFrontHandler),
                 (r'/c/%(thing_url)s/search', ThingSiteSearchHandler),
                 (r'/c/%(thing_url)s/new', ThingSiteCreateHandler),
                 ]