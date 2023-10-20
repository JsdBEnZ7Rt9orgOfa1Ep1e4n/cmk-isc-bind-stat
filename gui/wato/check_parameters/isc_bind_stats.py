#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    HostRulespec,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
    RulespecGroupCheckParametersDiscovery,
)
from cmk.gui.valuespec import Dictionary, Integer, ListOfStrings, TextInput, Tuple


def _valuespec_isc_bind_stat_inventory() -> Dictionary:
    return Dictionary(
        title=_("ISC Bind Statistics Names"),
        elements=[
            (
                "names",
                ListOfStrings(
                    title=_("Name of Statistic variables"),
                ),
            ),
        ],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupCheckParametersDiscovery,
        match_type="dict",
        name="isc_bind_stat_inventory",
        valuespec=_valuespec_isc_bind_stat_inventory,
    )
)


def _item_spec_stats():
    return TextInput(
        title=_("Explicit Statistic Names"),
        help=_("Specify statistic names that the rule should apply to"),
    )


def _parameter_valuespec_stats() -> Dictionary:
    return Dictionary(
        title=_("Set Levels"),
        elements=[
            (
                "levels",
                Tuple(
                    title=_("Maximum Value"),
                    elements=[
                        Integer(title=_("Warning at")),
                        Integer(title=_("Critical at")),
                    ],
                ),
            ),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="isc_bind_stats",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_stats,
        parameter_valuespec=_parameter_valuespec_stats,
        title=lambda: _("ISC Bind Statistics"),
    )
)
