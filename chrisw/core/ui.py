#!/usr/bin/env python
# encoding: utf-8
"""
ui.py

Created by Kang Zhang on 2011-02-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

import logging

from common.auth import get_current_user
from chrisw.core.exceptions import *

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


class check_permission(object):
  """ ``check_permission`` decorator: check the permission on the given 
  ``PermissionUI``
  
  Usage:
    @check_permission('follow', _("Can't follow the user"))
    def follow(self):
      self.user_stream_info.follow(self.current_user)
      return back()
   
  """
  def __init__(self, permission, error_msg):
    super(check_permission, self).__init__()
    self.permission = permission
    self.error_msg = error_msg

  def __call__(self, func):
    def wrapper(ui, *args, **kwargs):
      """docstring for wrapper"""
      f = getattr(ui.model_obj, 'can_' + self.permission)
      
      from common.auth import Guest
      
      if f(ui.model_user):
        return func(ui, *args, **kwargs)
      elif ui.model_user == Guest:
        # Guest can't be used to do anything
        return login()
        
      raise PermissionException(self.error_msg, ui.model_user, ui.model_obj)

    return wrapper  



class PermissionUI(object):
  """docstring for PermissionModel"""
  def __init__(self, model_obj):
    super(PermissionUI, self).__init__()
    
    if not model_obj:
      raise APIException("Can't find item. Wrong ID?")
    
    self.model_obj = model_obj
    self.model_user = get_current_user()
    
def view_method(func):
  """the target method is a view method, it returned 
      template_name, var_dict to be used by api_enabled decorator
      it will wrap the instance's fields in to the returned var_dict
  """
  
  def wrapper(self, *args, **kwargs):
    """docstring for wrapper"""
    
    action = func(self, *args, **kwargs)

    # append the instance variable
    if hasattr(action, 'var_dict'):
      var_dict = action.var_dict
      
      # add instance attributes
      var_dict.update(self.__dict__)
      # add class attributes
      var_dict.update(self.__class__.__dict__)
      
      # skip the keys
      for key in ('self', 'model_obj', 'model_user'):
        if var_dict.has_key(key): 
          del var_dict[key]

      # add permission info in vardict
      user = get_current_user()
      var_dict.update( inspect_permissions(self.model_obj, user) )
      
    return action
    
  return wrapper

def not_view_method(func):
  """decorator for methods that do not need to be wrapped.
  """
  func.im_not_view_method = True
  return func

class _ModelUIMeta(type):
  
  def __new__(cls, name, bases, attrs):
    
    for attr, item in attrs.items():
      if attr[0] is not '_' and callable(item) and \
        not hasattr(item, 'im_not_view_method'):
          attrs[attr] = view_method(item)
    
    return super(_ModelUIMeta, cls).__new__(cls, name, bases, attrs)
    

class ModelUI(PermissionUI):
  
  __metaclass__ = _ModelUIMeta
  
