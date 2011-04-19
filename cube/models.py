#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""


import logging

from chrisw import db, gdb
from chrisw.core.memcache import cache_result

from common.auth import get_current_user, User, Guest
from conf import settings

OWNER = 'has-thing-owner'
WANTING_ONE = 'has-thing-wanting-one'
RANK = 'has-been-thing-rank-by'
DIG = 'has-been-thing-comment-dig-by'


class ThingSite(db.Model):
  """docstring for ThingSite"""
  avaliable_slots = db.IntegerProperty(default=0)

  def can_create_thing(self, user):
    """docstring for can_create_thing"""
    return self.avaliable_slots > -10

  def create_thing(self, thing, user):
    """docstring for create_thing"""
    thing.creator = user
    thing.put()
    
    self.avaliable_slots -= 1
    self.put()


  @classmethod
  @cache_result('%s-site', 240)
  def get_instance(cls):
    """docstring for get_instance"""
    instance = super(ThingSite, cls).all().get()
    if not instance:
      instance = cls()
      instance.put()

    return instance


class Thing(gdb.Entity):
  """docstring for Thing"""
  creator = db.ReferenceProperty(User)

  title = db.StringProperty(required=True)

  introduction = db.StringProperty(required=True)

  photo_url = db.StringProperty(required=True, default=settings.DEFAULT_THING_PHOTO)

  source_url = db.StringProperty()

  tags = db.StringListProperty(default=[])
  
  extra_fields = db.ListFlyProperty(default=[])
  
  index_fields = ['title']
  keyword_index = db.StringListProperty(required=True, default=[])

  # rank properties
  rank = db.FloatProperty(required=True, default=0.0)
  rank_counts = db.ListFlyProperty(default=[0] * 6)
  rank_rates = db.ListFlyProperty(default=[0.0] * 6)
  rank_count_sum = db.IntegerFlyProperty(default=0)

  owner_count = db.IntegerFlyProperty(default=0)
  wanting_one_count = db.IntegerFlyProperty(default=0)
  comment_count = db.IntegerFlyProperty(default=0)
  review_count = db.IntegerFlyProperty(default=0)
  
  url_format = r"/c/%(url_prefix)s/%(tid)s"
  
  def can_view(self, user):
    """docstring for can_view"""
    return True
  
  ######
  #
  # Own related functions
  #
  ######
  
  def can_own(self, user):
    """docstring for can_own"""
    return user.is_not_guest() and not self.has_owner(user)

  def has_owner(self, user):
    """docstring for has_owner"""
    return self.has_link(OWNER, user)

  def add_owner(self, user):
    """docstring for add_owner"""
    self.link(OWNER, user)
    self._update_owner_count()
      
  def can_cancel_own(self, user):
    """docstring for can_cancel_own"""
    return self.has_owner(user)

  def remove_owner(self, user):
    """docstring for remove_owner"""
    self.unlink(OWNER, user)
    self._update_owner_count()

  def _update_owner_count(self):
    """docstring for update_owner_count"""
    self.owner_count = self.get_targets(OWNER, User).count()
    self.put()

  ######
  #
  # Want related functions
  #
  ######

  def can_want(self, user):
    """docstring for can_want"""
    return user.is_not_guest() and not self.has_wanting_one(user) and not \
      self.has_owner(user)

  def has_wanting_one(self, user):
    """docstring for has_wantor"""
    return self.has_link(WANTING_ONE, user)

  def add_wanting_one(self, user):
    """docstring for add_wanting_one"""
    self.link(WANTING_ONE, user)
    self._update_wanting_one_count()
  
  def can_cancel_want(self, user):
    """docstring for can_cancel_want"""
    return user.is_not_guest() and not self.has_owner(user) \
      and self.has_wanting_one(user)

  def remove_wanting_one(self, user):
    """docstring for remove_wanting_one"""
    self.unlink(WANTING_ONE, user)
    self._update_wanting_one_count()

  def _update_wanting_one_count(self):
    """docstring for update_wanting_one_count"""
    self.wanting_one_count = self.get_targets(WANTING_ONE, User).count()
    self.put()
    

  def _add_annotaion(self, user, annotation):
    """docstring for _add_annotaion"""
    annotation.author = user
    annotation.thing = self
    annotation.thing_type = self.get_type_name()
    annotation.put()
    
  ######
  #
  # comment related functions
  #
  ######

  def can_add_comment(self, user):
    """docstring for can_comment"""
    return user.is_not_guest() and not self.has_comment_by(user)

  def has_comment_by(self, user):
    """docstring for has_comment_by"""
    return self.get_comment(user) is not None

  def get_comment(self, user):
    """docstring for get_comment_by"""
    return self.comments.filter('author', user).get()

  def add_comment(self, user, comment):
    """docstring for add_comment"""
    self._add_annotaion(user, comment)

    self._update_comment_count()

  def _update_comment_count(self):
    """docstring for update_comment_count"""
    self.comment_count = self.comments.count()

  def remove_comment(self, comment):
    """docstring for remove_comment"""
    comment.delete()

    self._update_comment_count()
  
  ######
  #
  # review related functions
  #
  ######
  
  def can_add_review(self, user):
    """docstring for can_add_review"""
    return user.is_not_guest()
  
  def add_review(self, user, review):
    """docstring for add_review"""
    self._add_annotaion(user, review):
    
    self._update_review_count()
  
  def _update_review_count(self):
    """docstring for _update_review_count"""
    self.review_count = self.reviews.count()
  
  def remove_review(self, review):
    """docstring for remove_review"""
    review.delete()
    
    self._update_review_count()
  
  ######
  #
  # rank related functions
  #
  ######
    
  def can_rank(self, user):
    """docstring for can_rank"""
    return user.is_not_guest() and not self.get_rank(user) is None
  
  def get_rank(self, user):
    """docstring for get_rank"""
    return self.get_link_attr(RANK, user)
  
  def add_rank(self, user, rank):
    """docstring for add_rank"""
    if int(rank) in range(1, 6):
      self.link(RANK, user, link_attr=rank)
      self.update_rank_info()
    else:
      raise Exception("Rank must between 1 to 5")

  def update_rank_info(self):
    """docstring for update_rank_info"""
    self.rank = 0.0
    self.rank_count_sum = 0

    for i in range(1, 6):
      rank_count = self.get_targets(RANK, User, link_attr=str(i)).count()
      self.rank_counts[i] = rank_count
      self.rank += rank_count * 1.0 * i
      self.rank_count_sum += rank_count

    self.rank = self.rank / self.rank_count_sum
    
    for i in range(1, 6):
      self.rank_rates[i] = self.rank_counts[i] * 1.0 / self.rank_count_sum

    self.put()

  @property
  def rank_info(self):
    """docstring for rank_info"""
    rank = self.rank
    rank_count_sum = self.rank_count_sum
    ranks = zip(range(1, 6), self.rank_counts[1:])
    rates = zip(range(1, 6), self.rank_rates[1:])
    return locals()

  def update_keyword_index(self):
    """docstring for update_keyword_index"""
    pass

  def get_type_name(self):
    """docstring for get_type_name"""
    return self.__class__.get_cls_type_name()
    
  @property
  def type_name(self):
    return self.get_type_name()
  
  @property
  def url(self):
    url_prefix = self.get_type_name().lower()
    tid = self.key().id()
    
    return self.url_format % locals()

  @classmethod
  def get_cls_type_name(cls):
    """docstring for get_cls_type_name"""
    return cls.__name__


