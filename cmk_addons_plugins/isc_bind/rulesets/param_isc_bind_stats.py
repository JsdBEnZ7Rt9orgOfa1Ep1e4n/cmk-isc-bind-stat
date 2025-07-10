#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.rulesets.v1 import (
    rule_specs,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
    SimpleLevelsConfigModel,
)


def _param_form_isc_bind_stats() -> Dictionary:
    return Dictionary(
        elements={
            f"levels_Request{what}": DictElement[SimpleLevelsConfigModel[int]](
                parameter_form=SimpleLevels[int](
                    title=Title(f"Maximum Rate of IP{what} requests"),
                    form_spec_template=Integer(unit_symbol="req/sec"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(100000, 200000)),
                )
            )
            for what in ["v4", "v6"]
        },
    )


rule_spec_check_parameters = rule_specs.CheckParameters(
    name="param_isc_bind_stats",
    title=Title("ISC Bind Statistics"),
    topic=rule_specs.Topic.NETWORKING,
    parameter_form=_param_form_isc_bind_stats,
    condition=rule_specs.HostCondition(),
)
