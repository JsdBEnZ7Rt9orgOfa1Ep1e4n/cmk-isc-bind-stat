#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _l
from cmk.gui.plugins.metrics.utils import graph_info, metric_info


# https://bind9.readthedocs.io/en/stable/reference.html#statistics-counters

metric_info["nsstats.Requestv4"] = {
    "title": _l("IPv4 requests received"),
    "unit": "1/s",
    "color": "32/a",
}

metric_info["nsstats.Requestv6"] = {
    "title": _l("IPv6 requests received"),
    "unit": "1/s",
    "color": "22/a",
}
