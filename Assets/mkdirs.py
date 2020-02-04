# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:05:10 2019

@author: Abdelrahman
"""
import os
dsl = ["navbar",
"link-list",
"large-title",
"med-title",
"list-group",
"list-group-item",
"list-group-item-text",
"carousel",
"text",
"card-header",
"card-div",
"img",
"card-body",
"card-footer",
"footer",
"jumbotron",
"button"]

for element in dsl:
    os.mkdir(element)