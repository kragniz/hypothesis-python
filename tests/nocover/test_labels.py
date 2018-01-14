# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2018 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

import hypothesis.strategies as st
from hypothesis.internal.compat import hbytes
from hypothesis.internal.conjecture.data import Status, ConjectureData


def test_labels_are_cached():
    x = st.integers()
    assert x.label is x.label


def test_labels_are_distinct():
    assert st.integers().label != st.text().label


@st.composite
def foo(draw):
    pass


@st.composite
def bar(draw):
    pass


def test_different_composites_have_different_labels():
    assert foo().label != bar().label


def get_tags(strat, buf):
    d = ConjectureData.for_buffer(buf)
    d.draw(strat)
    d.freeze()
    assert d.status == Status.VALID
    return d.tags


def test_labels_get_used_for_tagging():
    assert get_tags(st.integers(), hbytes(8)) != get_tags(st.text(), hbytes(8))


def test_labels_get_used_for_tagging_branches():
    strat = st.one_of(
        st.booleans().map(lambda x: not x),
        st.booleans().map(lambda x: x),
    )

    assert get_tags(strat, hbytes(2)) != get_tags(strat, hbytes([1, 0]))
