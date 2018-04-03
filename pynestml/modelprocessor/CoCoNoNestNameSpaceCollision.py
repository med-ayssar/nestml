#
# CoCoNoNestNameSpaceCollision.py
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
from pynestml.modelprocessor.CoCo import CoCo
from pynestml.modelprocessor.ASTNeuron import ASTNeuron
from pynestml.utils.Logger import LoggingLevel, Logger
from pynestml.utils.Messages import Messages


class CoCoNoNestNameSpaceCollision(CoCo):
    """
    This coco tests that no functions are defined which collide with the nest namespace, which are:
      "update",
      "calibrate",
      "handle",
      "connect_sender",
      "check_connection",
      "get_status",
      "set_status",
      "init_state_",
      "init_buffers_"
    Allowed:
        function fun(...)
    Not allowed:    
        function handle(...) <- collision
    """
    __nestNameSpace = ['update', 'calibrate', 'handle', 'connect_sender', 'check_connection', 'get_status',
                       'set_status', 'init_state_', 'init_buffers_']

    @classmethod
    def check_co_co(cls, node=None):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ASTNeuron
        """
        assert (node is not None and isinstance(node, ASTNeuron)), \
            '(PyNestML.CoCo.CorrectNumerator) No or wrong type of neuron provided (%s)!' % type(node)
        for func in node.get_functions():
            if func.get_name() in cls.__nestNameSpace:
                code, message = Messages.getNestCollision(func.get_name())
                Logger.log_message(error_position=func.get_source_position(),
                                   code=code, message=message,
                                   log_level=LoggingLevel.ERROR)
        return
