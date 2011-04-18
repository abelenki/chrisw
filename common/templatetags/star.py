#!/usr/bin/env python
# encoding: utf-8
"""
star.py

Created by Kang Zhang on 2011-04-18.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from django import template

from chrisw.i18n import _
from chrisw.helper.django_helper import render_to_string

register = template.Library()

_star_html_template = """<div class="star_bar">
  <div style="width:%(star_value)s%%"></div>
</div>"""

class StarRenderNode(template.Node):
  """docstring for StreamRenderNode"""
  def __init__(self, star_value_name, full_star_number, in_portion):
    super(StarRenderNode, self).__init__()
    self.full_star_number = full_star_number
    self.in_portion = in_portion
    self.star_value_name = star_value_name
  
  def render(self, context):
    """docstring for render"""
    
    star_value = context[self.star_value_name]
    
    if not self.in_portion:
      star_value = int(star_value) * 1.0 / self.full_star_number
    else:
      star_value = float(star_value)
      
    star_value = int(star_value * 100)
    
    return _star_html_template % locals()
    
@register.tag
def star(parser, token):
  items = token.split_contents()
  
  if len(items) < 2:
    raise template.TemplateSyntaxError("%r tag takes at least 2 arguments" % \
      items[0])
  
  star_value_name = items[1]
  args = {}
  
  iterator = items[2:].__iter__()
  
  full_star_number = 5
  in_portion = False
  
  try:
    while True:
      symbol = iterator.next()
      
      if symbol == 'portion':
        in_portion = True
      if symbol == 'of':
        full_star_number = int(iterator.next())
  except StopIteration:
    pass
  
  args["full_star_number"] = full_star_number
  
  return StarRenderNode(star_value_name, full_star_number, in_portion)