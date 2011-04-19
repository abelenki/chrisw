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

from cube.models import ThingComment, ThingReview

class ThingForm(djangoforms.ModelForm):
  """docstring for ThingForm"""
  class Meta:
    """docstring for Meta"""
    fields = ['title', 'introduction', 'tags']
  
  title = fields.fields.CharField(label = _("Title"), min_length=2,\
        max_length=20)
  introduction = fields.CharField(label = _("Introductioin"),\
    widget=forms.Textarea, min_length=2, max_length = 200)
  tags = fields.fields.CharField(label = _("Tags (Please seperate tags by comma ',')"),\
  min_length=2, max_length=20)
  

class ThingCommentForm(djangoforms.ModelForm):
  """docstring for ThingCommentForm"""
  class Meta:
    model = ThingComment
    fields = ['content']

  content = fields.fields.CharField(label = _("Short comment"), min_length=10,\
      max_length=140)

class ThingReviewForm(djangoforms.ModelForm):
  """docstring for ThingReviewForm"""
  class Meta:
    model = ThingReview
    fields = ['content', 'title']

  title = fields.fields.CharField(label = _("Title"), min_length=10,\
    max_length=140)
  content = fields.CharField(label = _("Content"),\
    widget=forms.Textarea, min_length=2, max_length = 200)


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

    return template('page_thing_view.html', locals())

  @check_permission('edit', _("User is not allowed to edit this item."))
  def edit(self):
    """docstring for edit"""
    form = self.thing_meta.thing_form_class()
    return template('page_thing_edit.html', locals())

  @check_permission('edit', _("User is not allowed to edit this item."))
  def edit_post(self, request):
    """docstring for edit_post"""
    form = self.thing_meta.thing_form_class(data=request.POST, \
      instance=self.thing)
      
    if form.is_valid():
      instance = form.save(commit=False)
      instance.put()
    
    return template('page_thing_edit.html', locals())

  @check_permission('want', _('User are not allowed to want this item.'))
  def want(self):
    """docstring for want"""
    self.thing.add_wanting_one(self.user)
    return back()
  
  @check_permission('cancel_want', _('User are not allowed to cancel.'))
  def cancel_want(self):
    """docstring for cancel_want"""
    self.thing.remove_wanting_one(self.user)
    return back()

  @check_permission('own', _("User can't own this item."))
  def own(self):
    """docstring for own"""
    self.thing.add_owner(self.user)
    return back()
  
  @check_permission('cancel_own', _("User are not allowed to cancel."))
  def cancel_own(self):
    """docstring for cancel_own"""
    self.thing.remove_owner(self.user)
    return back()

  @check_permission('rank', _("User can't rank this item"))
  def rank(self, request):
    """docstring for rank"""
    rank_value = request.get('rank_value')
    if rank_value:
      self.thing.add_rank(self.user, rank_value)

    return back()

  @check_permission('add_comment', _("User can't comment this item."))
  def comment(self, request):
    """docstring for comment"""
    form = ThingCommentForm()
    post_url = request.path
    return template("page_item_create.html", locals())
  
  @check_permission('add_comment', _("User can't comment this item."))
  def comment_post(self, request):
    """docstring for comment_post"""
    form = ThingCommentForm(data=request.POST)
    if form.is_valid():
      new_comment = form.save(commit=False)
      self.thing.add_comment(self.user, new_comment)

      return back()
    
    post_url = request.path
    # site message here
    return template("page_item_create.html", locals())
  
  def view_comments(self, request):
    """docstring for view_comments"""
    
    # fetch the latest comments
    query = self.thing.comments.order('-create_at') 
    page = Page(query=query, request=request)
    comments = page.data()
    
    return template('page_thing_comment_view.html', locals())
  
  @check_permission('add_review', _("User can't review this item."))
  def review(self, request):
    """docstring for review"""
    form = ThingCommentForm()
    post_url = request.path
    return template("page_item_create.html", locals())
  
  @check_permission('add_review', _("User can't review this item."))
  def review_post(self, request):
    """docstring for review_post"""
    form = ThingReviewForm(data=request.POST)
    if form.is_valid():
      new_review = form.save(commit=False)
      self.thing.add_review(self.user, new_review)

      return back()
    
    post_url = request.path
    # site message here
    return template("page_item_create.html", locals())
  
  def view_reviews(self, request):
    """docstring for view_reviews"""
    # fetch the latest comments
    query = self.thing.reviews.order('-create_at') 
    page = Page(query=query, request=request)
    reviews = page.data()
    
    return template('page_thing_review_view.html', locals())
  

class ThingHandler(handlers.RequestHandler):
  """Here we use a trick to enable 'mixin' feature for Python.
  Consider the following code example:

  >>> class A():
  ...   def foo(self):
  ...     self.bar()

  >>> class B():
  ...   def bar(self):
  ...     print "bar"

  >>> C = type('C', (A, B, object),{})
  >>> C().foo()
  bar

  """

  thing_meta = None

  def get(self, thing_id):
    """docstring for get"""
    thing = self.thing_meta.thing_class.get_by_id(int(thing_id))
    thing_ui = self.thing_meta.thing_ui_class(thing)

    return self.get_impl(thing_ui)

  def post(self, thing_id):
    """docstring for post"""
    thing = self.thing_meta.thing_class.get_by_id(int(thing_id))
    thing_ui = self.thing_meta.thing_ui_class(thing)

    return self.post_impl(thing_ui)

class ThingWantHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.want()

class ThingCancelWantHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.cancel_want()

class ThingOwnHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.own()

class ThingCancelOwnHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.cancel_own()

class ThingRankHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.rank(self.request)

class ThingEditHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.edit()

  def post_impl(self, thingui):
    return thingui.edit(self.request)

class ThingViewHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.view()

class ThingCommentHandler(handlers.PartialHandler):
  def post_impl(self, thingui):
    return thingui.comment_post(self.request)
  
  def get_impl(self, thingui):
    return thingui.comment(self.request)

class ThingCommentsViewHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.view_comments(self.request)

class ThingAddReviewHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.review(self.request)
  
  def post_impl(self, thingui):
    return thingui.review_post(self.request)

class ThingReviewsViewHandler(handlers.PartialHandler):
  def get_impl(self, thingui):
    return thingui.view_reviews(self.request)


abstract_apps = [(r'/c/%(thing_url)s/(\d+)', ThingViewHandler),
                 (r'/c/%(thing_url)s/(\d+)/edit', ThingEditHandler),
                 (r'/c/%(thing_url)s/(\d+)/own', ThingOwnHandler),
                 (r'/c/%(thing_url)s/(\d+)/cancel_own', ThingCancelOwnHandler),
                 (r'/c/%(thing_url)s/(\d+)/want', ThingWantHandler),
                 (r'/c/%(thing_url)s/(\d+)/cancel_want', ThingCancelWantHandler),
                 (r'/c/%(thing_url)s/(\d+)/comments/new', ThingCommentHandler),
                 (r'/c/%(thing_url)s/(\d+)/comments', ThingCommentsViewHandler),
                 (r'/c/%(thing_url)s/(\d+)/reviews/new', ThingAddReviewHandler),
                 (r'/c/%(thing_url)s/(\d+)/reviews', ThingReviewsViewHandler),
                 (r'/c/%(thing_url)s/(\d+)/rank', ThingRankHandler)]

