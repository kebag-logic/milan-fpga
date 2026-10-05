# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_mutants.py - the planted defects of the saved-state store's host suite.

Each mutant is one defect planted into a COPY of sw/firmware/ctrl_nvm (every
seam must match its file exactly once, so a line that moves breaks the
self-test rather than compiling unchanged), and names the checks that must
fail on it. A named check that stays green is a finding: the check cannot
fail for the defect it claims to detect. Every check of the suite is named by
at least one mutant, which `unnamed_checks` proves before any is planted.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from nvm_bench import TREE, Refusal

STORE = "nvm_store.c"
CODEC = "nvm_klj2.c"
LITESPI = "plat/nvm_flash_litespi.c"


@dataclass(frozen=True)
class Mutant:
    """One planted defect: its seams (file, exact text, replacement) and the
    checks that must fail on it."""

    name: str
    seams: tuple[tuple[str, str, str], ...]
    kills: tuple[str, ...]


def _m(name: str, path: str, old: str, new: str, *kills: str) -> Mutant:
    """A one-seam mutant."""
    return Mutant(name, ((path, old, new),), kills)


#: Time from the PHC, as the shipping writer reads it (milan_baremetal.c
#: gettime_ns), held at the last value on a backward step.
PHC_NOW = """static uint64_t ls_last_us;

static uint32_t ls_csr_read(unsigned int offset)
{
	return *(volatile uint32_t *)(MILAN_CSR_BASE + offset);
}

static void ls_csr_write(unsigned int offset, uint32_t value)
{
	*(volatile uint32_t *)(MILAN_CSR_BASE + offset) = value;
}

static uint64_t ls_now_us(void *ctx)
{
	uint32_t hi1;
	uint32_t hi2;
	uint32_t lo;
	uint64_t now;

	(void)ctx;
	ls_csr_write(0x520u, 0x4u);
	do {
		hi1 = ls_csr_read(0x534u);
		lo = ls_csr_read(0x530u);
		hi2 = ls_csr_read(0x534u);
	} while (hi1 != hi2);
	now = (((uint64_t)hi2 << 32) | lo) / 1000u;
	if (now < ls_last_us)
		return ls_last_us;
	ls_last_us = now;
	return now;
}"""
TIMER_NOW = """static uint64_t ls_now_us(void *ctx)
{
	uint32_t v;

	(void)ctx;
	timer0_update_value_write(1);
	v = timer0_value_read();
	/* the timer counts down; the difference is wrap-safe in 32 bits */
	ls_ticks += (uint32_t)(ls_tick_last - v);
	ls_tick_last = v;
	return ls_ticks / LS_TICKS_PER_US;
}"""
RESTAGE_SEQ = ("\treturn nvm_klj2_check(nvm_stage, NVM_IMG_LEN) == NVM_VD_OK &&\n"
               "\t       nvm_klj2_seq(nvm_stage) == seq;")
FAILED_READ_PASSES = "\t\tn = nvm_min(NVM_STEP_BYTES, NVM_IMG_LEN - nvm.pos);\n"

