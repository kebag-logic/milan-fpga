# R532-12 reviewer probes: disposable mutations of the round-12 SRP feedback
# observation (srp_mbx.c). Each is run against whole suites ('*'); a probe is
# CAUGHT when the suite fails. 'expect' is the reviewer's prior: CAUGHT for a
# behaviour change the standing tests must detect, ANY for an informative probe
# (possibly equivalent or only transient inside one PDU), judged in REPORT.md.
_M = [
    ("q01-precedence-advertise-first",
     "        s->desired = (s->registered_kinds & 1u) ? 1u : (s->registered_kinds & 2u);",
     "        s->desired = (s->registered_kinds & 2u) ? 2u : (s->registered_kinds & 1u);", "ANY"),
    ("q02-no-pre-receive-seed",
     "        // Seed copied kinds from the registrar before entering any callback.\n        snapshot(i);\n",
     "        // seed removed\n", "ANY"),
    ("q03-leave-ignores-talkers",
     "    } else if (type == MSRP_ATTR_TYPE_TALKER_ADV || type == MSRP_ATTR_TYPE_TALKER_FAILED) {",
     "    } else if (false) {", "CAUGHT"),
    ("q04-leave-clears-advertise-only",
     "talker_changed(from_ctx(ctx),value,type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u,false);",
     "talker_changed(from_ctx(ctx),value,2u,false);", "ANY"),
    ("q05-set-ignores-identity",
     "            if (registered && memcmp(s->dest_mac,v->dest_mac,6) == 0 && s->vid == v->vlan_id) {",
     "            if (registered) {", "CAUGHT"),
    ("q06-change-clears-both-kinds",
     "            s->registered_kinds &= (uint8_t)~kind;",
     "            s->registered_kinds = 0;", "ANY"),
    ("q07-seed-drops-failed",
     "                    sink->registered_kinds |= 1u;\n",
     "", "CAUGHT"),
    ("q08-seed-drops-advertise",
     "                    sink->registered_kinds |= 2u;\n",
     "", "CAUGHT"),
    ("q09-filter-no-observation",
     "        s->desired = (s->registered_kinds & 1u) ? 1u : (s->registered_kinds & 2u);\n        capture(s,previous);",
     "        (void)previous;", "CAUGHT"),
    ("q10-filter-reenters-visitor",
     "    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {\n        struct srp_sink *s = &i->sinks[k];\n        uint8_t previous = s->desired;",
     "    snapshot(i);\n    for (unsigned k = 0; k < 0u; ++k) {\n        struct srp_sink *s = &i->sinks[k];\n        uint8_t previous = s->desired;", "ANY"),
    ("q11-reset-keeps-kinds",
     "        i->sinks[k].registered_kinds = 0;\n        capture(&i->sinks[k],previous);",
     "        capture(&i->sinks[k],previous);", "ANY"),
    ("q12-snapshot-keeps-kinds",
     "        i->sinks[k].desired = 0;\n        i->sinks[k].registered_kinds = 0;\n    }",
     "        i->sinks[k].desired = 0;\n    }", "ANY"),
    ("q13-failed-indication-as-advertise",
     "talker_changed(from_ctx(ctx),&value->talker,1u,true);",
     "talker_changed(from_ctx(ctx),&value->talker,2u,true);", "CAUGHT"),
]

PROBES = []
for name, old, new, expect in _M:
    for suite in ("test_acmp_mbx.cpp", "srp_mbx.cpp"):
        PROBES.append({"name": f"{name}@{suite.removesuffix('.cpp')}", "test": "*", "old": old, "new": new,
                       "needle": "", "path": "srp/srp_mbx.c", "suite": suite, "expect": "ANY"})
