#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by Kang Zhang on 2010-09-29.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import uhome, userui
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
  def get(self):
    # path = os.path.join(os.path.dirname(__file__), '../templates/base.html')
    # self.response.out.write(template.render(path, {'user': 'andyzhau'}))
    from api.shortcuts import render_to_string
    from duser.auth import get_current_user
    self.response.out.write(render_to_string('base.html', {'user': get_current_user()}))

apps = uhome.apps + [('/', MainHandler),]

def create_login_url(url):
  """docstring for create_login_url"""
  import urllib
  back_url = urllib.quote_plus(url)
  return settings.LOGIN_URL + "?back_url=" + back_url

