# SPDX-License-Identifier: Apache-2.0
"""Reviewer mutation campaign: plant one change per scratch copy, build, run the
unit runner, and record which named tests fail. The source tree is never edited."""

import argparse
import concurrent.futures as cf
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

MAD = "src/core/mrp_mad.c"
MSRP = "src/modules/msrp.c"
PDU = "src/core/mrp_pdu.c"

# (label, file, old, new, expected failing test names; [] means "any failure")
CASES = [
    # Sample of the author's 39 reversals, checked against named tests.
    ("a-leaveall-scope", MAD, "if (a->attr_type == attr_type)",
     "if (a->attr_type == attr_type || a->attr_type != attr_type)",
     ["msrp_leaveall_changes_only_the_message_type_and_port",
      "mmrp_leaveall_changes_only_the_message_type_and_port"]),
    ("a-msrp-address", MSRP, "{ 0x01u, 0x80u, 0xC2u, 0x00u, 0x00u, 0x0Eu }",
     "{ 0x91u, 0xE0u, 0xF0u, 0x00u, 0x0Eu, 0x80u }",
     ["every_application_uses_its_standard_destination"]),
    ("a-milan-delayed-in-leave", MAD,
     "if (app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&",
     "if (false && app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&",
     ["talker_leave_in_is_immediate", "listener_leave_in_is_immediate"]),
    ("a-milan-restarted-lv-deadline", MAD,
     "const struct reg_entry *e = &reg_table[ev][ai->reg];",
     "const struct reg_entry *e = &reg_table[ev][ai->reg];\n"
     "    if (app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV && ai->reg == MRP_REG_STATE_LV) {\n"
     "        e = &reg_table[MRP_EVENT_RLV][MRP_REG_STATE_IN];\n    }",
     ["leave_in_lv_keeps_the_original_deadline"]),
    ("a-milan-option-scope", MAD,
     "if (app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&", "if (ev == MRP_EVENT_RLV &&",
     ["mvrp_keeps_ieee_leave_timing", "mmrp_keeps_ieee_leave_timing",
      "disabled_application_option_preserves_ieee_timing"]),
    ("a-wire-prevalidation", PDU, "int r = parse_pass(pdu, len, ops, NULL, NULL, NULL);", "int r = 0;",
     ["a_malformed_later_message_has_no_earlier_indications"]),
    ("a-split-fairness", MAD, "a->tx_deferred != (priority == 0)", "a->tx_deferred != (priority != 0)", []),
    ("a-talker-replacement", MAD, "rc->app->ops->attr_replaces) {", "rc->app->ops->attr_replaces && false) {", []),
    ("a-refused-storage", MAD, "if (r != 0) {\n        return r;",
     "if (r != 0) {\n        ps->prepared_pdu = NULL;\n        return r;", []),
    ("a-received-withdrawal-value", MAD, "previous && !declares ? previous :",
     "previous && !declares && false ? previous :", []),
    # Reviewer-owned plants.
    ("r-milan-on-rla", MAD, "if (app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&",
     "if (app->ops->milan_rapid_leave && (ev == MRP_EVENT_RLV || ev == MRP_EVENT_RLA) &&",
     ["leave_in_lv_keeps_the_original_deadline"]),
    ("r-milan-on-redeclare", MAD, "if (app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&",
     "if (app->ops->milan_rapid_leave && (ev == MRP_EVENT_RLV || ev == MRP_EVENT_REDECLARE) &&", []),
    ("r-milan-on-txla", MAD, "if (app->ops->milan_rapid_leave && ev == MRP_EVENT_RLV &&",
     "if (app->ops->milan_rapid_leave && (ev == MRP_EVENT_RLV || ev == MRP_EVENT_TXLA) &&", []),
    ("r-milan-no-indication", MAD, "REG_IND_LV, REG_TIMER_NONE, MRP_REG_STATE_MT\n    };",
     "REG_IND_NONE, REG_TIMER_NONE, MRP_REG_STATE_MT\n    };",
     ["talker_leave_in_is_immediate", "listener_leave_in_is_immediate"]),
    ("r-milan-from-lv-too", MAD, "ev == MRP_EVENT_RLV &&\n        ai->reg == MRP_REG_STATE_IN)",
     "ev == MRP_EVENT_RLV &&\n        ai->reg != MRP_REG_STATE_MT)",
     ["leave_in_lv_keeps_the_original_deadline"]),
    ("r-lv-join-indication-removed", MAD,
     "_RE(REG_IND_JOIN, REG_TIMER_STOP, MRP_REG_STATE_IN),  /* LV: Stop, Join; IN   */",
     "_RE(REG_IND_NONE, REG_TIMER_STOP, MRP_REG_STATE_IN),  /* LV: Stop, Join; IN   */", []),
    ("r-rx-leaveall-no-la-reset", MAD,
     "    la_event(rc->app, rc->ps, MRP_EVENT_RLA, rc->port_id);\n    for", "    for", []),
    ("r-tx-leaveall-no-local-rla", MAD,
     "        // 10.7.6.6: the committed sLA also signals rLA locally.\n        broadcast_event(app, ps, MRP_EVENT_RLA, port_id);",
     "        // reversal", []),
    ("r-parse-accept-bad-la", PDU, "if (la > MRP_LA_ALL || need > end - off)", "if (need > end - off)", []),
    ("r-parse-accept-bad-threepacked", PDU, "if (ev[k] > 215u) {", "if (ev[k] > 255u) {", []),
    ("r-domain-priority-bound", MSRP, "buf[1] > 7u || offset > 7u - buf[1]", "false", []),
    ("r-talker-dest-offset", MSRP, "increment_stream(t->dest_mac, 6, offset);",
     "increment_stream(t->dest_mac, 6, 0);", []),
    ("r-reclaim-lo", MAD, "(a->appl == MRP_APPL_STATE_VO ||",
     "(a->appl == MRP_APPL_STATE_VO || a->appl == MRP_APPL_STATE_LO ||", []),
    ("r-reclaim-registered", MAD, "if (a->reg == MRP_REG_STATE_MT &&", "if (true &&", []),
    ("r-leaveall-draw-upper", MAD, "ps->random % (ps->leaveall_cs / 2u - 1u)",
     "ps->random % (ps->leaveall_cs / 2u + 1u)", []),
    ("r-no-txlaf", MAD, "} else if (la) {\n            deliver_event(app, ps, a, MRP_EVENT_TXLAF",
     "} else if (false) {\n            deliver_event(app, ps, a, MRP_EVENT_TXLAF", []),
    ("r-no-join-spacing", MAD, "ps->join_wait = ps->join_cs;", "ps->join_wait = 0;", []),
    ("r-listener-subtype-tx", MAD, "mrp_four_pack(bytes[len], 0, 0, 0)", "mrp_four_pack(2, 0, 0, 0)", []),
    ("r-msrp-listlen", MAD, "buf[3] = (uint8_t)list;", "buf[3] = (uint8_t)(list + 1u);", []),
    ("r-destroy-leave-timer", MAD,
     "            shlan_timer_remove(&a->leave_timer);\n            shlan_free(a);\n            a = next;",
     "            shlan_free(a);\n            a = next;", []),
    ("r-rx-during-retention", MAD,
     "int mrp_rx(struct mrp_app *app, uint8_t port_id,\n           const uint8_t *pdu, size_t pdu_len)\n{\n    if (!app || port_id >= priv_of(app)->n_ports || (priv_of(app)->ports[port_id].in_send || priv_of(app)->ports[port_id].prepared_pdu)) {",
     "int mrp_rx(struct mrp_app *app, uint8_t port_id,\n           const uint8_t *pdu, size_t pdu_len)\n{\n    if (!app || port_id >= priv_of(app)->n_ports || (priv_of(app)->ports[port_id].in_send)) {", []),
    ("r-seed-ignored", MAD, "    ps->random = seed;", "    ps->random = 1u;", []),
    ("r-ignore-subtype-registers", PDU, "if (decl[k % 4u] == 0) {", "if (false) {", []),
    ("r-unknown-msrp-type-rejected", PDU, "if (!expected && msrp) {", "if (false) {", []),
    ("r-txla-registrar-ignored", MAD,
     "    {   /* IN: start leavetimer → LV */\n        _RE(REG_IND_NONE, REG_TIMER_START, MRP_REG_STATE_LV),",
     "    {   /* IN: start leavetimer → LV */\n        _RX,", []),
    ("r-replace-without-leavetimer", MAD,
     "                deliver_event(rc->app,rc->ps,old,MRP_EVENT_LEAVETIMER,rc->port_id);\n", "", []),
]

