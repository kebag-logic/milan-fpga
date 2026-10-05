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


MUTANTS = (
    _m("no_crc_check", STORE, "\tif (~crc != nvm_rd32le(trailer))\n\t\treturn NVM_VD_CRC;\n", "",
       "torn_falls_back", "verdict_parity"),
    # the slot is judged again in RAM before it is applied, with its own CRC
    # test, so a torn slot is refused there too: only both removed lets a
    # torn container be applied
    Mutant("no_crc_anywhere",
           ((STORE, "\tif (~crc != nvm_rd32le(trailer))\n\t\treturn NVM_VD_CRC;\n", ""),
            (CODEC, "\tif (~crc != nvm_rd32le(img + img_len - NVM_KLJ2_TRAILER))\n\t\treturn NVM_VD_CRC;\n",
             "")),
           ("powercut",)),
    _m("pick_older", STORE, "(int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "(int32_t)(s->seq_a - s->seq_b) >= 0) ? 1 : 0;", "newer_wins"),
    _m("pick_no_wrap", STORE, "((int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "(s->seq_a >= s->seq_b) ? 0 : 1;", "newer_wins"),
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
    _m("stage_not_rechecked", STORE,
       "\treturn nvm_klj2_check(nvm_stage, NVM_IMG_LEN) == NVM_VD_OK;", "\treturn 1;",
       "read_flip_at_stage"),
    _m("no_rollback", STORE,
       "\tif (nvm.state->rollback(nvm.state->ctx) != 0)\n\t\treturn NVM_T_CLOSED;\n"
       "\treturn NVM_T_DEFAULTS;", "\treturn NVM_T_DEFAULTS;",
       "apply_fault_rolls_back", "settle_fault_rolls_back"),
    _m("rollback_failure_ignored", STORE,
       "\tif (nvm.state->rollback(nvm.state->ctx) != 0)\n\t\treturn NVM_T_CLOSED;\n",
       "\t(void)nvm.state->rollback(nvm.state->ctx);\n", "rollback_fault_closes"),
    _m("release_on_closed", STORE, "\tif (nvm.st.terminal == NVM_T_CLOSED)\n\t\treturn;\n", "",
       "rollback_fault_closes"),
    _m("fault_as_refusal", STORE,
       "\t\t\tif (res == NVM_FAULT)\n\t\t\t\treturn nvm_abort(NVM_C_APPLY);\n", "",
       "apply_fault_rolls_back"),
    _m("refusal_aborts", STORE,
       "\t\t\telse\n\t\t\t\tnvm.st.refused++;",
       "\t\t\telse\n\t\t\t\treturn nvm_abort(NVM_C_APPLY);", "refused_keeps_default"),
    _m("settle_fault_ignored", STORE,
       "\t\t\tif (s->settle(s->ctx) == NVM_FAULT)\n\t\t\t\treturn nvm_abort(NVM_C_SETTLE);\n",
       "\t\t\t(void)s->settle(s->ctx);\n", "settle_fault_rolls_back"),
    _m("settle_after_names", STORE, "\t\tif (r.group == NVM_G_NAME && !settled) {",
       "\t\tif (0 && r.group == NVM_G_NAME && !settled) {", "golden_restore"),
    _m("release_before_apply", STORE,
       "\tstruct nvm_rec r = nvm_rec_first();\n\tint settled = 0;\n",
       "\tstruct nvm_rec r = nvm_rec_first();\n\tint settled = 0;\n\n\ts->release(s->ctx);\n",
       "golden_restore"),
    _m("apply_erased", STORE, "\t\tif (nvm_all_erased(rec, NVM_REC_HDR)) {", "\t\tif (0) {",
       "erased_records"),
    _m("model_ready_ignored", STORE, "\tif (!state->model_ready(state->ctx)) {", "\tif (0) {",
       "model_unproven_closes"),
    _m("quiet_period", STORE,
       "\tif (!nvm.dirty_armed) {\n\t\tnvm.dirty_armed = 1;\n\t\tnvm.dirty_since_us = nvm_now();\n"
       "\t}\n\t/* a new change",
       "\tnvm.dirty_armed = 1;\n\tnvm.dirty_since_us = nvm_now();\n\t/* a new change", "debounce"),
    _m("no_debounce", STORE,
       "\tif (now - nvm.dirty_since_us < NVM_US(MILAN_NVM_DEBOUNCE_MS))\n\t\treturn;\n", "",
       "debounce"),
    _m("dr2b_ignores_durability", STORE,
       "\tif (!nvm.stage_changed && nvm.stage_durable && !nvm.force) {",
       "\tif (!nvm.stage_changed && !nvm.force) {", "failed_commit_not_skipped"),
    _m("no_dr2b", STORE, "\tif (!nvm.stage_changed && nvm.stage_durable && !nvm.force) {",
       "\tif (0) {", "unchanged_no_erase"),
    _m("no_backoff", STORE, "\tnvm.retry_at_us = now + NVM_US(NVM_TXN_BACKOFF_MS);",
       "\tnvm.retry_at_us = now;", "media_failures"),
    _m("unbounded_attempts", STORE,
       "\tif (nvm.st.attempts >= NVM_TXN_ATTEMPTS)\n\t\tnvm.st.exhausted = 1;\n", "",
       "media_failures"),
    _m("no_blankcheck", STORE, "\t\t\tnvm.st.phase = NVM_P_BLANKCHECK;",
       "\t\t\tnvm.st.phase = NVM_P_PROGRAM;", "media_failures"),
    _m("no_verify", STORE, "\t\tif (nvm_chunk[i] != nvm_stage[nvm.pos + i]) {", "\t\tif (0) {",
       "media_failures", "failed_commit_not_skipped"),
    _m("no_timeout", STORE,
       "\tif (busy < 0 || nvm_now() - nvm.op_start_us > timeout_us)\n\t\tnvm_fail(vd);",
       "\tif (busy < 0)\n\t\tnvm_fail(vd);", "media_failures"),
    _m("attempts_kept", STORE,
       "\tnvm.st.attempts = 0;\n\tnvm.st.exhausted = 0;\n\tnvm_publish();", "\tnvm_publish();",
       "recovers_after_failure"),
    _m("stale_kept", STORE, "\tif (!nvm_any(nvm.dirty))\n\t\tnvm.st.stale = 0;\n", "",
       "recovers_after_failure"),
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
    _m("litespi_no_wren", LITESPI, "\tls_write_enable();\n\tls_command(LS_CMD_PP, addr);",
       "\tls_command(LS_CMD_PP, addr);", "first_commit_bytes"),
    _m("litespi_status_ignored", LITESPI, "\treturn (status & LS_SR_WIP) ? 1 : 0;",
       "\t(void)status;\n\treturn 0;", "first_commit_bytes"),
    Mutant("litespi_no_guard",
           ((LITESPI, " ||\n\t    !ls_in_journal(addr, len))", ")"),
            (LITESPI, "\tif (!ls_in_journal(base, LS_BLOCK))\n\t\treturn -1;\n", "")),
           ("port_guard",)),
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
