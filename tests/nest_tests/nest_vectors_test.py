# -*- coding: utf-8 -*-
#
# nest_vectors_test.py
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
import os
import unittest
import numpy as np

import nest

from pynestml.frontend.pynestml_frontend import to_nest, install_nest


class NestVectorsIntegrationTest(unittest.TestCase):
    """
    Tests the code generation and vector operations from NESTML to NEST.
    """

    def test_vectors(self):
        input_path = os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), "resources", "Vectors.nestml")))
        nest_path = nest.ll_api.sli_func("statusdict/prefix ::")
        target_path = 'target'
        logging_level = 'INFO'
        module_name = 'nestmlmodule'
        store_log = False
        suffix = '_nestml'
        dev = True
        to_nest(input_path, target_path, logging_level, module_name, store_log, suffix, dev)
        install_nest(target_path, nest_path)
        nest.set_verbosity("M_ALL")

        nest.ResetKernel()
        nest.Install("nestmlmodule")

        neuron = nest.Create("vectors_nestml")
        multimeter = nest.Create('multimeter')
        recordables = list()
        recordables.extend(["G_IN_" + str(i + 1) for i in range(0, 20)])
        recordables.extend(["G_EX_" + str(i + 1) for i in range(0, 10)])
        recordables.append("V_m")
        multimeter.set({"record_from": recordables})
        nest.Connect(multimeter, neuron)

        nest.Simulate(2.0)

        events = multimeter.get("events")
        g_in = events["G_IN_1"]
        g_ex = events["G_EX_2"]
        print("g_in: {}, g_ex: {}".format(g_in, g_ex))
        np.testing.assert_almost_equal(g_in[-1], 11.)
        np.testing.assert_almost_equal(g_ex[-1], -2.)

        v_m = multimeter.get("events")["V_m"]
        print("V_m: {}".format(v_m))
        np.testing.assert_almost_equal(v_m[-1], -0.3)
