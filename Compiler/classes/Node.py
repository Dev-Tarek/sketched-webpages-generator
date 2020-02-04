#!/usr/bin/env python
from __future__ import print_function
import random

classes = {
    'img': {'card-div': 'card-img-top'},
    'jumbotron': {'container': 'my-4'},
    'large-title': {'jumbotron': 'display-3'},
    'text': {'jumbotron': 'lead'},
    'button': {'jumbotron': 'btn-lg mx-1'},
}

IMAGE_SIZES = ['700x400', '400x700', '700x700']

class Node:
    def __init__(self, key, parent_node, content_holder, id=''):
        self.key = key
        self.parent = parent_node
        self.children = []
        self.content_holder = content_holder
        self.id = id

    def add_child(self, child):
        self.children.append(child)

    def show(self):
        print(self.key)
        for child in self.children:
            child.show()

    def render(self, mapping, rendering_function=None):
        content = ""
        for child in self.children:
            content += child.render(mapping, rendering_function)
        
        value = mapping[self.key]
        
        value = value.replace('$', 'id="'+self.id+'"')
        value = value.replace('~', self.id)
        
        if classes.get(self.key):
            if classes.get(self.key).get(self.parent.key):
                value = value.replace('@', classes.get(self.key).get(self.parent.key))
            else:
                value = value.replace('@', '')
                
        if self.key == 'img':
            value = value.replace('_size_', random.choice(IMAGE_SIZES))
            if self.parent.key == 'card-div':
                value = value.replace("style=\"width: inherit;\"", '')
        
        if rendering_function is not None:
            if self.key == 'text' and self.parent.key == 'card-footer':
                value = rendering_function('text-footer', value)
            else:
                value = rendering_function(self.key, value)

        if len(self.children) != 0:
            value = value.replace(self.content_holder, content)

        return value
