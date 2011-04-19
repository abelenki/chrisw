#!/usr/bin/env python
# encoding: utf-8
"""
exceptions.py

Created by Kang Zhang on 2011-02-15.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

__all__ = ['CannotResolvePath', 'PermissionException', 'APIError', 'UnknownActionException']

class ChriswException(Exception):
  pass

class CannotResolvePath(ChriswException):
  """docstring for CannotResolvePath"""
  pass

class PermissionException(ChriswException):
  """docstring for PermissionError"""
  def __init__(self, msg, user, obj):
    super(PermissionException, self).__init__(msg)
    self.user = user
    self.obj = obj
    self.msg = msg

class APIError(ChriswException):
  def __init__(self, reason):
    super(APIError, self).__init__(reason)
    self.reason = reason

class UnknownActionException(ChriswException):
  def __init__(self, action):
    super(UnknownActionException, self).__init__(str(action))
    self.reason = "Can't recognized Action: " + str(action)
