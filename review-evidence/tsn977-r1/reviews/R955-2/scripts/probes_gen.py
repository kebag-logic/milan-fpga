#!/usr/bin/env python3
"""Generate reviewer probe mutants for the new paths in src/acmp.c. Usage: probes_gen.py ACMP_C OUT_JSON"""
import json, re, sys
src = open(sys.argv[1]).read()
P = []
def add(name, old, new):
    P.append({"name": name, "old": old, "new": new})
# Walk structure in the three new loops, anchored by each loop's first unique body line.
heads = {"publish": "\t\tbool settled = s->state", "admit": "\t\tuint64_t talker = s->binding.talker_entity_id;",
         "finish": "\t\tif (record_moved(s)) {"}
loop = ("\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k, bits >>= 1) {\n\t\tif (k % 32u == 0u) {\n\t\t\tbits = a->dirty[k / 32u];\n"
        "\t\t}\n\t\tif ((bits & 1u) == 0u) {\n\t\t\tcontinue;\n\t\t}\n\t\tstruct acmp_sink *s = &a->sinks[k];\n")
for w, h in heads.items():
    old = loop + h
    add(f"r-{w}-word-zero", old, old.replace("a->dirty[k / 32u]", "a->dirty[0]"))
    add(f"r-{w}-no-shift", old, old.replace("++k, bits >>= 1)", "++k)"))
    add(f"r-{w}-no-reload", old, old.replace("if (k % 32u == 0u)", "if (k == 0u)"))
    add(f"r-{w}-every-sink", old, old.replace("if ((bits & 1u) == 0u)", "if (false && (bits & 1u) == 0u)"))
    add(f"r-{w}-stop-at-empty-word", old, old.replace("\t\t\tbits = a->dirty[k / 32u];\n\t\t}\n",
        "\t\t\tbits = a->dirty[k / 32u];\n\t\t}\n\t\tif (bits == 0u) {\n\t\t\tbreak;\n\t\t}\n"))
# record_moved: every term and every gate.
rm = src[src.index("static bool record_moved"):src.index("// Milan v1.2 5.6.4.1")]
L = "(uint32_t)(p[0] ^ flags) | p[1] | (uint32_t)(p[2] ^ (unique >> 8)) |"
add("r-rec-drop-p0", L, L.replace("(uint32_t)(p[0] ^ flags) | ", ""))
add("r-rec-drop-p1", L, L.replace("p[1] | ", ""))
add("r-rec-drop-p2", L, L.replace(" | (uint32_t)(p[2] ^ (unique >> 8)) |", " |"))
add("r-rec-drop-p3", "\t\t\t(uint32_t)(p[3] ^ (unique & 0xFFu)) |\n", "")
for i in range(4, 20):
    m = re.search(r"\(p\[%d\] \^ [^|]*?\)\)?\)?(?= \||;)" % i, rm)
    term = m.group(0)
    # balance parentheses of the captured term
    while term.count("(") > term.count(")"):
        term += ")"
    while term.count(")") > term.count("("):
        term = term[:-1]
    add(f"r-rec-drop-p{i}", term, "0u")
add("r-rec-unique-ungated", "uint16_t unique = b ? s->binding.talker_unique_id : 0u;", "uint16_t unique = s->binding.talker_unique_id;")
add("r-rec-talker-ungated", "uint64_t talker = b ? s->binding.talker_entity_id : 0u;", "uint64_t talker = s->binding.talker_entity_id;")
add("r-rec-controller-ungated", "uint64_t controller = b ? s->binding.controller_entity_id : 0u;", "uint64_t controller = s->binding.controller_entity_id;")
add("r-rec-no-started-flag", "uint8_t flags = (uint8_t)(b ? (BIND_VALID | (s->started ? BIND_STARTED : 0u) |", "uint8_t flags = (uint8_t)(b ? (BIND_VALID | 0u |")
add("r-rec-no-wait-flag", "\t\t\t       (s->binding.streaming_wait ? BIND_STREAMING_WAIT : 0u)) : 0u);\n\tuint16_t unique", "\t\t\t       0u) : 0u);\n\tuint16_t unique")
add("r-rec-no-valid-flag", "uint8_t flags = (uint8_t)(b ? (BIND_VALID | (s->started", "uint8_t flags = (uint8_t)(b ? (0u | (s->started")
add("r-rec-th-low", "uint32_t th = (uint32_t)(talker >> 32);", "uint32_t th = (uint32_t)(talker);")
add("r-rec-ch-low", "uint32_t ch = (uint32_t)(controller >> 32);", "uint32_t ch = (uint32_t)(controller);")
add("r-rec-always-moved", "\t\t(p[16] ^ (cl >> 24)) | (p[17] ^ ((cl >> 16) & 0xFFu)) | (p[18] ^ ((cl >> 8) & 0xFFu)) | (p[19] ^ (cl & 0xFFu));\n\treturn diff != 0u;",
    "\t\t(p[16] ^ (cl >> 24)) | (p[17] ^ ((cl >> 16) & 0xFFu)) | (p[18] ^ ((cl >> 8) & 0xFFu)) | (p[19] ^ (cl & 0xFFu));\n\treturn diff != 0u || true;")