class _ThingAnnotation(gdb.Entity):
  """docstring for ThingComment"""
  author = db.ReferenceProperty(User)
  content = db.TextProperty(required=True)
  
  thing_type = db.StringProperty()
  
  score = db.FloatProperty()

  ups = db.IntegerFlyProperty(default=0)
  downs = db.IntegerFlyProperty(default=0)
  
  url_format = r"/c/annotation/%(annotation_id)s"

  def can_dig(self, user):
    """docstring for can_dig"""
    return user.is_not_guest() and not self.has_digged_by(user)

  def has_digged_by(self, user):
    """docstring for has_digged"""
    return self.has_link(DIG, user)

  def up(self, user):
    """docstring for up"""
    self.link(DIG, user, link_attr=str(1))
    self.update_digs()

  def down(self, user):
    """docstring for down"""
    self.link(DIG, user, link_attr=str(-1))
    self.update_digs()

  def update_digs(self):
    """docstring for update_digs"""
    self.ups = self.get_targets(DIG, User, link_attr=str(1)).count()
    self.downs = self.get_targets(DIG, User, link_attr=str(-1)).count()
    
    self.score = self.ups * 1.0

    self.put()
  
  
  def can_remove(self, user):
    """docstring for can_remove"""
    return self.has_author(user)
  
  def has_author(self, user):
    """docstring for has_author"""
    return self.author.key() == user.key()
  
  
  @property
  def url(self):
    """docstring for url"""
    annotation_id = self.key().id()
    return self.url_format % annotation_id
    

class ThingComment(_ThingAnnotation):
  """docstring for ThingComment"""
  thing = db.ReferenceProperty(Thing, collection_name='comments')
  
  url_format = r"/c/comment/%(annotation_id)s"


class ThingReview(_ThingAnnotation):
  """docstring for ThingReview"""
  title = db.StringProperty(required=True)
  thing = db.ReferenceProperty(Thing, collection_name='reviews')
  
  url_format = r"/c/review/%(annotation_id)s"
    

