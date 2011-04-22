#!/usr/bin/env python
# encoding: utf-8
"""
books.py

Created by Kang Zhang on 2011-04-12.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db

from cube.core import ThingMeta
from cube.models import Thing, ThingSite

__all__ = ['apps']



class Book(Thing):
  """docstring for Book"""
  isbn = db.StringProperty()
  
  def fields(self):
    """docstring for fields"""
    return super(Book, self).fields() + [("isbn", self.isbn)]

class BookSite(ThingSite):
  """docstring for BookSite"""
  pass

class BookMeta(ThingMeta):
  """docstring for BookMeta"""
  class_prefix = "Book"
  url_prefix = 'book'
  
  title = 'Book'
  
  _thing_class = Book
  _thing_site_class = BookSite
  
meta = BookMeta()

apps = meta.apps
    