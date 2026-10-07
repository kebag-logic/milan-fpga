#!/usr/bin/env python3
"""r530_probes.py - reviewer-planted defects for PR #688 (lane F3), round R530-1.

Each probe is a defect the reviewer chose (not copied from the author's
acmp_mutants.py table), planted into a COPY of sw/firmware/ctrl through the
campaign's own plant() helper, then the arms that test it are built and run.
A probe is CAUGHT when its arm exits 1 and one of the tests the reviewer
expects to cover that behaviour reports [FAIL]. Every [FAIL] line is printed.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 r530_probes.py <clone> <scratch> [K/N [FIRST]]
FIRST skips the table's first FIRST probes: batch 1 is 0 to 38, batch 2 from 39.
Batch 1 was run as slices 1/3, 2/3 and 3/3 with FIRST 0; batch 2 as 1/2 and 2/2 with FIRST 39;
batch 3 (the clock wrap) as 1/1 with FIRST 50.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
part = sys.argv[3] if len(sys.argv) > 3 else "1/1"
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_mutants import plant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

C, X, N = "acmp/acmp.c", "acmp/acmp_mbx.c", "acmp/acmp_nvm.c"
CORE = ("acmp", "acmpwalk")
# (name, path, old, new, arms, expected tests (prefix match; any one suffices))
PROBES = (
    # ---- listener cells (Table 5.30) ----
    ("L1-duplicate-takes-new-seq", C, "\t\ts->probe_retried = true;\n\t\tsend_probe(a, k);",
     "\t\ts->probe_retried = true;\n\t\tprobe(a, k);", CORE,
     ("AcmpCore.A10", "Table530/ListenerWalk.Graded")),
    ("L2-retry-clears-status", C, "\t} else if (kind == ACMP_TIMER_RETRY) {                  // step 2: the ACMP status stays\n\t\tdelay(a, s);",
     "\t} else if (kind == ACMP_TIMER_RETRY) {\n\t\ts->acmp_status = 0u;\n\t\tdelay(a, s);", CORE,
     ("AcmpCore.A11", "Table530/ListenerWalk.Graded")),
    ("L3-lock-status-13", C, "struct pdu r = echo(cmd, ACMP_STATUS_CONTROLLER_NOT_AUTHORIZED);",
     "struct pdu r = echo(cmd, 13u);", CORE, ("AcmpCore.A4", "ListenerScenario.LD3")),
    ("L4-probe-resp-no-seq-guard", C, " ||\n\t    rsp->talker_uid != s->probe_talker_uid || rsp->seq != s->probe_seq) {",
     " ||\n\t    rsp->talker_uid != s->probe_talker_uid) {", CORE, ("AcmpCore.A7",)),
    ("L5-guard-reads-binding-controller", C, "if (rsp->controller != s->probe_controller ||",
     "if (rsp->controller != s->binding.controller_entity_id ||", CORE, ("AcmpCore.A7TheGuardReads",)),
    ("L6-departed-unsettles", C, "\t    s->state == ACMP_PRB_W_RETRY) {\n\t\tsm_stop(s);\n\t\tpassive(s);",
     "\t    s->state == ACMP_PRB_W_RETRY || s->state == ACMP_SETTLED_NO_RSV) {\n\t\tsm_stop(s);\n\t\tpassive(s);",
     CORE, ("AcmpCore.A22", "Table530/ListenerWalk.Graded")),
    ("L7-same-source-rebind-restarts", C, "\t\tbind_response(a, interface, k, cmd);\n\t\treturn;\n\t}",
     "\t\tbind_response(a, interface, k, cmd);\n\t}", CORE, ("AcmpCore.A5", "Table530/ListenerWalk.Graded")),
    ("L8-no-tk-ignores-discovered", C, "static void reprobe(struct acmp *a, struct acmp_sink *s)\n{\n\tif (!s->discovered) {",
     "static void reprobe(struct acmp *a, struct acmp_sink *s)\n{\n\tif (!s->discovered || s->state == ACMP_SETTLED_NO_RSV) {",
     CORE, ("AcmpCore.A13", "Table530/ListenerWalk.Graded")),
    ("L9-unbind-keeps-srp", C, "\tstruct acmp_sink *s = &a->sinks[k];\n\tif (s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK) {\n\t\tsrp_stop(a, k);\n\t}\n\tdisc_stop(s);\n\ts->bound = false;",
     "\tstruct acmp_sink *s = &a->sinks[k];\n\tdisc_stop(s);\n\ts->bound = false;", CORE,
     ("AcmpCore.A3", "Table530/ListenerWalk.Graded")),
    ("L10-failed-probe-keeps-status-0", C, "\t\ts->acmp_status = rsp->status;\n", "", CORE,
     ("AcmpCore.A9", "Table530/ListenerWalk.Graded")),
    ("L11-unknown-sink-not-answered", C, "\t\tstruct pdu r = echo(cmd, ACMP_STATUS_LISTENER_UNKNOWN_ID);         // Table 5.27\n\t\trespond(a, interface, &r, 0u);\n",
     "", CORE, ("AcmpCore.A2Unknown", "ListenerScenario.LW2")),
    # ---- discovery (5.6.4) ----
    ("D1-restart-strict-less", C, "if (index <= s->disc_available_index) {", "if (index < s->disc_available_index) {",
     CORE, ("AcmpCore.A22", "Table554/DiscoveryWalk.Graded")),
    ("D2-restart-skips-gm", C, "\t\tif (!gm_matches(a, d)) {\n\t\t\ts->adp_armed = false;",
     "\t\tif (false) {\n\t\t\ts->adp_armed = false;", CORE, ("AcmpCore.A22", "Table554/DiscoveryWalk.Graded")),
    ("D3-departing-skips-ifx", C, "if (!s->discovered || ifx != s->disc_interface_index) {",
     "if (!s->discovered) {", CORE, ("AcmpCore.A22", "Table554/DiscoveryWalk.Graded")),
    ("D4-valid-time-low-bits", C, "(uint32_t)(frame[A_VALID_TIME] >> 3) * ACMP_VALID_TIME_UNIT_MS",
     "(uint32_t)(frame[A_VALID_TIME] & 0x1Fu) * ACMP_VALID_TIME_UNIT_MS", CORE, ("AcmpCore.A22",)),
    ("D5-refresh-not-rearmed", C, "\ts->disc_available_index = index;                        // step 3\n\tadp_arm(a, s, valid_ms);",
     "\ts->disc_available_index = index;", CORE, ("AcmpCore.A22", "Table554/DiscoveryWalk.Graded")),
    ("D6-departing-keeps-no-adp", C, "\ts->adp_armed = false;\n\ttk_departed(s);\n}", "\ttk_departed(s);\n}", CORE,
     ("AcmpCore.A22", "Table554/DiscoveryWalk.Graded")),
    ("D7-adp-any-interface", C, "if (!s->disc_running || s->interface != interface ||",
     "if (!s->disc_running ||", CORE, ("AcmpCore.A22Only",)),
    ("D8-first-available-skips-gm", C, "\t\tif (!gm_matches(a, d)) {\n\t\t\treturn;                                 // 5.6.4.5.1 step 1",
     "\t\tif (false) {\n\t\t\treturn;", CORE, ("AcmpCore.A22Available", "Table554/DiscoveryWalk.Graded")),
    # ---- talker (5.5.4) ----
    ("T1-disconnect-unknown-success", C, "\tif (src >= a->cfg.n_sources) {",
     "\tif (src >= a->cfg.n_sources && cmd->msg != ACMP_MSG_DISCONNECT_TX_COMMAND) {", CORE,
     ("AcmpCore.A20Disconnect", "TalkerWalk.TW3")),
    ("T2-probe-tx-drops-streaming-wait", C, "r.flags = cmd->flags & (ACMP_FLAG_FAST_CONNECT | ACMP_FLAG_STREAMING_WAIT);",
     "r.flags = cmd->flags & ACMP_FLAG_FAST_CONNECT;", CORE, ("AcmpCore.A20Probe", "TalkerWalk.TW1")),
    ("T3-get-tx-state-echoes-listener", C, "\tr.listener = 0u;\n\tr.listener_uid = 0u;\n", "", CORE,
     ("AcmpCore.A20Disconnect", "TalkerWalk.TW2")),
    ("T4-get-tx-connection-checks-source", C, "if (cmd->msg == ACMP_MSG_GET_TX_CONNECTION_COMMAND) {",
     "if (cmd->msg == ACMP_MSG_GET_TX_CONNECTION_COMMAND && src < a->cfg.n_sources) {", CORE,
     ("AcmpCore.A20Disconnect", "TalkerWalk.TW3")),
    ("T5-probe-tx-any-interface", C, "if (cmd->msg == ACMP_MSG_PROBE_TX_COMMAND && interface != a->cfg.source_interface[src]) {",
     "if (cmd->msg == ACMP_MSG_PROBE_TX_COMMAND && interface > a->cfg.source_interface[src]) {", CORE,
     ("AcmpCore.A20Probe", "TalkerWalk.TW4")),
    # ---- adapter / ordering (#653, owed, timers, tap) ----
    ("X1-stale-tag-accepted", X, "if (!i->armed || ev->timer_tag != i->tag) {", "if (!i->armed) {", ("acmp",),
     ("AcmpMailbox.B4",)),
    ("X2-tap-departing-to-adp", X, "if ((f->bytes[ACMP_HEADER_BYTES + 1u] & 0x0Fu) <= ACMP_ADP_MSG_ENTITY_DEPARTING) {",
     "if ((f->bytes[ACMP_HEADER_BYTES + 1u] & 0x0Fu) == ACMP_ADP_MSG_ENTITY_AVAILABLE) {", ("acmp",),
     ("AcmpMailbox.B5", "AcmpMailbox.C10")),
    ("X3-one-slot-for-all-interfaces", X, "m->ifs[k].slot = (uint8_t)(first_slot + k);",
     "m->ifs[k].slot = (uint8_t)(first_slot);", ("acmp",), ("AcmpMailbox.B3", "AcmpMailbox.B7")),
    ("X4-change-before-response", C, "if (s->change_owed == 0u && !view_equal(&v, &s->reported)) {",
     "if (!view_equal(&v, &s->reported)) {", CORE, ("AcmpCore.A19", "AcmpMailbox.E1")),
    ("X5-send-past-owed", C, "if (a->owed_count == 0u && p_send(a, interface, frame)) {",
     "if (p_send(a, interface, frame)) {", CORE, ("AcmpCore.A19Nothing", "AcmpMailbox.E")),
    ("X6-poll-lets-loop-sleep", X, "\treturn acmp_poll(&m->acmp);", "\t(void)acmp_poll(&m->acmp);\n\treturn false;",
     ("acmp",), ("AcmpMailbox.E",)),
    ("X7-rearm-every-entry", C, "if (any && (!a->timer_armed[i] || a->timer_at[i] != at)) {", "if (any) {", CORE,
     ("AcmpMailbox.C", "AcmpCore.A17")),
    ("X8-reentry-not-refused", C, "static bool enter(struct acmp *a)\n{\n\tif (a->in_port) {",
     "static bool enter(struct acmp *a)\n{\n\tif (a->in_port && a->draws == 0xFFFFFFFFu) {", CORE, ("AcmpCore.A23",)),
    # ---- the saved-state store (F1) ----
    ("S1-restore-without-discovery", C, "\t\tdisc_start(s);\n\t\ts->probing = ACMP_PROBING_PASSIVE;",
     "\t\ts->probing = ACMP_PROBING_PASSIVE;", ("acmp", "acmpnvm"), ("AcmpCore.A24", "AcmpStore.N1")),
    ("S2-restore-not-settled", C, "\t\ts->state = ACMP_PRB_W_AVAIL;\n\t}\n\tsink_settle(s);",
     "\t\ts->state = ACMP_PRB_W_AVAIL;\n\t}", ("acmp", "acmpnvm"), ("AcmpCore.A24", "AcmpStore.N1")),
    ("S3-flag-bits-swapped", C, "#define BIND_STARTED 0x02u\n#define BIND_STREAMING_WAIT 0x04u",
     "#define BIND_STARTED 0x04u\n#define BIND_STREAMING_WAIT 0x02u", ("acmp", "acmpnvm"),
     ("AcmpCore.A24", "AcmpStore.N")),
    ("S4-d3-rollback-drops-bindings", N, "\tstruct acmp_nvm *n = ctx;\n\tif (walk != NVM_W_BIND) {",
     "\tstruct acmp_nvm *n = ctx;\n\tacmp_restore_rollback(n->acmp);\n\tif (walk != NVM_W_BIND) {", ("acmpnvm",),
     ("AcmpStore.N6",)),
    ("S5-unbound-not-latched", C, "\trecord_of(&a->sinks[sink], payload);\n\treturn true;",
     "\trecord_of(&a->sinks[sink], payload);\n\treturn a->sinks[sink].bound;", ("acmp", "acmpnvm"),
     ("AcmpStore.N2", "AcmpCore.A24")),
    ("S6-controller-not-saved", C, "\t\twire_put_be(payload + 12, s->binding.controller_entity_id, 8);\n", "",
     ("acmp", "acmpnvm"), ("AcmpCore.A24", "AcmpStore.N1", "AcmpCore.A5")),
    ("S7-talker-uid-offset", C, "\t\twire_put_be(payload + 2, s->binding.talker_unique_id, 2);",
     "\t\twire_put_be(payload + 1, s->binding.talker_unique_id, 2);", ("acmp", "acmpnvm"),
     ("AcmpCore.A24", "AcmpStore.N1")),
    # ---- batch 2 (index 39 on) ----
    ("D3b-departing-skips-ifx", C, "if (!s->discovered || ifx != s->disc_interface_index) {",
     "(void)ifx;\n\tif (!s->discovered) {", CORE, ("AcmpCore.A22", "Table554/DiscoveryWalk.Graded")),
    ("L12-resp2-ignores-response", C, "if (s->state != ACMP_PRB_W_RESP && s->state != ACMP_PRB_W_RESP2) {",
     "if (s->state != ACMP_PRB_W_RESP) {", CORE, ("AcmpCore.A10", "AcmpCore.A8", "Table530/ListenerWalk.Graded")),
    ("L13-unbind-not-locked", C, "} else if (lock_refuses(a, cmd)) {",
     "} else if (cmd->msg == ACMP_MSG_BIND_RX_COMMAND && lock_refuses(a, cmd)) {", CORE, ("AcmpCore.A4Locked",)),
    ("L14-get-rx-no-fast-connect", C, "r.flags = (uint16_t)(ACMP_FLAG_FAST_CONNECT | (", "r.flags = (uint16_t)(0u | (",
     CORE, ("AcmpCore.A2GetRxStateInEveryState", "Table530/ListenerWalk.Graded")),
    ("L15-unknown-sink-off-by-one", C, "\tunsigned k = cmd->listener_uid;\n\tif (k >= a->cfg.n_sinks) {",
     "\tunsigned k = cmd->listener_uid;\n\tif (k > a->cfg.n_sinks) {", CORE, ("AcmpCore.A2Unknown", "ListenerScenario.LW2")),
    ("L16-owed-room-off-by-one", C, "\tif (a->owed_count < ACMP_OWED_MAX) {\n\t\treturn true;",
     "\tif (a->owed_count <= ACMP_OWED_MAX) {\n\t\treturn true;", CORE, ("AcmpCore.A19AFull",)),
    ("D9-gm-restart-keeps-no-adp", C, "\t\t\ts->adp_armed = false;                   // 2b: TK_NOT_DISCOVERED, no step 3\n", "",
     CORE, ("AcmpCore.A22", "Table554/DiscoveryWalk.Graded")),
    ("T6-unknown-source-off-by-one", C, "\tif (src >= a->cfg.n_sources) {", "\tif (src > a->cfg.n_sources) {", CORE,
     ("AcmpCore.A20", "TalkerWalk")),
    ("X10-poll-never-releases", C,
     "a->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed - ((o->release >> k) & 1u));",
     "a->sinks[k].change_owed = a->sinks[k].change_owed;", CORE, ("AcmpCore.A19", "AcmpMailbox.E1")),
    ("X11-tap-drops-discover", X, "\tm->adp_next.fn(m->adp_next.ctx, f);\n", "", ("acmp",), ("AcmpMailbox.B5",)),
    ("S8-longer-record-applied", C,
     "if (sink >= a->cfg.n_sinks || len != ACMP_BINDING_BYTES) {\n\t\treturn ACMP_RESTORE_REFUSED;",
     "if (sink >= a->cfg.n_sinks || len < ACMP_BINDING_BYTES) {\n\t\treturn ACMP_RESTORE_REFUSED;", ("acmp", "acmpnvm"),
     ("AcmpCore.A24Unbound", "AcmpStore.N6")),
    # ---- batch 3 (index 50 on): the millisecond clock's wrap (FR_NFR 3.4.2 "timer wrap") ----
    ("W1-due-unsigned-compare", C, "\treturn (int32_t)(deadline - at) <= 0;", "\treturn deadline <= at;", CORE,
     ("AcmpCore", "AcmpMailbox", "Table530", "Table554")),
    ("W2-earliest-unsigned-compare", C, "if (armed && (!*any || (int32_t)(deadline - *at) < 0)) {",
     "if (armed && (!*any || deadline < *at)) {", CORE, ("AcmpCore", "AcmpMailbox", "Table530", "Table554")),
)


def main() -> int:
    k, n = (int(x) for x in part.split("/"))
    first = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    pool = PROBES[first:]
    size = -(-len(pool) // n)
    table = pool[(k - 1) * size:k * size]
    arms = {"acmp": ctrl_arms.arm_acmp, "acmpwalk": ctrl_arms.arm_acmpwalk, "acmpnvm": ctrl_arms.arm_acmpnvm}
    root = scratch / f"probes-{first}-{k}"
    root.mkdir(parents=True, exist_ok=True)
    reuse = root / "reuse"
    cut_reuse(reuse)
    build = fw_gtest.Build()
    escaped = 0
    for name, path, old, new, use, expect in table:
        m = Mutant(name, path, old, new, use[0], "", "")
        try:
            src = plant(m, root)
        except Refusal as exc:
            print(f"[REFUSED] {name}: {exc}")
            escaped += 1
            continue
        tree = Tree(src, root / name / "build", reuse, build)
        fails: list[str] = []
        rcs = []
        for arm in use:
            try:
                out = arms[arm](tree)
            except Refusal as exc:
                out = Outcome(arm, 2, f"refused: {exc}")
            rcs.append(f"{arm}={out.rc}")
            fails += [f"{arm}: " + ln.strip() for ln in out.log.splitlines() if "[FAIL]" in ln]
            if out.rc == 2:
                fails.append(f"{arm}: REFUSED {out.log[:300]}")
        hit = [f for f in fails if any(f.split("[FAIL]", 1)[-1].strip().startswith(e) for e in expect)]
        ok = bool(hit)
        escaped += 0 if ok else 1
        print(f"[{'CAUGHT' if ok else 'ESCAPED'}] {name} ({' '.join(rcs)}): {len(fails)} [FAIL] line(s); "
              f"expected one of {', '.join(expect)}")
        for f in fails[:12]:
            print(f"    {f[:220]}")
        shutil.rmtree(root / name, ignore_errors=True)
    print(f"probes slice {k}/{n}: {len(table) - escaped} of {len(table)} caught by an expected test")
    return 0


if __name__ == "__main__":
    sys.exit(main())
