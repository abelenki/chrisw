#!/usr/bin/env python
# encoding: utf-8
"""
thing_annotation.py

Created by Kang Zhang on 2011-04-19.
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

class _ThingAnnotationUI(ModelUI):
  """docstring for _ThingAnnotationUI"""
  def __init__(self, annotation):
    super(_ThingAnnotationUI, self).__init__(annotation)
    self.annotation = annotation
    self.user = get_current_user()
  
  @check_permission('dig', _("User can't dig this annotation"))
  def up(self):
    self.annotation.up(self.user)
    return back(self.annotation.url)
  
  @check_permission('dig', _("User can't dig this annotation"))
  def down(self):
    self.annotation.down(self.user)
    return back(self.annotation.url)    
  
class ThingCommentUI(_ThingAnnotationUI):
  """docstring for ThingCommentUI"""
  def __init__(self, comment):
    super(ThingCommentUI, self).__init__(comment)
    self.comment = comment
  
  @check_permission('remove', _("User can't remove this annotation"))
  def remove(self):
    self.thing.remove_comment(self)
    return back()
  

class ThingReviewUI(_ThingAnnotationUI):
  """docstring for ThingReviewUI"""
  def __init__(self, review):
    super(ThingReviewUI, self).__init__(review)
    self.review = review
  
  @check_permission('remove', _("User can't remove this review"))
  def remove(self):
    self.thing.remove_review(self)
    return back()
    

class ThingCommentHandler(handlers.RequestHandler):
  """docstring for ThingCommentHandler"""
  def get(self, comment_id):
    """docstring for get"""
    comment_ui = ThingCommentUI(ThingComment.get_by_id(int(comment_id)))
    return self.get_impl(comment_ui)

class ThingReviewHandler(handlers.RequestHandler):
  """docstring for ThingCommentHandler"""
  def get(self, review_id):
    """docstring for get"""
    review_ui = ThingReviewUI(ThingReview.get_by_id(int(review_id)))
    return self.get_impl(review_ui)

class ThingCommentUpHandler(ThingCommentHandler):
  def get_impl(self, comment_ui):
    return comment_ui.up()

class ThingCommentDownHandler(ThingCommentHandler):
  def get_impl(self, comment_ui):
    return comment_ui.down()

class ThingCommentRemoveHandler(ThingCommentHandler):
  def get_impl(self, comment_ui):
    return comment_ui.remove()


class ThingReviewUpHandler(ThingReviewHandler):
  def get_impl(self, review_ui):
    return review_ui.up()

class ThingReviewDownHandler(ThingReviewHandler):
  def get_impl(self, review_ui):
    return review_ui.down()

class ThingReviewRemoveHandler(ThingReviewHandler):
  def get_impl(self, review_ui):
    return review_ui.remove()


apps = [(r'/c/comment/(\d+)/up', ThingCommentUpHandler),
        (r'/c/comment/(\d+)/down', ThingCommentDownHandler),
        (r'/c/comment/(\d+)/remove', ThingCommentRemoveHandler),
        (r'/c/review/(\d+)/up', ThingReviewUpHandler),
        (r'/c/review/(\d+)/down', ThingReviewDownHandler),
        (r'/c/review/(\d+)/remove', ThingReviewRemoveHandler)]

    
    
    
