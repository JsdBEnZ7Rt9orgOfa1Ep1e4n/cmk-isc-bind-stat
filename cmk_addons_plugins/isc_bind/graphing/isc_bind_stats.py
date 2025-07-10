#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# https://bind9.readthedocs.io/en/stable/reference.html#statistics-counters

from cmk.graphing.v1 import Title
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.metrics import (
    Color,
    DecimalNotation,
    Metric,
    Unit,
)
from cmk.graphing.v1.perfometers import (
    Closed,
    FocusRange,
    Open,
    Perfometer,
    Stacked,
)

UNIT_PER_SECOND = Unit(DecimalNotation("/s"))

metric_nsstats_Requestv4 = Metric(
    name="nsstats.Requestv4",
    title=Title("IPv4 requests received"),
    unit=UNIT_PER_SECOND,
    color=Color.LIGHT_CYAN,
)

metric_nsstats_Requestv6 = Metric(
    name="nsstats.Requestv6",
    title=Title("IPv6 requests received"),
    unit=UNIT_PER_SECOND,
    color=Color.CYAN,
)

perfometer_nsstats_Requestv4 = Perfometer(
    name="nsstats.Requestv4",
    focus_range=FocusRange(Closed(0), Open(1000)),
    segments=["nsstats.Requestv4"],
)

perfometer_nsstats_Requestv6 = Perfometer(
    name="nsstats.Requestv6",
    focus_range=FocusRange(Closed(0), Open(1000)),
    segments=["nsstats.Requestv6"],
)

perfometer_nsstats_reqs = Stacked(
    name="nsstats_reqs",
    lower=Perfometer(
        name="nsstats_reqs_v4",
        focus_range=FocusRange(Closed(0), Open(1000)),
        segments=["nsstats.Requestv4"],
    ),
    upper=Perfometer(
        name="nsstats_reqs_v6",
        focus_range=FocusRange(Closed(0), Open(1000)),
        segments=["nsstats.Requestv6"],
    )
)
