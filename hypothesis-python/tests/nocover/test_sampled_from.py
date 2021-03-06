# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

import pytest

import hypothesis.strategies as st
from hypothesis import given
from hypothesis.internal.compat import hrange
from tests.common.utils import counts_calls


@pytest.mark.parametrize("n", [100, 10 ** 5, 10 ** 6, 2 ** 25])
def test_filter_large_lists(n):
    filter_limit = 100 * 10000

    @counts_calls
    def cond(x):
        assert cond.calls < filter_limit
        return x % 2 != 0

    s = st.sampled_from(hrange(n)).filter(cond)

    @given(s)
    def run(x):
        assert x % 2 != 0

    run()

    assert cond.calls < filter_limit
