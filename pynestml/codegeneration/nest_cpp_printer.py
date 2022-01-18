# -*- coding: utf-8 -*-
#
# nest_cpp_printer.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.


from argparse import Namespace
from typing import Any, List, Mapping, Optional, Sequence
import pynestml
from pynestml.meta_model.ast_declaration import ASTDeclaration
from pynestml.meta_model.ast_function import ASTFunction
from pynestml.meta_model.ast_node import ASTNode
from pynestml.codegeneration.nest_codegenerator import NESTCodeGenerator
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.meta_model.ast_synapse import ASTSynapse
from jinja2 import Environment, Template, FileSystemLoader
import os
import copy
import textwrap


class NestCppPrinter:
    def __init__(self, node: ASTNode):
        if node.get_scope() is None:
            from pynestml.visitors.ast_symbol_table_visitor import ASTSymbolTableVisitor
            visitor = ASTSymbolTableVisitor()
            visitor.handle(node)

        code_generator = NESTCodeGenerator()
        if isinstance(node, ASTNeuron):
            code_generator.analyse_transform_neurons([node])
            self.namespace = code_generator._get_neuron_model_namespace(node)
        elif isinstance(node, ASTSynapse):
            code_generator.analyse_transform_synapses([node])
            self.namespace = code_generator._NESTCodeGenerator_get_synapse_model_namespace(node)
        else:
            raise TypeError(
                "The parameter node must be an instance of one the following sub-classes: [ASTNeuron, ASTSynapse]")
        self.node = node
        self.templates_root = os.path.join(pynestml.__path__[0], "codegeneration", "resources_nest", "point_neuron")
        self.directives = os.path.join(self.templates_root, "directives")

    def get_template(self, template_name):
        loader = FileSystemLoader(self.directives)
        env = Environment(loader=loader)
        template = env.get_template(f"{template_name}.jinja2")
        env.loader.searchpath.append(self.templates_root)
        return template

    def print_function(self, func: ASTFunction, func_namespace=""):
        output = self.namespace["printer"].print_function_definition(func, func_namespace)
        output += "{"

        ast = copy.deepcopy(self.namespace.get("ast", None))
        self.namespace["ast"] = func.get_block()

        block_template = self.get_template("Block")
        function_body = block_template.render(self.namespace)
        # reset to original value
        self.namespace["ast"] = ast
        padding = 2 * ' '
        padded_function_body = textwrap.indent(function_body, padding)

        output += padded_function_body
        output += "\n}"

        return output

    def print_declaration(self, declaration: ASTDeclaration):
        declaration_template = self.get_template("Declaration")
        ast = copy.deepcopy(self.namespace.get("ast", None))
        self.namespace["ast"] = declaration
        cpp_declaration = declaration_template.render(self.namespace)
        # reset to original value
        self.namespace["ast"] = ast
        return cpp_declaration

    def print_functions(self, namespace=""):
        functions = self.node.get_functions()
        outputs = {}
        for func in functions:
            name = func.get_name()
            output = self.print_function(func, namespace)
            outputs[name] = output
        return outputs

    def print_declarations(self, ast_block):
        declarations = ast_block.get_declarations()
        outputs = {}
        for declaration in declarations:
            variables = declaration.get_variables()
            names = tuple([v.name for v in variables])
            printed_declaration = self.print_declaration(declaration)
            outputs[names] = printed_declaration
        return outputs

    def print_struct(self, struct_template_name):
        struct_template = self.get_template(struct_template_name)
        cpp_struct = struct_template.render(self.namespace)
        return cpp_struct

    def print_state_struct(self):
        return self.print_struct("StateStruct")

    def print_parameters_struct(self):
        return self.print_struct("ParameterStruct")

    def print_internal_struct(self):
        return self.print_struct("InternalStruct")
