#!/usr/bin/env python
# encoding: utf-8
"""
Page.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

_url_format = "%(path)s?offset=%(offset)s&limit=%(limit)s"

class Page(object):
  """docstring for Paginator"""
  def __init__(self, request, query, limit=15):
    super(Page, self).__init__()
    self.request = request
    self.query = query
    self.path = request.path
    
    self.offset = int(request.get('offset', 0))
    self.limit = int(request.get('limit', limit))
    
    self.count = self.query.count()
  
  def data(self):
    """docstring for data"""
    return self.query.fetch(limit=self.limit, offset=self.offset)
  
  def has_next(self):
    """docstring for has_next"""
    return self.limit < self.count
  
  def has_prev(self):
    """docstring for has_previous"""
    return self.offset != 0
    
  def next_url(self):
    """docstring for next_url"""
    path, offset, limit = self.path, self.offset + self.limit, self.limit
    return _url_format % locals()
      
  def prev_url(self):
    """docstring for prev_url"""
    path, offset, limit = self.path, self.offset - self.limit, self.limit
    return _url_format % locals()
      
  def url(self):
    """docstring for url"""
    path, offset, limit = self.path, self.offset, self.limit
    return _url_format % locals()