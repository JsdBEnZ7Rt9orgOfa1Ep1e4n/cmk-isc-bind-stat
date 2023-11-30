#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithoutItem,
    Levels,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import Dictionary


def _parameter_valuespec_stats() -> Dictionary:
    return Dictionary(
        elements=[
            (
                "levels_nsstats.Requestv4",
                Levels(
                    title=_("Maximum Rate of IPv4 requests"),
                    default_value=None,
                    default_levels=(100000, 200000),
                    unit="req/sec",
                ),
            ),
            (
                "levels_nsstats.Requestv6",
                Levels(
                    title=_("Maximum Rate of IPv6 requests"),
                    default_value=None,
                    default_levels=(100000, 200000),
                    unit="req/sec",
                ),
            ),
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="isc_bind_stats",
        group=RulespecGroupCheckParametersApplications,
        parameter_valuespec=_parameter_valuespec_stats,
        title=lambda: _("ISC Bind Statistics"),
    )
)