FAIL_RE = re.compile(r"(?:Failure|Exception): (?:[\w ]+ -> )*(\w+)")


def run_case(case, source, work, prefix, milan):
    label, name, old, new, expected = case
    root = work / label
    if root.exists():
        shutil.rmtree(root)
    tree = root / "src"
    shutil.copytree(source, tree)
    path = tree / name
    text = path.read_text()
    record = {"label": label, "file": name, "expected": expected, "milan": milan}
    if text.count(old) != 1:
        record.update(status="TARGET-NOT-UNIQUE", count=text.count(old))
        return record
    path.write_text(text.replace(old, new))
    env = os.environ.copy()
    env["CMAKE_PREFIX_PATH"] = str(prefix)
    env["LD_LIBRARY_PATH"] = str(prefix / "lib")
    build = root / "build"
    log = []
    for cmd in (["cmake", "-S", str(tree), "-B", str(build), "-DCMAKE_BUILD_TYPE=Debug",
                 f"-DLWSRP_MILAN={'ON' if milan else 'OFF'}"],
                ["cmake", "--build", str(build), "--parallel", "2"]):
        r = subprocess.run(cmd, env=env, capture_output=True, text=True)
        log.append(f"$ {' '.join(cmd)}\nrc={r.returncode}\n{r.stdout}{r.stderr}")
        if r.returncode:
            record.update(status="BUILD-FAILED", rc=r.returncode)
            (root / "log.txt").write_text("\n".join(log))
            return record
    try:
        r = subprocess.run([str(build / "unit_tests")], env=env, capture_output=True, text=True, timeout=120)
        out, rc = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = (e.stdout or b"").decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    log.append(f"$ unit_tests\nrc={rc}\n{out}")
    (root / "log.txt").write_text("\n".join(log))
    failed = sorted(set(FAIL_RE.findall(out)))
    summary = [l for l in out.splitlines() if l.startswith("Completed \"main\"")]
    record.update(rc=rc, failed_tests=failed, summary=summary[-1] if summary else "")
    killed = rc != 0 and (bool(failed) or rc == "timeout" or (isinstance(rc, int) and rc < 0))
    named = all(t in failed for t in expected)
    record["status"] = ("KILLED" if named else "KILLED-WRONG-TEST") if killed else "SURVIVED"
    shutil.rmtree(build, ignore_errors=True)
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--prefix", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--jobs", type=int, default=7)
    p.add_argument("--milan", action="store_true")
    a = p.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(lambda c: run_case(c, a.source, a.work, a.prefix, a.milan), CASES))
    a.out.write_text(json.dumps(results, indent=2) + "\n")
    for r in results:
        print(f"{r['status']:18} {r['label']:34} failed={','.join(r.get('failed_tests', []))}")


if __name__ == "__main__":
    main()
