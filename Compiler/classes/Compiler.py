#!/usr/bin/env python

import json
if __package__ is None or __package__ == '':
    from classes.Node import *
else:
    from .Node import *

def getID(i):
    idNumber = str(i).zfill(4)
    return '_element_id_' + idNumber

class Compiler:
    def __init__(self, dsl_mapping_file_path):
        with open(dsl_mapping_file_path) as data_file:
            self.dsl_mapping = json.load(data_file)

        self.opening_tag = self.dsl_mapping["opening-tag"]
        self.closing_tag = self.dsl_mapping["closing-tag"]
        self.content_holder = self.opening_tag + self.closing_tag

        self.root = Node("body", None, self.content_holder)

    def compile(self, input_file_path, output_file_path, rendering_function=None):
        dsl_file = open(input_file_path)
        current_parent = self.root
        i = 0
        for token in dsl_file:
            token = token.replace(" ", "").replace('\t','').replace("\n", "")

            if token.find(self.opening_tag) != -1:
                token = token.replace(self.opening_tag, "")
                element = Node(token, current_parent, self.content_holder, getID(i))
                current_parent.add_child(element)
                current_parent = element
                i += 1
            elif token.find(self.closing_tag) != -1:
                current_parent = current_parent.parent
            else:
                tokens = token.split(",")
                for t in tokens:
                    element = Node(t, current_parent, self.content_holder, getID(i))
                    current_parent.add_child(element)
                    i += 1
        output_html = '<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta charset="utf-8" />\n    <link rel="shortcut icon" href="%PUBLIC_URL%/favicon.ico" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <meta name="theme-color" content="#000000" />\n    <!-- Bootstrap core CSS -->\n    <link href="../compiled-bootstrap/css/bootstrap.css" rel="stylesheet">\n    \n    <!-- Custom styles for this template -->\n    <link href="../effect.css" rel="stylesheet">\n	<link href="../page.css" rel="stylesheet">\n\n <title>Generated Page</title>\n   </head>\n  <body>\n'
        output_html += self.root.render(self.dsl_mapping, rendering_function=rendering_function)
        output_html += '\n\t<script>\n\t\tvar x = document.getElementsByClassName("list-group-item");\n\t\tfor(var i = 0; i < x.length; i++) x[i].style.width = (parseInt(x[i].parentElement.offsetWidth) - 24) + "px";\n\t\tvar z = document.getElementsByClassName("card-header");\n\t\tfor(var i = 0; i < z.length; i++) z[i].style.width = (parseInt(z[i].parentElement.offsetWidth) - 24) + "px";\n\t</script>\n\n <script src="../jquery/jquery.min.js"></script>\n    <script src="../compiled-bootstrap/js/bootstrap.bundle.min.js"></script>\n  </body>\n</html>\n'
        with open(output_file_path, 'w') as output_file:
            output_file.write(output_html)
