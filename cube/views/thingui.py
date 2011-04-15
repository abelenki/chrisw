#!/usr/bin/env python
# encoding: utf-8
"""
thingui.py

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

from cube.models import ThingComment

class ThingForm(djangoforms.ModelForm):
  """docstring for ThingForm"""
  pass

class ThingCommentForm(djangoforms.ModelForm):
  """docstring for ThingCommentForm"""
  class Meta:
    model = ThingComment
    fields = content

  content = fields.fields.CharField(label = _("Short comment"), min_length=10,\
      max_length=140)

class ThingUI(ModelUI):
  """docstring for ThingUI"""

  thing_meta = None

  def __init__(self, thing):
    super(ThingUI, self).__init__(thing)
    self.thing = thing
    self.user = get_current_user()

  @check_permission('view', _('User is not allowed to view this item.'))
  def view(self):
    """docstring for view"""
    current_item = self.thing

  @check_permission('edit', _("User is not allowed to edit this item."))
  def edit(self):
    """docstring for edit"""
    pass

  @check_permission('edit', _("User is not allowed to edit this item."))
  def edit_post(self):
    """docstring for edit_post"""
    pass

  @check_permission('want', _('User are not allowed to want this item.'))
  def want(self):
    """docstring for want"""
    self.thing.add_wanting_one(self.user)
    return back()

  @check_permission('own', _("User can't own this item."))
  def own(self):
    """docstring for own"""
    self.thing.add_owner(self.user)
    return back()

  @check_permission('rank', _("User can't rank this item"))
  def rank(self, request):
    """docstring for rank"""
    rank_value = request.get('rank_value')
    if rank_value:
      self.thing.add_rank(self.user, rank_value)

    return back()

  @check_permission('comment', _("User can't comment this item."))
  def comment(self, request):
    """docstring for comment_post"""
    form = ThingCommentForm(data=request.POST)
    if form.is_valid():
      new_comment = form.save(commit=False)
      self.thing.add_comment(self.user, commit)

      return back()

    # site message here
    return back()


t


