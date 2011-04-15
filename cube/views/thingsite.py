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
    pass

  def view_tags(self):
    """docstring for view_tags"""
    pass

  def search(self, request):
    """docstring for search"""
    pass

  def search_post(self, request):
    """docstring for search_post"""
    pass

  def create(self):
    """docstring for create"""
    pass


class ThingSiteHandler(handlers.RequestHandler):
  """docstring for ThingSiteHandler"""

  thing_meta = None

  def get(self):
    """docstring for get"""
    thing_site = thing_meta.thing_site_class.get_instance()
    thing_site_ui = ThingSiteUI(thing_site)

    return self.get_impl(thing_site_ui)

  def post(self):
    """docstring for post"""

    thing_site = thing_meta.thing_site_class.get_instance()
    thing_site_ui = ThingSiteUI(thing_site)

    return self.post_impl(thing_site_ui)