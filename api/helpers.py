#!/usr/bin/env python
# encoding: utf-8
"""
helpers.py

Created by Kang Zhang on 2010-10-01.
Copyright (c) 2010 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

def inspect_permissions(model_obj, user):
  """Inspect the model object to get possible permissions
  
  The model's permission method neeeds start with "can_", while it contains
  and only contains two arguments ['self', 'user']:
  Example:
  
  class StoreModel(db.Model):
    def can_edit(self, user):
      return True
  
  """
  out = {}
  
  import inspect
  logging.debug(" %s ", str(model_obj))
  for name, member in inspect.getmembers(model_obj):
    # logging.debug(" Member %s : %s ", str(name), str(member))
    if inspect.ismethod(member) and name[:4] == 'can_':
      # keep compitable with python 2.5
      args, varargs, keywords, defaults = inspect.getargspec(member)
      if args == ['self', 'user']:
        out[name] = member(user)
  
  return out


