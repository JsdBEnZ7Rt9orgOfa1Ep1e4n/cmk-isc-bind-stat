#!/usr/bin/env python3
# Copyright (C) 2022 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.
from collections import defaultdict
import time
from typing import Any, Iterable, Iterator, Mapping, NamedTuple, Optional, Sequence

from .agent_based_api.v1 import check_levels, get_rate, get_value_store, regex, register, render, Result, Service, State
from .agent_based_api.v1.type_defs import CheckResult, DiscoveryResult, StringTable

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


#def _parse_server(source: Iterator[Sequence[str]]) -> Mapping[str, Any]:
#	return dict(source)

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


register.agent_section(name="isc_bind_stats", parse_function=parse)


def discovery_stat(
    params: Sequence[Mapping[str, Any]], section: Section
) -> DiscoveryResult:

    def regex_match(what: Sequence[str], name: str) -> bool:
        if not what:
            return True
        for entry in what:
            if entry.startswith("~"):
                if regex(entry[1:]).match(name):
                    return True
                continue
            if entry == name:
                return True
        return False

    # defaults are always last and empty to apeace the new api
    for var in section:
        for settings in params:
            names = settings.get("names", [])
            if regex_match(names, var):
                yield Service(item=var)


def check_stat(item: str, params: Mapping[str, Any], section: Section) -> CheckResult:
    if item not in section:
        yield Result(state=State.UNKNOWN, summary="variable not found")
        return
    store = get_value_store()
    if 'boot-time' not in store or store['boot-time'] != section['boot-time']:
        store.clear()
        store['boot-time'] = section['boot-time']
    val = section[item]
    if val is not None:
        try:
            val_int = int(val)
        except:
            yield Result(state=State.OK, summary=f"{val}")
            return
        rate = get_rate(store, item, time.time(), val_int)
        yield from check_levels(
            int(rate),
            levels_upper=params.get("levels"),
            metric_name=item,
            render_func=str,
            label=item,
        )



_DEFAULT_LEVELS = (1000, 2000)
_DEFAULT_DISCOVERY_PARAMETERS = {
        "names": [
            "nsstats.Requestv4",
            ]
        }

register.check_plugin(
    name="isc_bind_stats",
    sections=["isc_bind_stats"],
    service_name="ISC Bind %s rate",
    check_ruleset_name="isc_bind_stats",
    discovery_function=discovery_stat,
    discovery_default_parameters=_DEFAULT_DISCOVERY_PARAMETERS,
    discovery_ruleset_name="isc_bind_stat_inventory",
    discovery_ruleset_type=register.RuleSetType.ALL,
    check_function=check_stat,
    check_default_parameters={
            "levels": _DEFAULT_LEVELS,
        },
)
