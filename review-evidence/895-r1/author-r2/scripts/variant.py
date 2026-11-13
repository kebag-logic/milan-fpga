#!/usr/bin/env python3
"""Apply one named, behaviour-preserving rewrite of srp_mbx.c's declare_sources to a scratch TREE (lane 895 round 2).
usage: variant.py TREE NAME"""
import sys
from pathlib import Path
tree, name = Path(sys.argv[1]), sys.argv[2]
p = tree / 'sw/firmware/ctrl/srp/srp_mbx.c'
s = p.read_text()
LEAVE = ("            if (mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,&value) "
         "!= 0) {\n                done = false;\n            } else {\n                i->talkers &= ~bit;\n"
         "                m->held_cs[n] = SRP_REDECLARE_CS;\n            }\n")
V = {
 'stale': ("    i->stale = i->stale || t->reg_from != t->reg_to;\n", "    i->stale |= t->reg_from != t->reg_to;\n"),
 'valid2': ("        const bool valid = (i->gate & bit) != 0u;\n", "        const bool valid = (i->gate >> n & 1u) != 0u;\n"),
 'newret': ("                if (how == SRP_DECLARE_NEW) {\n                    return false;\n                }\n                done = false;\n",
            "                done = false;\n                if (how == SRP_DECLARE_NEW) {\n                    return false;\n                }\n"),
 'adv': ("        if (i->admitted[n]) {\n            used += slope;\n        }\n", "        if (advertised && (i->talkers & bit) != 0u) {\n            used += slope;\n        }\n"),
 'room': ("    uint64_t used = 0;\n", "    uint64_t used = 0;\n    const uint64_t room = (uint64_t)m->config.link_rate_bps * 3u / 4u;\n",
          "        bool admitted = i->sources[n].allocated && value.talker.max_interval_frames > 0 &&\n"
          "                        used + slope <= (uint64_t)m->config.link_rate_bps * 3u / 4u;\n",
          "        bool admitted = i->sources[n].allocated && value.talker.max_interval_frames > 0 && used + slope <= room;\n"),
 'swap': (LEAVE, "            if (mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,"
          "&value) == 0) {\n                i->talkers &= ~bit;\n                m->held_cs[n] = SRP_REDECLARE_CS;\n"
          "            } else {\n                done = false;\n            }\n"),
 'left': (LEAVE, "            const bool left = mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : "
          "MSRP_ATTR_TYPE_TALKER_FAILED,&value) == 0;\n            done = done && left;\n            if (left) {\n"
          "                i->talkers &= ~bit;\n                m->held_cs[n] = SRP_REDECLARE_CS;\n            }\n"),
 'clamp': ("        if (size < 68u) {\n            size = 68u;\n        }\n", "        size = size < 68u ? 68u : size;\n"),
 'code': ("            value.failure_info[8] = i->sources[n].allocated ? 1 : 2;\n",
          "            value.failure_info[8] = (uint8_t)(2u - i->sources[n].allocated);\n"),
 'used': ("        if (i->admitted[n]) {\n            used += slope;\n        }\n",
          "        used += i->admitted[n] ? slope : 0u;\n"),
 'size32': ("        uint64_t size = (uint64_t)value.talker.max_frame_size + 22u;\n        if (size < 68u) {\n"
            "            size = 68u;\n        }\n        uint64_t slope = (size + 20u) * value.talker.max_interval_frames * 64000u;\n",
            "        uint32_t size = value.talker.max_frame_size + 22u;\n        if (size < 68u) {\n            size = 68u;\n"
            "        }\n        uint64_t slope = (uint64_t)(size + 20u) * value.talker.max_interval_frames * 64000u;\n"),
}
for part in name.split('+'):
    pairs = V[part]
    for old, new in zip(pairs[0::2], pairs[1::2]):
        assert s.count(old) == 1, part
        s = s.replace(old, new)
p.write_text(s)
