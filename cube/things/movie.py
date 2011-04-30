#!/usr/bin/env python
# encoding: utf-8
"""
movies.py

Created by Kang Zhang on 2011-04-30.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw import db

from chrisw.i18n import _

from cube.core import ThingMeta
from cube.models import Thing, ThingSite

__all__ = ['apps']



class Movie(Thing):
  """docstring for Movie"""
  director = db.StringProperty()
  editor = db.StringProperty()
  movie_type = db.StringProperty()
  company = db.StringProperty()
  release_at = db.DateTimeProperty()
  actors = db.StringProperty()
  country = db.StringProperty()
  
  def fields(self):
    """docstring for fields"""
    return super(Movie, self).fields() + [(_("Actors"), self.actors),
      (_("Director"), self.director), (_("Company"), self.company),
      (_("Editor"), self.editor),
      (_("Release at"), self.release_at), (_("Movie Type"), self.movie_type),
      ]

class MovieSite(ThingSite):
  """docstring for MovieSite"""
  title = _("Daoshicha Movie")

class MovieMeta(ThingMeta):
  """docstring for MovieMeta"""
  class_prefix = "Movie"
  url_prefix = 'movie'
  
  title = 'Movie'
  
  _thing_class = Movie
  _thing_site_class = MovieSite
  
meta = MovieMeta()

apps = meta.apps
