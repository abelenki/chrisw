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
  def __init__(self, thing_site):
    super(ThingSiteUI, self).__init__(thing_site)
    self.thing_site = thing_site

  def view_all(self):
    """docstring for view"""
    return template('page_thing_site_view_all.html', locals())

  def view_tags(self):
    """docstring for view_tags"""
    pass

  def search(self, request):
    """docstring for search"""
    return template('page_thing_site_search.html', locals())

  def search_post(self, request):
    """docstring for search_post"""
    pass

  @check_permission('create', _('You are not allowed to create this type of item.'))
  def create(self):
    """docstring for create"""
    return template('page_thing_site_create.html', locals())

  @check_permission('create', _('You are not allowed to create this type of item.'))
  def create_post(self, request):
    """docstring for create_post"""
    pass


class ThingSiteHandler(handlers.RequestHandler):
  """docstring for ThingSiteHandler"""

  thing_meta = None

  def get(self):
    """docstring for get"""
    thing_site = thing_meta.thing_site_class.get_instance()
    thing_site_ui = thing_meta.thing_site_ui_class(thing_site)

    return self.get_impl(thing_site_ui)

  def post(self):
    """docstring for post"""
    thing_site = thing_meta.thing_site_class.get_instance()
    thing_site_ui = thing_site_ui_class(thing_site)

    return self.post_impl(thing_site_ui)


class ThingSiteViewAllHandler(handlers.PartialHandler):
  """docstring for ThingSiteViewHandler"""
  def get_impl(self, thing_site_ui):
    """docstring for get_impl"""
    return thing_site_ui.view_all()

class ThingSiteSearchHandler(handlers.PartialHandler):
  """docstring for ThingSiteSearchHandler"""
  def get_impl(self, thing_site_ui):
    """docstring for get_impl"""
    return thing_site_ui.search(self.request)

  def post_impl(self, thing_site_ui):
    """docstring for post_impl"""
    return thing_site_ui.search_post(self.request)

class ThingSiteCreateHandler(handlers.PartialHandler):
  """docstring for ThingSiteCreateHandler"""
  def get_impl(self, thing_site_ui):
    """docstring for get_impl"""
    return thing_site_ui.create(self.request)

  def post_impl(self, thing_site_ui):
    """docstring for post_impl"""
    return thing_site_ui.create_post(self.request)


abstract_apps = [(r'/{thing_url}/all', ThingSiteViewHandler),
                 (r'/{thing_url}/search', ThingSiteSearchHandler),
                 (r'/{thing_url}/new', ThingSiteCreateHandler),
                 ]