MUTANTS = (
    # ---- the boot path ----
    _m("no_crc_check", STORE, "\t\tvd = nvm_klj2_check(nvm_stage, img_len);",
       "\t\tvd = nvm_klj2_check_body(nvm_stage, img_len, img_len);",
       "torn_falls_back", "verdict_parity"),
    # the judgment and the re-stage share the codec's CRC test: only both
    # removed lets a torn container be applied
    Mutant("no_crc_anywhere",
           ((STORE, "\tif (~crc != nvm_rd32le(trailer))\n\t\treturn NVM_VD_CRC;\n", ""),
            (CODEC, "\tif (~crc != nvm_rd32le(img + img_len - NVM_KLJ2_TRAILER))\n\t\treturn NVM_VD_CRC;\n",
             "")),
           ("powercut",)),
    _m("pick_older", STORE, "(int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "(int32_t)(s->seq_a - s->seq_b) >= 0) ? 1 : 0;", "newer_wins"),
    _m("pick_no_wrap", STORE, "((int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "(s->seq_a >= s->seq_b) ? 0 : 1;", "newer_wins"),
    # section 7's pseudo-code read literally: B on equal sequences
    _m("tie_picks_b", STORE, "((int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "((int32_t)(s->seq_a - s->seq_b) > 0) ? 0 : 1;", "newer_wins"),
    _m("erased_header_only", CODEC,
       "\t\tif (!nvm_all_erased(p + NVM_REC_HDR, r.plen))\n\t\t\treturn NVM_VD_REC;\n", "",
       "verdict_parity"),
    _m("no_ascending", CODEC, "\tif ((int)p[3] <= last)\n\t\treturn NVM_VD_REC;\n", "",
       "verdict_parity"),
    _m("overrun_as_rec", CODEC,
       "\tif (pos + NVM_REC_HDR + plen > end)\n\t\treturn NVM_VD_LEN;\n\t/* A payload",
       "\tif (pos + NVM_REC_HDR + plen > end)\n\t\treturn NVM_VD_REC;\n\t/* A payload",
       "verdict_parity"),
    _m("incomplete_accepted", CODEC, "\tif (seen != NVM_N_REC)\n\t\treturn NVM_VD_INCOMPLETE;\n", "",
       "verdict_parity"),
    _m("no_version_check", CODEC,
       "\tif ((nvm_rd32le(hdr + 4) >> 16) != (NVM_KLJ2_FMT_VER >> 16))\n\t\treturn NVM_VD_VER;\n", "",
       "wrong_version_falls_back"),
    _m("no_blank_verdict", CODEC, "\tif (nvm_all_erased(hdr, NVM_KLJ2_HDR))\n\t\treturn NVM_VD_BLANK;\n",
       "", "blank_boot"),
    _m("pad_not_zero", CODEC, "\t\timg[NVM_KLJ2_HDR + NVM_AREA_RAW + i] = 0u;",
       "\t\timg[NVM_KLJ2_HDR + NVM_AREA_RAW + i] = NVM_ERASED;", "blank_boot"),
    _m("header_n_rec", CODEC, "\tnvm_wr32le(img + 12, NVM_N_REC);",
       "\tnvm_wr32le(img + 12, NVM_N_REC + 1u);", "blank_boot", "first_commit_bytes"),
    _m("frame_crc_init", CODEC, "\tcrc = nvm_crc16_update(0xffffu, rec, 6u);",
       "\tcrc = nvm_crc16_update(0x0000u, rec, 6u);", "vector_round_trip", "change_commit_bytes"),
    _m("no_blank_stage", STORE, "\tif (chosen == NVM_NONE)\n\t\tnvm_klj2_blank(nvm_stage);\n", "",
       "blank_boot"),
    _m("verdict_not_named", STORE,
       "\t\tnvm.st.last_verdict = (nvm.st.verdict_a != NVM_VD_BLANK) ?\n"
       "\t\t\t\t      nvm.st.verdict_a : nvm.st.verdict_b;",
       "\t\tnvm.st.last_verdict = NVM_VD_BLANK;", "both_torn_blank"),
    _m("stage_not_rechecked", STORE, RESTAGE_SEQ, "\t(void)seq;\n\treturn 1;", "read_flip_at_stage"),
    _m("stage_seq_unchecked", STORE, RESTAGE_SEQ,
       "\t(void)seq;\n\treturn nvm_klj2_check(nvm_stage, NVM_IMG_LEN) == NVM_VD_OK;",
       "read_alias_at_stage"),
    # the sequence taken from a read after the CRC passed, unchecked, and
    # never compared again
    Mutant("select_on_unchecked_reread",
           ((STORE, "\t\tif (vd == NVM_VD_OK)\n\t\t\t*seq = nvm_klj2_seq(nvm_stage);",
             "\t\tif (vd == NVM_VD_OK && !f->read(f->ctx, addr, nvm_stage, NVM_KLJ2_HDR))\n"
             "\t\t\t*seq = nvm_klj2_seq(nvm_stage);"),
            (STORE, RESTAGE_SEQ,
             "\t(void)seq;\n\treturn nvm_klj2_check(nvm_stage, NVM_IMG_LEN) == NVM_VD_OK;")),
           ("read_flip_boot",)),
    _m("slot_read_fail_ignored", STORE,
       "\t\tif (f->read(f->ctx, addr, nvm_stage, img_len))\n\t\t\treturn NVM_VD_LEN;\n",
       "\t\t(void)f->read(f->ctx, addr, nvm_stage, img_len);\n", "read_fail_boot"),
    _m("no_rollback", STORE,
       "\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_D3) != 0)\n\t\treturn NVM_T_CLOSED;\n"
       "\treturn NVM_T_DEFAULTS;", "\treturn NVM_T_DEFAULTS;",
       "apply_fault_rolls_back", "settle_fault_rolls_back"),
    _m("rollback_failure_ignored", STORE,
       "\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_D3) != 0)\n\t\treturn NVM_T_CLOSED;\n",
       "\t(void)nvm.state->rollback(nvm.state->ctx, NVM_W_D3);\n", "rollback_fault_closes"),
    _m("release_on_closed", STORE, "\tif (nvm.st.terminal == NVM_T_CLOSED)\n\t\treturn;\n", "",
       "rollback_fault_closes"),
    _m("fault_as_refusal", STORE, "\tif (res == NVM_FAULT)\n\t\treturn 1;\n", "",
       "apply_fault_rolls_back", "binding_walk"),
    _m("refusal_aborts", STORE, "\telse\n\t\tnvm.st.refused++;", "\telse\n\t\treturn 1;",
       "refused_keeps_default"),
    _m("settle_fault_ignored", STORE,
       "\t\t\tif (s->settle(s->ctx) == NVM_FAULT)\n\t\t\t\treturn nvm_abort(NVM_C_SETTLE);\n",
       "\t\t\t(void)s->settle(s->ctx);\n", "settle_fault_rolls_back"),
    _m("settle_after_names", STORE, "\t\tif (r.group == NVM_G_NAME && !settled) {",
       "\t\tif (0 && r.group == NVM_G_NAME && !settled) {", "golden_restore"),
    _m("release_before_apply", STORE, "\tstruct nvm_rec r;\n\tint settled = 0;\n",
       "\tstruct nvm_rec r;\n\tint settled = 0;\n\n\ts->release(s->ctx);\n", "golden_restore"),
    _m("apply_erased", STORE, "\tif (nvm_all_erased(rec, NVM_REC_HDR)) {", "\tif (0) {",
       "erased_records"),
    _m("model_ready_ignored", STORE, "\tif (!state->model_ready(state->ctx)) {", "\tif (0) {",
       "model_unproven_closes"),
    # ---- the two walks (D3 sections 8.1 and 8.6) ----
    _m("d3_rollback_takes_bindings", STORE,
       "\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_D3) != 0)",
       "\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_BIND) |\n"
       "\t    nvm.state->rollback(nvm.state->ctx, NVM_W_D3))",
       "apply_fault_rolls_back", "settle_fault_rolls_back"),
    # one walk: the bindings inside the D3 transaction
    Mutant("bindings_in_d3_walk",
           ((STORE, "\t\tif (r.group == NVM_G_BIND)\n\t\t\tcontinue;\n", ""),
            (STORE, "\t\tnvm.st.bind_terminal = nvm_walk_bind();",
             "\t\tnvm.st.bind_terminal = NVM_T_COMPLETE;")),
           ("binding_walk", "golden_restore")),
    _m("binding_fault_aborts_d3", STORE,
       "\t\tnvm.st.terminal = (nvm.st.bind_terminal == NVM_T_CLOSED) ?\n"
       "\t\t\t\t  NVM_T_CLOSED : nvm_walk_d3();",
       "\t\tnvm.st.terminal = (nvm.st.bind_terminal != NVM_T_COMPLETE) ?\n"
       "\t\t\t\t  nvm_abort(NVM_C_APPLY) : nvm_walk_d3();", "binding_walk"),
    _m("binding_fault_keeps_preloads", STORE,
       "\t\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_BIND) != 0)\n\t\t\treturn NVM_T_CLOSED;\n",
       "", "binding_walk"),
    # ---- DR2a ----
    _m("quiet_period", STORE, "\tif (!taken && !nvm.dirty_armed) {", "\tif (!taken) {", "debounce"),
    _m("no_debounce", STORE, "\t      nvm.now_us - nvm.dirty_since_us >= NVM_US(MILAN_NVM_DEBOUNCE_MS);",
       "\t      1;", "debounce"),
    # a change the running capture takes still arms the window
    _m("capture_leaves_window_armed", STORE, "\tif (!taken && !nvm.dirty_armed) {",
       "\tif (!nvm.dirty_armed) {", "debounce"),
    # ---- DR2b ----
    _m("dr2b_ignores_durability", STORE, "\t} else if (nvm.stage_durable && !nvm.force) {",
       "\t} else if (!nvm.force) {", "failed_commit_not_skipped"),
    _m("no_dr2b", STORE, "\t} else if (nvm.stage_durable && !nvm.force) {", "\t} else if (0) {",
       "unchanged_no_erase"),
    # ---- DR2c ----
    _m("no_backoff", STORE, "\tnvm.retry_at_us = nvm.now_us + NVM_US(NVM_TXN_BACKOFF_MS);",
       "\tnvm.retry_at_us = nvm.now_us;", "media_failures"),
    _m("unbounded_attempts", STORE, "\tif (nvm.st.attempts >= NVM_TXN_ATTEMPTS) {",
       "\tif (0) {", "media_failures"),
    # every change call opens a new budget, changed or not
    _m("budget_rearmed_by_change", STORE,
       "\tnvm.dirty[r.id >> 5] |= 1u << (r.id & 31u);\n\tif (!taken",
       "\tnvm.dirty[r.id >> 5] |= 1u << (r.id & 31u);\n\tnvm.st.attempts = 0;\n"
       "\tnvm.st.exhausted = 0;\n\tif (!taken", "dr2c_unchanged_set"),
    _m("budget_rearmed_by_capture", STORE, "\tif (nvm.stage_changed) {", "\tif (1) {",
       "dr2c_unchanged_set"),
    # the console bypasses the budget, or the backoff
    _m("commit_now_overrides_exhaustion", STORE, "\t} else if (nvm.st.exhausted) {",
       "\t} else if (nvm.st.exhausted && !nvm.force) {", "dr2c_console"),
    _m("commit_now_ignores_backoff", STORE,
       "\tif (nvm.retry_armed && nvm_now() < nvm.retry_at_us)\n\t\treturn 0;\n", "",
       "dr2c_console"),
    _m("success_forgives_exhaustion", STORE,
       "\tnvm.st.attempts = 0;\n\tnvm.st.last_verdict = NVM_VD_OK;",
       "\tnvm.st.attempts = 0;\n\tnvm.st.abandoned = 0;\n\tnvm.st.last_verdict = NVM_VD_OK;",
       "recovers_after_failure", "dr2c_unchanged_set"),
    _m("stale_kept", STORE, "\tif (!nvm_any(nvm.dirty))\n\t\tnvm.st.stale = 0;\n", "",
       "recovers_after_failure"),
    # ---- the write sequence ----
    _m("no_blankcheck", STORE, "\t\t\tnvm.st.phase = NVM_P_BLANKCHECK;",
       "\t\t\tnvm.st.phase = NVM_P_PROGRAM;", "media_failures"),
    _m("blankcheck_first_stretch_only", STORE,
       "\tnvm.pos += n;\n\tif (nvm.pos >= NVM_IMG_LEN) {\n\t\tnvm.pos = 0;",
       "\tnvm.pos = NVM_IMG_LEN;\n\tif (nvm.pos >= NVM_IMG_LEN) {\n\t\tnvm.pos = 0;",
       "blankcheck_tail"),
    _m("blankcheck_read_fail_ignored", STORE, "\tif (!n || !nvm_all_erased(nvm_chunk, n)) {",
       "\tif (!n)\n" + FAILED_READ_PASSES + "\telse if (!nvm_all_erased(nvm_chunk, n)) {",
       "media_verdicts"),
    _m("no_verify", STORE, "\t\tif (nvm_chunk[i] != nvm_stage[nvm.pos + i]) {", "\t\tif (0) {",
       "media_failures", "failed_commit_not_skipped"),
    _m("verify_skips_last_stretch", STORE,
       "\tnvm.pos += n;\n\tif (nvm.pos >= NVM_IMG_LEN)\n\t\tnvm_commit_done();",
       "\tnvm.pos += n;\n\tif (nvm.pos + NVM_STEP_BYTES >= NVM_IMG_LEN)\n\t\tnvm_commit_done();",
       "verify_tail"),
    _m("verify_read_fail_ignored", STORE,
       "\tif (!n) {\n\t\tnvm_fail(NVM_VD_VERIFY);\n\t\treturn;\n\t}\n\tfor (i = 0; i < n; ++i) {",
       "\tif (!n)\n" + FAILED_READ_PASSES + "\telse\n\tfor (i = 0; i < n; ++i) {",
       "media_verdicts"),
    _m("program_refusal_ignored", STORE,
       "\tif (f->program(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_stage + nvm.pos, n)) {\n"
       "\t\tnvm_fail(NVM_VD_PROGRAM);\n\t\treturn;\n\t}",
       "\t(void)f->program(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_stage + nvm.pos, n);",
       "media_verdicts"),
    _m("no_timeout", STORE,
       "\tif (busy < 0 || nvm.now_us - nvm.op_start_us > timeout_us)\n\t\tnvm_fail(vd);",
       "\tif (busy < 0)\n\t\tnvm_fail(vd);", "media_failures"),
    _m("same_sequence", STORE, "\tnvm.next_seq = nvm.st.seq + 1u;", "\tnvm.next_seq = nvm.st.seq;",
       "change_commit_bytes"),
    _m("refused_slot_overwritten", STORE,
       "\treturn nvm.st.verdict_a != NVM_VD_BLANK && nvm.st.verdict_b == NVM_VD_BLANK;",
       "\treturn 0;", "refused_slot_kept"),
    Mutant("erase_authoritative",
           ((STORE, "\t\treturn !nvm.st.auth;", "\t\treturn nvm.st.auth;"),
            (STORE, "\tif (nvm.target == nvm.st.auth || f->erase", "\tif (f->erase")),
           ("change_commit_bytes", "powercut")),
    Mutant("descending_pages",
           ((STORE, "\tuint32_t n = nvm_min(NVM_FLASH_PAGE, NVM_IMG_LEN - nvm.pos);\n\n"
                    "\tif (f->program(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_stage + nvm.pos, n)) {",
             "\tuint32_t at = ((NVM_IMG_LEN - 1u) / NVM_FLASH_PAGE) * NVM_FLASH_PAGE - nvm.pos;\n"
             "\tuint32_t n = nvm_min(NVM_FLASH_PAGE, NVM_IMG_LEN - at);\n\n"
             "\tif (f->program(f->ctx, nvm_slot_addr(nvm.target) + at, nvm_stage + at, n)) {"),
            (STORE, "\t\t\tnvm.pos += nvm.len;", "\t\t\tnvm.pos += NVM_FLASH_PAGE;")),
           ("first_commit_bytes",)),
    Mutant("capture_in_one_step",
           ((STORE, "\tnvm.cursor = nvm_rec_next(r);\n\tnvm.dirty[r.id >> 5] &= ~(1u << (r.id & 31u));\n"
                    "\tnvm.inflight[r.id >> 5] |= 1u << (r.id & 31u);\n\tnvm_latch(r);\n}",
             "\twhile (r.ok) {\n\t\tif (nvm_bit(nvm.dirty, r.id)) {\n"
             "\t\t\tnvm.dirty[r.id >> 5] &= ~(1u << (r.id & 31u));\n"
             "\t\t\tnvm.inflight[r.id >> 5] |= 1u << (r.id & 31u);\n\t\t\tnvm_latch(r);\n\t\t}\n"
             "\t\tr = nvm_rec_next(r);\n\t}\n\tnvm.cursor = r;\n}"),),
           ("service_bound",)),
    _m("spin_wait", STORE, "\tint busy = f->busy(f->ctx);\n\n\tif (busy == 0)\n\t\treturn 1;",
       "\tint busy = f->busy(f->ctx);\n\n\twhile (busy == 1 && nvm_now() - nvm.op_start_us <= timeout_us)\n"
       "\t\tbusy = f->busy(f->ctx);\n\tif (busy == 0)\n\t\treturn 1;", "service_bound"),
    # ---- the LiteSPI port ----
    _m("litespi_no_wren", LITESPI,
       "\tif (ls_window(&ls_wren, 1u, 0, 0u) || ls_window(cmd, 4u, src, len))",
       "\tif (ls_window(cmd, 4u, src, len))", "first_commit_bytes"),
    _m("litespi_status_ignored", LITESPI, "\treturn (status & LS_SR_WIP) ? 1 : 0;",
       "\t(void)status;\n\treturn 0;", "first_commit_bytes"),
    Mutant("litespi_no_guard",
           ((LITESPI, " ||\n\t    !ls_in_journal(addr, len))", ")"),
            (LITESPI, "\tif (!ls_in_journal(base, LS_BLOCK))\n\t\treturn -1;\n", "")),
           ("port_guard",)),
    # time from the PHC, held on a backward step
    _m("phc_time", LITESPI, TIMER_NOW, PHC_NOW, "time_base"),
    _m("clock_not_accumulated", LITESPI,
       "\tls_ticks += (uint32_t)(ls_tick_last - v);\n\tls_tick_last = v;\n"
       "\treturn ls_ticks / LS_TICKS_PER_US;",
       "\tls_tick_last = v;\n\treturn (0xffffffffu - v) / LS_TICKS_PER_US;", "time_base"),
    # a wait on the command master with no bound
    _m("xfer_unbounded", LITESPI, "\tfor (n = 0; n < LS_POLL_MAX; ++n)\n", "\tfor (n = 0;; ++n)\n",
       "port_stall"),
    _m("open_unbounded", LITESPI, "\t\tif (++n > LS_POLL_MAX)\n\t\t\treturn -1;\n", "", "port_stall"),
    _m("stall_ignored", LITESPI,
       "\tif (ls_window(&ls_wren, 1u, 0, 0u) || ls_window(cmd, 4u, src, len))\n\t\treturn -1;",
       "\t(void)ls_window(&ls_wren, 1u, 0, 0u);\n\t(void)ls_window(cmd, 4u, src, len);",
       "port_stall"),
)


def unnamed_checks(names: list[str]) -> list[str]:
    """Checks no mutant names: a check with no planted defect is unproven."""
    named = {k for m in MUTANTS for k in m.kills}
    return [n for n in names if n not in named]


def plant(m: Mutant, dest: Path) -> None:
    """Copy the store's tree to `dest` and plant `m` into the copy."""
    shutil.copytree(TREE, dest, ignore=shutil.ignore_patterns("__pycache__"))
    for rel, old, new in m.seams:
        path = dest / rel
        text = path.read_text()
        if text.count(old) != 1:
            raise Refusal(f"mutant {m.name}: seam found {text.count(old)} times in {rel}")
        path.write_text(text.replace(old, new))


def survivors(m: Mutant, grade: dict[str, list[str]]) -> list[str]:
    """The checks `m` names that its graded run left green."""
    return [k for k in m.kills if not grade.get(k)]
