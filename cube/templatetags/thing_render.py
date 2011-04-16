#!/usr/bin/env python
# encoding: utf-8
"""
thing_render.py

Created by Kang Zhang on 2011-04-16.
Copyright (c) 2011 Shanghai Jiao Tong University. All rights reserved.
"""

from chrisw.i18n import _
from chrisw.helper.django_helper import render_to_string

from home.models import TEXT_STREAM

register = template.Library()

_TEXT = 'text'
_SQUARE = 'square'
_BOX = 'box'

_supported_types = {
  'Book':('',),
}

class ThingRenderNode(template.Node):
  """docstring for StreamRenderNode"""
  def __init__(self, thing_name, render_mode=_TEXT):
    super(UserStreamRenderNode, self).__init__()
    self.thing_name = thing_name
    self.render_mode = render_mode
  
  def render(self, context):
    current_item = context[self.thing_name]
    
    context.update(locals())
    
    if not thing:
      return "Skipped"
      
    template_name_format = "item_%(render_mode)s_%(thing_type)s.html"
    thing_type = 'thing'
    render_mode = self.render_mode
    
    if _supported_types.has_key(thing.type_name) and \
      render_mode in _supported_types[thing.type_name]:
      thing_type = thing.type_name.lower()
    
    template_name = template_name_format % locals()
    
    return render_to_string(template_name, context)
    

@register.tag
def thing_render(parser, token):
  items = token.split_contents()
  
  if len(items) < 2:
    raise template.TemplateSyntaxError("%r tag takes at least 2 arguments" % \
      items[0])
  
  thing_name = items[1]
  args = {}
  
  for item in items[2:]:
    if item.lower() in (_TEXT, _SQUARE, _BOX):
      args["render_mode"] = item.lower()
    else:
      raise template.TemplateSyntaxError("%r tag got an unknown argument: %r"\
        % (items[0], item))
  
  return UserStreamRenderNode(thing_name, **args)