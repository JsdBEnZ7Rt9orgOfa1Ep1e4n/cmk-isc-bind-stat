cmk-isc-bind-stat
=================

BIND 9  DNS server allows you to gather statistics counters
if configured. The list of counters with descriptions can be found
[there](https://bind9.readthedocs.io/en/stable/reference.html#statistics-counters).

You need to enable BIND 9 HTTP statistics channel
 
    statistics-channels { inet 127.0.0.1 port 8080 ; };

see [here](https://kb.isc.org/docs/monitoring-recommendations-for-bind-9)
for more information.

Install CheckMK agent plugin into `/usr/lib/check_mk_agent/plugins/isc_bind_stats.py`.

Currently the only two counters are used for monitoring:

    levels_nsstats.Requestv4
    levels_nsstats.Requestv6

The only one service is inventorized: `ISC Bind rate`.
You can define levels for both metrics, the default is 100000, 200000 requests
per second. It depends on your situation what is normal traffic and what is
maybe DDoS and shoult be alerted.

--
Václav Ovsík <vaclav.ovsik@gmail.com>  Sun, 26 Nov 2023 22:10:25 +0100  