add("r-fin-saved-not-written", "\t\t\trecord_of(s, s->saved);\n\t\t\tp_persist(a, k);", "\t\t\tp_persist(a, k);")
# view_moved: every term and every gate.
vm = {"stream": "(stream_id ^ y->stream.stream_id) | ", "dest": "(dest_mac ^ y->stream.dest_mac) |",
      "vlan": "(uint64_t)(vlan_id ^ y->stream.vlan_id) |", "bound": "| (uint64_t)(s->bound != y->bound) |",
      "started": "(uint64_t)(s->started != y->started) | (uint64_t)(registered", "registered": "| (uint64_t)(registered != y->talker_registered) |"}
add("r-view-drop-stream", vm["stream"], "")
add("r-view-drop-dest", "(stream_id ^ y->stream.stream_id) | (dest_mac ^ y->stream.dest_mac) |", "(stream_id ^ y->stream.stream_id) |")
add("r-view-drop-vlan", "\t\t\t(uint64_t)(vlan_id ^ y->stream.vlan_id) |\n", "")
add("r-view-drop-bound", "(uint64_t)(s->acmp_status ^ y->acmp_status) | (uint64_t)(s->bound != y->bound) |", "(uint64_t)(s->acmp_status ^ y->acmp_status) |")
add("r-view-drop-started", "(uint64_t)(s->started != y->started) | (uint64_t)(registered != y", "(uint64_t)(registered != y")
add("r-view-drop-registered", "| (uint64_t)(registered != y->talker_registered) |", "|")
add("r-view-drop-failed", " |\n\t\t\t(uint64_t)((registered && s->tk_failed) != y->registering_failed);", ";")
add("r-view-failed-ungated", "(uint64_t)((registered && s->tk_failed) != y->registering_failed)", "(uint64_t)(s->tk_failed != y->registering_failed)")
add("r-view-stream-ungated", "\tuint64_t stream_id = settled ? s->stream.stream_id : 0u;", "\tuint64_t stream_id = s->stream.stream_id;")
add("r-view-dest-ungated", "\tuint64_t dest_mac = settled ? s->stream.dest_mac : 0u;", "\tuint64_t dest_mac = s->stream.dest_mac;")
add("r-view-vlan-ungated", "\tuint16_t vlan_id = settled ? s->stream.vlan_id : 0u;", "\tuint16_t vlan_id = s->stream.vlan_id;")
add("r-view-settled-rsv-only", "\tbool settled = s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK;\n\tbool registered", "\tbool settled = s->state == ACMP_SETTLED_RSV_OK;\n\tbool registered")
add("r-view-registered-any-settled", "\tbool registered = s->state == ACMP_SETTLED_RSV_OK;\n\tuint64_t stream_id", "\tbool registered = s->state == ACMP_SETTLED_RSV_OK || s->state == ACMP_SETTLED_NO_RSV;\n\tuint64_t stream_id")
add("r-view-always-moved", "\t\t\t(uint64_t)((registered && s->tk_failed) != y->registering_failed);\n\treturn diff != 0u;", "\t\t\t(uint64_t)((registered && s->tk_failed) != y->registering_failed);\n\treturn diff != 0u || true;")
add("r-fin-reported-not-written", "\t\t\tview_of(s, &s->reported);\n\t\t\tp_changed(a, k);", "\t\t\tp_changed(a, k);")
# view_of field-by-field copies.
for f in ["talker_entity_id", "controller_entity_id", "talker_unique_id", "streaming_wait"]:
    add("r-viewof-drop-binding-" + f, f"\tv->binding.{f} = s->binding.{f};\n", "")
for f in ["stream_id", "dest_mac", "vlan_id"]:
    add("r-viewof-drop-stream-" + f, f"\t\tv->stream.{f} = s->stream.{f};\n", "")
add("r-viewof-binding-swap-ids", "\tv->binding.talker_entity_id = s->binding.talker_entity_id;\n\tv->binding.controller_entity_id = s->binding.controller_entity_id;",
    "\tv->binding.talker_entity_id = s->binding.controller_entity_id;\n\tv->binding.controller_entity_id = s->binding.talker_entity_id;")
add("r-clear-dirty-if-kept", "\t}\n\ta->dirty_if = 0u;\n}", "\t}\n}")
bad = [p["name"] for p in P if src.count(p["old"]) != 1 or p["old"] == p["new"]]
if bad:
    sys.exit("anchors not unique or no-op: " + ", ".join(bad))
json.dump(P, open(sys.argv[2], "w"), indent=1)
print(len(P), "probes")
