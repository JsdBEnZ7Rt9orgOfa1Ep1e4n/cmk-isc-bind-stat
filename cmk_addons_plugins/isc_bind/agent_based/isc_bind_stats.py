#!/usr/bin/env python3
# Copyright (C) 2022 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections import defaultdict
from typing import Any, Mapping, Optional

from cmk.agent_based.v2 import ( 
    AgentSection,
    CheckPlugin, 
    CheckResult, 
    check_levels,
    DiscoveryResult, 
    get_value_store,
    Result, 
    Service, 
    State, 
    StringTable,
    get_rate,
)

Section = Mapping[str, Any]

# <<<isc_bind_stats>>>
# [server]
# json-stats-version 1.5.1
# boot-time 2023-08-04T18:07:40.764Z
# config-time 2023-08-07T10:43:48.904Z
# current-time 2023-08-17T13:06:08.610Z
# version 9.16.42-Debian
# opcodes.QUERY 18674373
# opcodes.IQUERY 0
# …


def parse(string_table: StringTable) -> Optional[Section]:
    if not string_table:
        return None
    all_sections = {"[server]"}
    sections = defaultdict(list)
    section = None
    for line in string_table:
        if line[0] in all_sections:
            section = line[0][1:-1]
        else:
            sections[section].append(line)
    return dict(iter(sections["server"]))


agent_section_isc_bind_stats = AgentSection(
    name="isc_bind_stats",
    parse_function=parse,
)


VARNAME=(
    "nsstats.Requestv4",
    "nsstats.Requestv6",
)

def discovery_stat(section: Section) -> DiscoveryResult:
    for k in ('current-timestamp', 'boot-time'):
        if k not in section:
            return
    for k in VARNAME:
        if k in section:
            yield Service()
            return

def check_stat(params: Mapping[str, Any], section: Section) -> CheckResult:
    if 'boot-time' not in section or 'current-timestamp' not in section:
        yield Result(state=State.UNKNOWN, summary="missing data")
        return
    store = get_value_store()
    if 'boot-time' not in store or store['boot-time'] != section['boot-time']:
        store.clear()
        store['boot-time'] = section['boot-time']
    ts = float(section['current-timestamp'])
    for k in VARNAME:
        if k not in section:
            continue
        v = int(section[k])
        rate = get_rate(store, k, ts, v)
        yield from check_levels(
            rate,
            levels_upper=params.get("levels_"+k.removeprefix("nsstats.")),
            metric_name=k,
            render_func=lambda v: f"{v:.1f}/s",
            label=k,
        )

_DEFAULT_LEVELS = ("fixed", (100000, 200000))

check_plugin_isc_bind_stats = CheckPlugin( 
    name="isc_bind_stats",
    sections=["isc_bind_stats"],
    service_name="ISC Bind rate",
    check_ruleset_name="param_isc_bind_stats",
    discovery_function=discovery_stat,
    check_function=check_stat,
    check_default_parameters={
            "levels_Requestv4": _DEFAULT_LEVELS,
            "levels_Requestv6": _DEFAULT_LEVELS,
        },
)
