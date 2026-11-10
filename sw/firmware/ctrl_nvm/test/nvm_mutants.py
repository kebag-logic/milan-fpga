# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""nvm_mutants.py - the planted defects of the saved-state store's host suite.

Each mutant is one defect planted into a COPY of sw/firmware/ctrl_nvm (every
seam must match its file exactly once, so a line that moves breaks the
self-test rather than compiling unchanged), and names the checks that must
fail on it. A check is a GoogleTest test of that name (test_nvm_boot.cpp,
test_nvm_write.cpp, test_nvm_journal.cpp, test_nvm_vector.cpp,
test_nvm_more.cpp, test_nvm_codec.cpp, test_nvm_flashmock.cpp,
test_nvm_litespi.cpp, the two doctored shapes' test_nvm_shapes.cpp and the
bound shape's test_nvm_bound.cpp), on either port it runs on. A named
check whose test stays green is a finding: the test cannot fail for the
defect it claims to detect. Every check of the suite is named by at least one
mutant, which `unnamed_checks` proves before any is planted.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from nvm_bench import TREE, Refusal

import fw_gtest

STORE = "nvm_store.c"
CODEC = "nvm_klj2.c"
LITESPI = "plat/nvm_flash_litespi.c"


@dataclass(frozen=True)
class Mutant:
    """One planted defect: its seams (file, exact text, replacement), the
    checks that must fail on it, and the shape it is graded at when not the
    self-test's own (a defect that only shows at one clock)."""

    name: str
    seams: tuple[tuple[str, str, str], ...]
    kills: tuple[str, ...]
    shape: str = ""


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
TO_US = "\treturn ls_ticks / LS_HZ * 1000000u + ls_ticks % LS_HZ * 1000000u / LS_HZ;"
TIMER_NOW = """static uint64_t ls_now_us(void *ctx)
{
	uint32_t v;

	(void)ctx;
	v = ls_timer();
	/* the timer counts down; the difference is wrap-safe in 32 bits */
	ls_ticks += (uint32_t)(ls_tick_last - v);
	ls_tick_last = v;
	/* whole seconds, then the rest: fewer clocks than one second's, so
	 * times 10^6 it stays inside 64 bits */
""" + TO_US + "\n}"
CALL_TICKS = ("const uint32_t nvm_flash_litespi_call_ticks = "
              "(uint32_t)(LS_CALL_US * LS_HZ / 1000000u);")
RESTAGE_SEQ = ("\tif (nvm_klj2_check(nvm_stage, NVM_IMG_LEN) != NVM_VD_OK ||\n"
               "\t    nvm_klj2_seq(nvm_stage) != nvm.base_seq[slot])\n\t\treturn 0;")
RESTAGE_CRC = "\tif (nvm_klj2_check(nvm_stage, NVM_IMG_LEN) != NVM_VD_OK)\n\t\treturn 0;"
FAILED_READ_PASSES = "\t\tn = nvm_min(NVM_STEP_BYTES, NVM_IMG_LEN - nvm.pos);\n"
STANDS = "\t\tif (seen[n].vd == NVM_VD_OK || nvm_agrees(seen, n))"
SAME_BYTES = ("seen[j].vd == seen[n].vd && seen[j].digest == seen[n].digest &&\n"
              "\t\t    seen[j].bytes == seen[n].bytes")
#: A shape whose system clock is not a whole number of MHz.
ARTY = "endstation_arty_current"
BIND_WALK = "\t\tnvm.st.bind_terminal = nvm_walk_bind();"
BIND_CLOSED = "\tif (nvm.st.bind_terminal == NVM_T_CLOSED) {\n\t\tnvm.st.terminal = NVM_T_CLOSED;\n" \
              "\t\treturn;\n\t}\n"

MUTANTS = (
    # ---- the boot path ----
    _m("no_crc_check", STORE, "\t\tvd = nvm_klj2_check(nvm_stage, img_len);",
       "\t\tvd = nvm_klj2_check_body(nvm_stage, img_len, img_len);",
       "torn_falls_back", "verdict_parity"),
    # the judgment and the re-stage share the codec's CRC test: only both
    # removed lets a torn container be applied
    Mutant("no_crc_anywhere",
           ((STORE, "\tif (~crc != nvm_rd32le(trailer))\n\t\treturn NVM_VD_CRC;\n", ""),
            (CODEC, "\tif (~crc != nvm_rd32le(img + img_len - NVM_KLJ_TRAILER))\n\t\treturn NVM_VD_CRC;\n",
             "")),
           ("powercut",)),
    _m("pick_older", STORE, "(int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "(int32_t)(s->seq_a - s->seq_b) >= 0) ? 1 : 0;", "newer_wins"),
    _m("pick_no_wrap", STORE, "((int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "(s->seq_a >= s->seq_b) ? 0 : 1;", "newer_wins"),
    # B on equal sequences, the rule #665 decision 1 did not take
    _m("tie_picks_b", STORE, "((int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
       "((int32_t)(s->seq_a - s->seq_b) > 0) ? 0 : 1;", "newer_wins"),
    _m("erased_header_only", CODEC,
       "\t\tif (!nvm_all_erased(p + NVM_REC_HDR, r.plen))\n\t\t\treturn NVM_VD_REC;\n", "",
       "verdict_parity", "codec_parity"),
    _m("no_ascending", CODEC, "\tif ((int)id <= last)\n\t\treturn NVM_VD_REC;\n", "",
       "verdict_parity", "codec_parity"),
    _m("overrun_as_rec", CODEC,
       "\tif (pos + NVM_REC_HDR + plen > end)\n\t\treturn NVM_VD_LEN;\n\t/* A payload",
       "\tif (pos + NVM_REC_HDR + plen > end)\n\t\treturn NVM_VD_REC;\n\t/* A payload",
       "verdict_parity", "codec_parity"),
    _m("incomplete_accepted", CODEC, "\tif (seen != NVM_N_REC)\n\t\treturn NVM_VD_INCOMPLETE;\n", "",
       "verdict_parity", "codec_parity"),
    # ---- the codec asked directly: its room, a short loaded prefix, its lookups ----
    _m("erased_payload_end_bound", CODEC, "\t\tif (pos + NVM_REC_HDR + r.plen > loaded)\n",
       "\t\tif (pos + NVM_REC_HDR + r.plen > end)\n", "codec_erased_loaded_prefix"),
    _m("erased_payload_guard_early", CODEC, "\t\tif (pos + NVM_REC_HDR + r.plen > loaded)\n",
       "\t\tif (pos + NVM_REC_HDR + r.plen >= loaded)\n", "codec_erased_loaded_prefix"),
    _m("erased_payload_guard_late", CODEC, "\t\tif (pos + NVM_REC_HDR + r.plen > loaded)\n",
       "\t\tif (pos + NVM_REC_HDR + r.plen > loaded + 1u)\n", "codec_erased_loaded_prefix"),
    _m("room_unchecked", CODEC, "\tif (img_len > room)\n\t\treturn NVM_VD_LEN;\n", "", "codec_room"),
    # R507-1-F1: a prefix that ends before a record header, read on past
    # its end, or refused as a length fault
    _m("short_prefix_read_on", CODEC, "\t\tif (pos + NVM_REC_HDR > loaded)\n\t\t\treturn NVM_VD_REC;\n", "",
       "codec_loaded_prefix"),
    _m("short_prefix_as_len", CODEC, "\t\tif (pos + NVM_REC_HDR > loaded)\n\t\t\treturn NVM_VD_REC;\n",
       "\t\tif (pos + NVM_REC_HDR > loaded)\n\t\t\treturn NVM_VD_LEN;\n", "codec_loaded_prefix"),
    # R506-2-F1: the header's guard one byte off its exact end, either way,
    # and the payload's guard the same
    _m("header_guard_early", CODEC, "\t\tif (pos + NVM_REC_HDR > loaded)\n",
       "\t\tif (pos + NVM_REC_HDR >= loaded)\n", "codec_loaded_prefix"),
    _m("header_guard_late", CODEC, "\t\tif (pos + NVM_REC_HDR > loaded)\n",
       "\t\tif (pos + NVM_REC_HDR > loaded + 1u)\n", "codec_loaded_prefix"),
    _m("payload_guard_early", CODEC, "\tif (pos + NVM_REC_HDR + plen > loaded)\n",
       "\tif (pos + NVM_REC_HDR + plen >= loaded)\n", "codec_loaded_prefix"),
    _m("payload_guard_late", CODEC, "\tif (pos + NVM_REC_HDR + plen > loaded)\n",
       "\tif (pos + NVM_REC_HDR + plen > loaded + 1u)\n", "codec_loaded_prefix"),
    _m("lookup_index_unbounded", CODEC,
       "\tif (group >= NVM_G_COUNT || index >= nvm_blocks[group].count)\n\t\treturn r;",
       "\tif (group >= NVM_G_COUNT)\n\t\treturn r;", "codec_lookups"),
    # ---- a container longer than the stage ----
    _m("long_crc_unchecked", STORE, "\tif (~crc != nvm_rd32le(trailer))\n\t\treturn NVM_VD_CRC;\n", "",
       "long_container_reads"),
    _m("unread_not_counted", STORE, "\t\t\tnvm.st.read_faults++;\n\t\t\tcontinue;       /* the port",
       "\t\t\tcontinue;       /* the port",
       "long_container_reads"),
    _m("no_version_check", CODEC,
       "\tif ((nvm_rd32le(hdr + 4) >> 16) != (NVM_KLJ3_FMT_VER >> 16))\n\t\treturn NVM_VD_VER;\n", "",
       "wrong_version_falls_back"),
    # ---- #823 decision 2: KLJ2 is the previous format, refused VD_VER ----
    _m("klj2_not_recognised", CODEC, "\tif (nvm_rd32le(hdr) == NVM_KLJ2_MAGIC)\n\t\treturn NVM_VD_VER;\n", "",
       "klj2_in_slot_refused", "verdict_parity", "codec_parity"),
    Mutant("klj2_reinterpreted",
           ((CODEC, "\tif (nvm_rd32le(hdr) == NVM_KLJ2_MAGIC)\n\t\treturn NVM_VD_VER;\n", ""),
            (CODEC, "\tif (nvm_rd32le(hdr) != NVM_KLJ3_MAGIC)\n",
             "\tif (nvm_rd32le(hdr) != NVM_KLJ3_MAGIC && nvm_rd32le(hdr) != NVM_KLJ2_MAGIC)\n"),
            (CODEC, "\tif ((nvm_rd32le(hdr + 4) >> 16) != (NVM_KLJ3_FMT_VER >> 16))\n",
             "\tif ((nvm_rd32le(hdr + 4) >> 16) != (NVM_KLJ3_FMT_VER >> 16) &&\n"
             "\t    (nvm_rd32le(hdr + 4) >> 16) != 2u)\n")),
           ("klj2_in_slot_refused", "verdict_parity")),
    _m("legacy_not_read", STORE, "\tnvm_legacy_check();\n", "", "klj2_journal_refused"),
    _m("legacy_reason_dropped", STORE,
       "\t\tif (nvm.st.last_verdict == NVM_VD_BLANK && nvm.st.legacy)\n\t\t\tnvm.st.last_verdict = NVM_VD_VER;\n",
       "", "klj2_journal_refused"),
    # only a KLJ2 header is the previous format, and its reason replaces a
    # blank verdict only
    _m("legacy_any_nonblank_header", STORE, "\t\t    nvm_rd32le(nvm_chunk) == NVM_KLJ2_MAGIC)",
       "\t\t    !nvm_all_erased(nvm_chunk, NVM_KLJ_HDR))", "legacy_other_format_not_recorded"),
    _m("ver_overrides_own_refusal", STORE, "\t\tif (nvm.st.last_verdict == NVM_VD_BLANK && nvm.st.legacy)\n",
       "\t\tif (nvm.st.legacy)\n", "own_refusal_kept_over_legacy"),
    # today's slot B read at the end of today's journal: the user slot
    _m("legacy_b_wrong_place", "nvm_shape.h",
       "#define NVM_LEGACY_B       (MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE / 2u)",
       "#define NVM_LEGACY_B       (MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE)",
       "klj2_journal_at_its_flash_map_address"),
    _m("legacy_read_fault_recorded", STORE,
       "\t\tif (f->read(f->ctx, NVM_LEGACY_A + i * slot, nvm_chunk, NVM_KLJ_HDR) == 0 &&\n"
       "\t\t    nvm_rd32le(nvm_chunk) == NVM_KLJ2_MAGIC)",
       "\t\tif (f->read(f->ctx, NVM_LEGACY_A + i * slot, nvm_chunk, NVM_KLJ_HDR) != 0 ||\n"
       "\t\t    nvm_rd32le(nvm_chunk) == NVM_KLJ2_MAGIC)",
       "klj2_journal_unreadable"),
    _m("reserved_byte_ignored", CODEC, " || p[2] != NVM3_LAYOUT || p[3] != 0u)", " || p[2] != NVM3_LAYOUT)",
       "verdict_parity", "codec_parity"),
    # ---- #823 decision 1: the NAME block's first, last and one-past ids ----
    _m("name_base_moved", "nvm_layout3.h", "#define NVM3_ID_NAME (NVM3_ID_MAPO + NVM3_CAP_MAPO)",
       "#define NVM3_ID_NAME (NVM3_ID_MAPO + NVM3_CAP_MAPO + 1u)", "name_block_ends", "golden_restore"),
    _m("name_last_dropped", CODEC, "\twhile (g < NVM_G_COUNT && index >= nvm_blocks[g].count) {",
       "\twhile (g < NVM_G_COUNT && index + (g == NVM_G_NAME) >= nvm_blocks[g].count) {",
       "name_block_ends", "capacity_round_trip"),
    _m("id_space_unbounded", CODEC, "\tif (!r.ok || r.plen != plen)\n\t\treturn NVM_VD_REC;\n\t*out = r;",
       "\tif ((!r.ok && id < NVM_ID_SPACE) || (r.ok && r.plen != plen))\n\t\treturn NVM_VD_REC;\n\t*out = r;",
       "one_past_refused", "verdict_parity"),
    _m("no_blank_verdict", CODEC, "\tif (nvm_all_erased(hdr, NVM_KLJ_HDR))\n\t\treturn NVM_VD_BLANK;\n",
       "", "blank_boot"),
    _m("pad_not_zero", CODEC, "\t\timg[i] = 0u;", "\t\timg[i] = NVM_ERASED;", "blank_boot"),
    _m("header_n_rec", CODEC, "\tnvm_klj2_seg_header(img, seq, NVM_N_REC, NVM_IMG_LEN);",
       "\tnvm_klj2_seg_header(img, seq, NVM_N_REC + 1u, NVM_IMG_LEN);", "blank_boot", "first_commit_bytes"),
    _m("frame_crc_init", CODEC, "\tcrc = nvm_crc16_update(0xffffu, rec, NVM_REC_HDR - 2u);",
       "\tcrc = nvm_crc16_update(0x0000u, rec, NVM_REC_HDR - 2u);", "vector_round_trip", "change_commit_bytes"),
    _m("no_blank_stage", STORE, "\tif (chosen == NVM_NONE)\n\t\tnvm_klj2_blank(nvm_stage);\n", "",
       "blank_boot"),
    _m("verdict_not_named", STORE,
       "\t\tnvm.st.last_verdict = (nvm.st.verdict_a != NVM_VD_BLANK) ?\n"
       "\t\t\t\t      nvm.st.verdict_a : nvm.st.verdict_b;",
       "\t\tnvm.st.last_verdict = NVM_VD_BLANK;", "both_torn_blank"),
    _m("stage_not_rechecked", STORE, RESTAGE_SEQ, "", "read_flip_at_stage"),
    _m("stage_seq_unchecked", STORE, RESTAGE_SEQ, RESTAGE_CRC, "read_alias_at_stage"),
    # the sequence taken from a read after the CRC passed, unchecked, and
    # never compared again
    Mutant("select_on_unchecked_reread",
           ((STORE, "\t\tif (vd == NVM_VD_OK)\n\t\t\t*seq = nvm_klj2_seq(nvm_stage);",
             "\t\tif (vd == NVM_VD_OK &&\n"
             "\t\t    !nvm.flash->read(nvm.flash->ctx, addr, nvm_stage, NVM_KLJ_HDR))\n"
             "\t\t\t*seq = nvm_klj2_seq(nvm_stage);"),
            (STORE, RESTAGE_SEQ, RESTAGE_CRC)),
           ("read_flip_boot",)),
    _m("slot_read_fail_ignored", STORE,
       "\t\tif (nvm_take(rd, addr, nvm_stage, img_len))\n\t\t\treturn NVM_UNREAD;\n",
       "\t\t(void)nvm_take(rd, addr, nvm_stage, img_len);\n", "read_fail_boot"),
    # ---- #665 decision 2: a media read fault leaves the authority unknown ----
    # the round-2 store: an unread slot is merely refused and the next commit
    # restarts the sequence below it
    _m("unread_not_held", STORE, "\t\tnvm.st.phase = nvm.st.unread ? NVM_P_HELD : NVM_P_IDLE;",
       "\t\tnvm.st.phase = NVM_P_IDLE;", "authority_unknown", "fallback_restage",
       "read_disagreement"),
    _m("read_not_retried", STORE,
       "\t\t\tcontinue;       /* the port failed a read: read the slot again */",
       "\t\t\tbreak;", "read_fail_boot", "authority_unknown"),
    _m("refusal_unconfirmed", STORE, STANDS, "\t\tif (1)", "authority_unknown",
       "read_disagreement", "reads_differ_in_verdict", "reads_agree_in_digest_not_length"),
    _m("blank_unconfirmed", STORE, STANDS,
       "\t\tif (seen[n].vd == NVM_VD_OK || seen[n].vd == NVM_VD_BLANK || nvm_agrees(seen, n))",
       "authority_unknown"),
    # the round-3 store: two reads agree when their verdicts do, whatever
    # bytes they returned (R501-3)
    _m("refusal_by_verdict", STORE, SAME_BYTES, "seen[j].vd == seen[n].vd", "read_disagreement"),
    # the count left out of "the same bytes": a forged CRC-32 collision over
    # a shorter read agrees with the first
    _m("agreement_by_digest", STORE, SAME_BYTES, "seen[j].vd == seen[n].vd && seen[j].digest == seen[n].digest",
       "reads_agree_in_digest_not_length"),
    # reads that return other bytes than every earlier one are not counted
    # as media faults
    _m("disagreement_not_counted", STORE,
       "\t\tif (n)\n\t\t\tnvm.st.read_faults++;   /* other bytes than every earlier read */\n", "",
       "reads_differ_in_verdict", "reads_agree_in_digest_not_length"),
    _m("restage_not_retried", STORE,
       "\tfor (i = 0; i < NVM_READ_TRIES; ++i) {\n\t\tif (nvm_restage_once(slot, seq))",
       "\tfor (i = 0; i < 1u; ++i) {\n\t\tif (nvm_restage_once(slot, seq))",
       "read_flip_at_stage", "read_alias_at_stage", "read_fail_boot"),
    # the slot offered second is applied without its own re-stage
    _m("fallback_restage_unchecked", STORE,
       "\twhile (chosen != NVM_NONE && !nvm_stage_slot(chosen)) {",
       "\tif (chosen != NVM_NONE && !nvm_stage_slot(chosen)) {", "fallback_restage"),
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
    # a shape with no name record never settles (the doctored no-name shape)
    _m("no_settle_without_names", STORE,
       "\tif (!settled && s->settle(s->ctx) == NVM_FAULT)\n\t\treturn nvm_abort(NVM_C_SETTLE);\n", "",
       "settle_after_the_last_record"),
    # ---- DR3b at a doctored shape whose walk and sizes disagree ----
    _m("shape_not_checked", STORE, "\tshaped = nvm_shape_consistent();", "\tshaped = 1;",
       "shape_mismatch_disables_persistence"),
    _m("shape_mismatch_released_unproven", STORE, "\t} else if (nvm_model_proven()) {", "\t} else {",
       "shape_mismatch_disables_persistence"),
    _m("release_before_apply", STORE, "\tstruct nvm_rec r;\n\tint settled = 0;\n",
       "\tstruct nvm_rec r;\n\tint settled = 0;\n\n\ts->release(s->ctx);\n", "golden_restore"),
    _m("apply_erased", STORE, "\tif (nvm_all_erased(rec, NVM_REC_HDR)) {", "\tif (0) {",
       "erased_records"),
    _m("model_ready_ignored", STORE, "\tif (nvm.state->model_ready(nvm.state->ctx))\n\t\treturn 1;",
       "\tif (1)\n\t\treturn 1;", "model_unproven_closes"),
    # the round-2 order: the model check before the binding walk
    _m("bindings_skipped_unproven", STORE, BIND_WALK,
       "\t\tnvm.st.bind_terminal = nvm.state->model_ready(nvm.state->ctx) ?\n"
       "\t\t\t\t\t nvm_walk_bind() : NVM_T_NONE;", "model_unproven_closes"),
    # ---- the two walks (D3 sections 8.1 and 8.6) ----
    _m("d3_rollback_takes_bindings", STORE,
       "\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_D3) != 0)",
       "\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_BIND) |\n"
       "\t    nvm.state->rollback(nvm.state->ctx, NVM_W_D3))",
       "apply_fault_rolls_back", "settle_fault_rolls_back"),
    # one walk: the bindings inside the D3 transaction
    Mutant("bindings_in_d3_walk",
           ((STORE, "\t\tif (r.group == NVM_G_BIND)\n\t\t\tcontinue;\n", ""),
            (STORE, BIND_WALK, "\t\tnvm.st.bind_terminal = NVM_T_COMPLETE;")),
           ("binding_walk", "golden_restore")),
    _m("binding_fault_aborts_d3", STORE, BIND_CLOSED,
       BIND_CLOSED + "\tif (nvm.st.bind_terminal == NVM_T_DEFAULTS) {\n"
       "\t\tnvm.st.terminal = nvm_abort(NVM_C_APPLY);\n\t\treturn;\n\t}\n", "binding_walk"),
    _m("binding_fault_keeps_preloads", STORE,
       "\t\tif (nvm.state->rollback(nvm.state->ctx, NVM_W_BIND) != 0)\n\t\t\treturn NVM_T_CLOSED;\n",
       "", "binding_walk"),
    # ---- DR2a ----
    _m("quiet_period", STORE, "\tif (!taken && !nvm.dirty_armed) {", "\tif (!taken) {", "debounce"),
    _m("no_debounce", STORE, "\t      nvm.now_us - nvm.dirty_since_us >= NVM_US(NVM_WINDOW_MS);",
       "\t      1;", "debounce"),
    # a change the running capture takes still arms the window
    _m("capture_leaves_window_armed", STORE, "\tif (!taken && !nvm.dirty_armed) {",
       "\tif (!nvm.dirty_armed) {", "debounce"),
    # the record the capture examines next counted as passed
    _m("taken_off_by_one", STORE, "r.id >= nvm.cursor.id", "r.id > nvm.cursor.id", "debounce"),
    # every change during the capture counted as taken: one it has passed,
    # and one after its last latch, open no window and are never written
    _m("taken_while_capturing", STORE, "nvm.st.phase == NVM_P_CAPTURE && nvm.cursor.ok && r.id >= nvm.cursor.id;",
       "nvm.st.phase == NVM_P_CAPTURE;", "capture_window_edges"),
    _m("taken_after_last_latch", STORE, "nvm.cursor.ok && r.id >= nvm.cursor.id;", "r.id >= nvm.cursor.id;",
       "capture_window_edges"),
    # a change to a record the shape does not have marks one it does
    _m("change_of_no_record", STORE, "\tif (!r.ok || nvm.st.phase == NVM_P_OFF)\n\t\treturn;",
       "\tif (nvm.st.phase == NVM_P_OFF)\n\t\treturn;", "change_unknown_record"),
    # an owner with nothing to save has its stale payload framed
    _m("nothing_to_save_framed", STORE,
       "\tif (!s->latch(s->ctx, r.group, r.index, nvm_payload, r.plen))\n\t\treturn 0;",
       "\tif (!s->latch(s->ctx, r.group, r.index, nvm_payload, r.plen) && 0)\n\t\treturn 0;", "nothing_to_save"),
    # ---- DR2b ----
    # DR2b judged on the capture alone: a work set a failed attempt left in
    # flight, unchanged since, is skipped
    _m("dr2b_ignores_durability", STORE, "\tif (!nvm_any(&nvm.inflight)) {\n\t\tif (nvm.force)",
       "\tif (!nvm.stage_changed) {\n\t\tif (nvm.force)", "failed_commit_not_skipped"),
    _m("no_dr2b", STORE, "\tif (!nvm_any(&nvm.inflight)) {\n\t\tif (nvm.force)", "\tif (0) {\n\t\tif (nvm.force)",
       "unchanged_no_erase"),
    # the console's commit skipped like any other over a verified container
    _m("console_force_ignored", STORE, "\t\tif (nvm.force)\n\t\t\tnvm.force_cmp = 1;",
       "\t\tif (nvm.force && 0)\n\t\t\tnvm.force_cmp = 1;", "console_commit_unchanged", "compaction_bytes"),
    # ---- DR2c ----
    _m("no_backoff", STORE, "\tnvm.retry_at_us = nvm.now_us + NVM_US(NVM_TXN_BACKOFF_MS);",
       "\tnvm.retry_at_us = nvm.now_us;", "media_failures"),
    _m("unbounded_attempts", STORE, "\tif (nvm.st.attempts >= NVM_TXN_ATTEMPTS) {",
       "\tif (0) {", "media_failures"),
    # every change call opens a new budget, changed or not
    _m("budget_rearmed_by_change", STORE,
       "\tnvm_open_set(&nvm.dirty, r.id);\n\tif (!taken",
       "\tnvm_open_set(&nvm.dirty, r.id);\n\tnvm.st.attempts = 0;\n"
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
       "\tnvm.st.commits_ok++;\n\tnvm.st.last_verdict = NVM_VD_OK;",
       "\tnvm.st.commits_ok++;\n\tnvm.st.abandoned = 0;\n\tnvm.st.last_verdict = NVM_VD_OK;",
       "recovers_after_failure", "dr2c_unchanged_set"),
    _m("stale_kept", STORE, "\tif (!nvm_any(&nvm.dirty))\n\t\tnvm.st.stale = 0;\n", "",
       "recovers_after_failure"),
    # a DR2b suppression leaves the claim stale with nothing outside a slot
    _m("dr2b_keeps_stale", STORE, "\t\tnvm_heal();\n\t\tnvm_to_idle();\n\t\treturn;\n\t}\n\tif (!nvm_can_append()) {",
       "\t\tnvm_to_idle();\n\t\treturn;\n\t}\n\tif (!nvm_can_append()) {", "recovers_after_failure"),
    # ---- the write sequence: a page of a segment ----
    _m("no_verify", STORE, "\t\tif (nvm_chunk[i] != nvm_page[i]) {", "\t\tif (0) {",
       "media_failures", "failed_commit_not_skipped"),
    _m("verify_skips_last_page", STORE, "\tfor (i = 0; i < s->page; ++i) {\n\t\tif (nvm_chunk[i] != nvm_page[i]) {",
       "\tfor (i = 0; i < s->page && s->pos + s->page < s->len; ++i) {\n\t\tif (nvm_chunk[i] != nvm_page[i]) {",
       "verify_tail"),
    _m("verify_read_fail_ignored", STORE,
       "\tif (f->read(f->ctx, nvm_page_addr(s), nvm_chunk, s->page)) {\n\t\tnvm_fail(NVM_VD_VERIFY);\n"
       "\t\treturn;\n\t}",
       "\tif (f->read(f->ctx, nvm_page_addr(s), nvm_chunk, s->page))\n\t\tfor (i = 0; i < s->page; ++i)\n"
       "\t\t\tnvm_chunk[i] = nvm_page[i];", "media_verdicts"),
    _m("program_refusal_ignored", STORE,
       "\tif (f->program(f->ctx, nvm_page_addr(s), nvm_page, s->page)) {\n\t\tnvm_fail(NVM_VD_PROGRAM);\n"
       "\t\treturn;\n\t}", "\t(void)f->program(f->ctx, nvm_page_addr(s), nvm_page, s->page);", "media_verdicts"),
    _m("no_timeout", STORE,
       "\tif (busy < 0 || nvm.now_us - nvm.op_start_us > timeout_us)\n\t\tnvm_fail(vd);",
       "\tif (busy < 0)\n\t\tnvm_fail(vd);", "time_base"),
    _m("refused_slot_overwritten", STORE,
       "\treturn nvm.st.verdict_a != NVM_VD_BLANK && nvm.st.verdict_b == NVM_VD_BLANK;",
       "\treturn 0;", "refused_slot_kept"),
    # DR5 with neither slot blank: the first commit lands on slot B
    _m("no_blank_slot_takes_b", STORE,
       "\treturn nvm.st.verdict_a != NVM_VD_BLANK && nvm.st.verdict_b == NVM_VD_BLANK;",
       "\treturn nvm.st.verdict_a != NVM_VD_BLANK;", "first_commit_no_blank_slot"),
    # the authoritative slot prepared, erased and compacted into
    _m("erase_authoritative", STORE, "\t\treturn !nvm.st.auth;", "\t\treturn nvm.st.auth;",
       "change_commit_bytes", "powercut"),
    # a base's pages programmed from its last down
    _m("descending_pages", STORE, "\treturn nvm_slot_addr(s->slot) + s->at + s->pos;",
       "\treturn nvm_slot_addr(s->slot) + s->at +\n"
       "\t       (s->kind == NVM_K_BASE ? (NVM_PAGES(s->len) - 1u) * NVM_FLASH_PAGE - s->pos : s->pos);",
       "first_commit_bytes"),
    Mutant("capture_in_one_step",
           ((STORE, "\tnvm.cursor = nvm_rec_next(r);\n\tnvm_open_take(&nvm.dirty, r.id);\n"
                    "\tif (!nvm_latch(r))\n\t\treturn;\n\tnvm_open_set(&nvm.inflight, r.id);",
             "\twhile (r.ok) {\n\t\tif (nvm_bit(&nvm.dirty, r.id)) {\n"
             "\t\t\tnvm_open_take(&nvm.dirty, r.id);\n"
             "\t\t\tif (nvm_latch(r))\n\t\t\t\tnvm_open_set(&nvm.inflight, r.id);\n\t\t}\n"
             "\t\tr = nvm_rec_next(r);\n\t}\n\tnvm.cursor = r;\n\tif (0)\n\t\tnvm_open_set(&nvm.inflight, r.id);"),),
           ("service_bound",)),
    # a latched record's crc16 counted over the layout 2 header's six bytes
    _m("step_bytes_layout2", STORE, "\tnvm.step_bytes += (NVM_REC_HDR - 2u) + r.plen;",
       "\tnvm.step_bytes += 6u + r.plen;", "service_bound"),
    # ---- #823 decision 6: the open bits carry their count ----
    _m("open_count_doubled", STORE, "\tif (nvm_bit(v, id))\n\t\treturn;\n\tv->bit[id >> 5] |= 1u << (id & 31u);",
       "\tv->bit[id >> 5] |= 1u << (id & 31u);", "open_count"),
    _m("open_count_kept", STORE, "\tv->bit[id >> 5] &= ~(1u << (id & 31u));\n\tv->count--;",
       "\tv->bit[id >> 5] &= ~(1u << (id & 31u));", "open_count"),
    _m("spin_wait", STORE, "\tint busy = f->busy(f->ctx);\n\n\tif (busy == 0)\n\t\treturn 1;",
       "\tint busy = f->busy(f->ctx);\n\n\twhile (busy == 1 && nvm_now() - nvm.op_start_us <= timeout_us)\n"
       "\t\tbusy = f->busy(f->ctx);\n\tif (busy == 0)\n\t\treturn 1;", "service_bound"),
    # ---- the journal (#823 decision 3): the boot's replay of a slot's log ----
    # the log never replayed: the slot is its base alone
    _m("replay_skipped", STORE,
       "\tif (nvm_log_read(slot, nvm.base_seq[slot], 1, nvm.end_of[slot], &rd, &lg) != NVM_VD_OK)\n"
       "\t\treturn 0;\n\tnvm.st.deltas = lg.n;\n\treturn lg.seq == seq;",
       "\t(void)rd;\n\t(void)lg;\n\treturn 1;", "append_order", "change_commit_bytes"),
    # T7: the deltas applied out of order, the first one again last
    _m("deltas_applied_out_of_order", STORE,
       "\tif (vd == NVM_UNREAD)\n\t\treturn vd;\n\tlg->end = off;",
       "\tif (vd == NVM_UNREAD)\n\t\treturn vd;\n\tif (apply && lg->n > 1u) {\n\t\tuint32_t s0 = 0u;\n"
       "\t\tuint32_t l0 = 0u;\n\n\t\t(void)nvm_seg_read(slot, NVM_LOG_START, 1, rd, &s0, &l0);\n\t}\n\tlg->end = off;",
       "append_order"),
    # T8: a segment accepted without its CRC-32
    _m("delta_crc_unchecked", STORE, "\tif (~crc != nvm_rd32le(nvm_chunk + pad))\n\t\treturn NVM_VD_CRC;\n", "",
       "torn_delta"),
    _m("stale_delta_accepted", STORE, "\tif ((int32_t)(got - *seq) <= 0)\n\t\treturn NVM_VD_STALE;\n", "",
       "stale_delta"),
    # a replay past the end the log was judged to have reads a torn segment
    # into the stage
    _m("replay_past_judged_end", STORE,
       "\twhile (off + NVM_KLJ_HDR <= NVM_SLOT_BYTES && off < limit) {",
       "\twhile (off + NVM_KLJ_HDR <= NVM_SLOT_BYTES && limit) {", "torn_delta"),
    # one walk of the log stands, a misread one included
    _m("log_walk_unconfirmed", STORE, "\t\tif (nvm_agrees(seen, n)) {\n\t\t\t*lg = got[n];",
       "\t\tif (1) {\n\t\t\t*lg = got[n];", "replay_reads"),
    _m("log_read_fault_not_counted", STORE,
       "\t\t\tnvm.st.read_faults++;\n\t\t\tcontinue;\n\t\t}\n\t\tif (nvm_agrees(seen, n)) {",
       "\t\t\tcontinue;\n\t\t}\n\t\tif (nvm_agrees(seen, n)) {", "replay_read_faults"),
    # a walk that cannot be judged leaves the base standing alone
    _m("unjudged_log_kept", STORE, "\tif (!nvm_log_check(slot, &lg))\n\t\treturn nvm_unread(slot);",
       "\tif (!nvm_log_check(slot, &lg))\n\t\treturn vd;", "replay_reads"),
    # a replay whose sequence is not the one the slot was chosen by applied
    _m("replay_seq_unchecked", STORE, "\tnvm.st.deltas = lg.n;\n\treturn lg.seq == seq;",
       "\tnvm.st.deltas = lg.n;\n\t(void)seq;\n\treturn 1;", "replay_reads"),
    # each rule of a delta's records and words, broken alone. Two guards are
    # not planted: a record header past the segment's end, and a payload
    # past it. Each keeps the walk's reads inside the segment, and the record
    # rules and the pad rule refuse every delta either would, so no verdict
    # can tell a store without them.
    _m("delta_magic_unchecked", STORE,
       "\t\tif ((((uint32_t)hdr[0] << 8) | hdr[1]) != NVM_REC_MAGIC || hdr[2] != NVM3_LAYOUT",
       "\t\tif (hdr[2] != NVM3_LAYOUT", "delta_refusals"),
    _m("delta_crc16_unchecked", STORE,
       "\t\tif (c16 != ((((uint32_t)hdr[8]) << 8) | hdr[9]))\n\t\t\treturn NVM_VD_REC;\n", "", "delta_refusals"),
    _m("delta_layout_unchecked", STORE, " != NVM_REC_MAGIC || hdr[2] != NVM3_LAYOUT || hdr[3] != 0u ||",
       " != NVM_REC_MAGIC || hdr[3] != 0u ||", "delta_refusals"),
    _m("delta_reserved_unchecked", STORE, " || hdr[2] != NVM3_LAYOUT || hdr[3] != 0u ||\n",
       " || hdr[2] != NVM3_LAYOUT ||\n", "delta_refusals"),
    _m("delta_order_unchecked", STORE, "\t\t    (int)id <= last || !r.ok || r.plen != plen)",
       "\t\t    !r.ok || r.plen != plen)", "delta_refusals"),
    _m("delta_shape_unchecked", STORE, "\t\t    (int)id <= last || !r.ok || r.plen != plen)",
       "\t\t    (int)id <= last || (r.ok && r.plen < plen))", "delta_refusals"),
    _m("delta_pad_unchecked", STORE, "\tif (pos + pad != end)\n\t\treturn NVM_VD_LEN;\n", "", "delta_refusals"),
    # graded where a delta that closes can outgrow a segment: the 1x1 shape's
    # records all fit one
    Mutant("delta_cap_unchecked", ((CODEC, "\tif (img_len > NVM_SEG_MAX || img_len > room)",
                                    "\tif (img_len > room)"),), ("delta_refusals",), "endstation_ax7101_8x8"),
    _m("delta_room_unchecked", CODEC, "\tif (img_len > NVM_SEG_MAX || img_len > room)",
       "\tif (img_len > NVM_SEG_MAX)", "delta_refusals"),
    _m("delta_owner_unchecked", CODEC,
       "\tif (nvm_rd32le(hdr + 20) != MILAN_ENTITY_ID_LO || nvm_rd32le(hdr + 24) != MILAN_ENTITY_ID_HI)\n"
       "\t\treturn NVM_VD_ENT;\n\tif (nvm_rd32le(hdr + 28)", "\tif (nvm_rd32le(hdr + 28)", "delta_refusals"),
    _m("delta_model_unchecked", CODEC,
       "\tif (nvm_rd32le(hdr + 28) != MILAN_MODEL_ID_LO || nvm_rd32le(hdr + 32) != MILAN_MODEL_ID_HI)\n"
       "\t\treturn NVM_VD_SHAPE;\n\tif (nvm_rd32le(hdr + 36) != NVM3_LAYOUT)\n\t\treturn NVM_VD_REC;\n\t*len",
       "\tif (nvm_rd32le(hdr + 36) != NVM3_LAYOUT)\n\t\treturn NVM_VD_REC;\n\t*len", "delta_refusals"),
    _m("delta_layout_word_unchecked", CODEC,
       "\tif (nvm_rd32le(hdr + 36) != NVM3_LAYOUT)\n\t\treturn NVM_VD_REC;\n\t*len", "\t*len", "delta_refusals"),
    # ---- the journal: the append ----
    # a delta at the same sequence as the slot's last segment
    _m("same_sequence", STORE, "\ts->seq = nvm.st.seq + 1u;", "\ts->seq = nvm.st.seq;", "change_commit_bytes"),
    # nothing appends past a torn segment
    _m("torn_appends", STORE, "\treturn nvm.st.auth != NVM_NONE && !nvm.st.torn && !nvm.full;",
       "\treturn nvm.st.auth != NVM_NONE && !nvm.full;", "torn_delta", "media_failures"),
    # a delta failed before any page of it was programmed is torn as well
    _m("torn_without_program", STORE, "\t} else if (nvm.app.programmed) {\n\t\tnvm.st.torn = 1;",
       "\t} else {\n\t\tnvm.st.torn = 1;", "suspend_slow", "suspend_master_stall"),
    # A1: one segment holds the whole burst, past its cap
    Mutant("seg_cap_ignored",
           ((STORE, "\tuint32_t cap = nvm_min(NVM_SEG_MAX, NVM_SLOT_BYTES - nvm.st.log_end);",
             "\tuint32_t cap = nvm_min(NVM_SEG_MAX * 4u, NVM_SLOT_BYTES - nvm.st.log_end);"),),
           ("burst_deltas",), "endstation_ax7101_8x8"),
    # T12: a full log drops the save it cannot take
    _m("full_drops_save", STORE, "\tif (!s->n_rec) {\n\t\tnvm.full = 1;",
       "\tif (!s->n_rec) {\n\t\tnvm_open_clear(&nvm.inflight);\n\t\tnvm.full = 1;", "reserve_exhausted"),
    # decision 7: no deadline on an append, or a 300 ms one (T13)
    _m("append_deadline_ignored", STORE,
       "\tif (!nvm.in_append || nvm.now_us - nvm.due_us <= NVM_US(NVM_APPEND_TIMEOUT_MS))", "\tif (1)",
       "append_deadline"),
    _m("deadline_300ms", "nvm_store.h", "#define NVM_APPEND_TIMEOUT_MS 500u", "#define NVM_APPEND_TIMEOUT_MS 300u",
       "append_deadline", "commit_deadline"),
    # T11: the 1,000 ms firmware window DR2a ruled before decision 4
    _m("window_1000ms", "nvm_store.h", "#define NVM_WINDOW_MS 150u", "#define NVM_WINDOW_MS 1000u", "debounce",
       "save_bound"),
    # ---- the journal: compaction ----
    # a record a base's page cuts read from the stage at the next page
    _m("carry_dropped", STORE, "(at < nvm.front) ? nvm_carry[at - nvm.carry_at] : nvm_stage[at];",
       "(at < nvm.front) ? nvm_stage[at] : nvm_stage[at];", "compaction_carry"),
    # T9: the authority moved before the base closes, or before the old log
    # is copied behind it
    _m("move_before_base_closes", STORE, "\t\tif (s->pos < s->len) {\n\t\t\tnvm_to_idle();",
       "\t\tif (s->pos < NVM_FLASH_PAGE) {\n\t\t\tnvm_to_idle();", "torn_compaction", "compaction_bytes"),
    _m("move_before_copy", STORE, "\tif (nvm.st.auth != NVM_NONE && nvm.copy_from + s->pos < nvm.st.log_end) {",
       "\tif (0) {", "compaction_yields", "torn_compaction"),
    # the base sequenced above the old slot: the copied deltas are stale behind it
    _m("base_seq_above_old", STORE, "\ts->seq = nvm.st.seq + (nvm.st.auth == NVM_NONE ? 1u : 0u);",
       "\ts->seq = nvm.st.seq + 1u;", "compaction_yields", "compaction_bytes"),
    # a value only the base carries cleared over an old slot: a tie at boot
    # may take the old slot without it
    _m("inflight_cleared_at_move", STORE, "\tnvm.force_cmp = 0;\n\tif (old == NVM_NONE) {",
       "\tnvm.force_cmp = 0;\n\tif (1) {", "reserve_exhausted"),
    _m("behind_ignored", STORE, "\tif (nvm.st.compacting && NVM_KLJ_HDR + r.off < nvm.front)\n"
       "\t\tnvm_open_set(&nvm.behind, r.id);\n", "", "first_base_behind"),
    # rule 8: the reserve never asks for a compaction
    _m("reserve_ignored", STORE, "\treturn NVM_SLOT_BYTES - nvm.st.log_end < NVM_RESERVE;", "\treturn 0;",
       "compaction_reserve"),
    # rule 5: a compaction that never yields to a save
    _m("compaction_never_yields", STORE, "\t\tif (s->pos < s->len) {\n\t\t\tnvm_to_idle();\n\t\t\treturn;",
       "\t\tif (s->pos < s->len) {\n\t\t\tnvm.st.phase = NVM_P_ASSEMBLE;\n\t\t\treturn;", "compaction_yields"),
    _m("copy_read_fail_ignored", STORE,
       "\t\tif (f->read(f->ctx, nvm_slot_addr(nvm.st.auth) + nvm.copy_from + s->pos, nvm_page,\n"
       "\t\t\t    NVM_FLASH_PAGE)) {",
       "\t\tif (f->read(f->ctx, nvm_slot_addr(nvm.st.auth) + nvm.copy_from + s->pos, nvm_page,\n"
       "\t\t\t    NVM_FLASH_PAGE) && 0) {", "compaction_copy_read"),
    _m("failed_compaction_not_prepared", STORE, "\t\tnvm.st.compacting = 0;\n\t\tnvm_prep(nvm.cmp.slot);",
       "\t\tnvm.st.compacting = 0;\n\t\tnvm.st.bg = NVM_B_READY;", "compaction_failure_reprepares"),
    # a work set a compaction left in flight forgiven its attempts: the
    # store loops compacting
    _m("move_forgives_attempts", STORE, "\tif (nvm.cur == &nvm.app || !nvm_any(&nvm.inflight)) {",
       "\tif (1) {", "media_failures"),
    # ---- the journal: the background preparation and the erase suspend ----
    # the other slot taken as blank unread
    _m("prep_skips_check", STORE, "\tnvm.prep_erased = 0;\n\tnvm.st.bg = NVM_B_CHECK;\n}",
       "\tnvm.prep_erased = 0;\n\tnvm.st.bg = NVM_B_READY;\n}", "capacity_commit_over_stale"),
    _m("prep_first_block_only", STORE, "\tif (nvm.prep_pos == NVM_SLOT_BYTES) {",
       "\tif (nvm.prep_pos == NVM_ERASE_BLOCK) {", "blankcheck_tail"),
    _m("check_skips_pages", STORE, "\tnvm.prep_pos += NVM_STEP_BYTES;\n\tif (nvm.prep_pos % NVM_ERASE_BLOCK == 0u)",
       "\tnvm.prep_pos += 2u * NVM_STEP_BYTES;\n\tif (nvm.prep_pos % NVM_ERASE_BLOCK == 0u)", "blankcheck_tail"),
    _m("check_read_fail_ignored", STORE,
       "\tif (f->read(f->ctx, nvm_slot_addr(nvm.prep_slot) + nvm.prep_pos, nvm_chunk, NVM_STEP_BYTES)) {\n"
       "\t\tnvm_prep_fail(NVM_VD_ERASE);\n\t\treturn;\n\t}",
       "\t(void)f->read(f->ctx, nvm_slot_addr(nvm.prep_slot) + nvm.prep_pos, nvm_chunk, NVM_STEP_BYTES);",
       "media_verdicts"),
    # an erase that leaves the block written taken for erased
    _m("erased_twice_accepted", STORE, "\tif (nvm.prep_erased || f->erase(", "\tif (f->erase(", "prep_failures"),
    # the right count of erases, each of the slot's first block
    _m("erase_first_block_every_time", STORE, "\tnvm.prep_pos &= ~(NVM_ERASE_BLOCK - 1u);", "\tnvm.prep_pos = 0;",
       "capacity_commit_over_stale"),
    _m("prep_unbounded", STORE, "\tnvm.st.bg = (++nvm.prep_tries >= NVM_TXN_ATTEMPTS) ? NVM_B_FAILED : NVM_B_CHECK;",
       "\tnvm.st.bg = NVM_B_CHECK;", "prep_failures"),
    _m("prep_no_backoff", STORE, "\tnvm.prep_at_us = nvm.now_us + NVM_US(NVM_TXN_BACKOFF_MS);",
       "\tnvm.prep_at_us = nvm.now_us;", "prep_failures"),
    _m("erase_timeout_ignored", STORE,
       "\tif (busy < 0 || nvm.erase_run_us + (nvm.now_us - nvm.erase_from_us) > NVM_US(MILAN_NVM_ERASE_TIMEOUT_MS))",
       "\tif (busy < 0)", "time_base"),
    # the erase's deadline counts the time a save held it suspended
    Mutant("erase_deadline_counts_suspend",
           ((STORE, "\tnvm.erase_run_us += nvm.op_start_us - nvm.erase_from_us;\n", ""),
            (STORE, "\tnvm.suspended = 0;\n\tnvm.erase_from_us = nvm.now_us;\n", "\tnvm.suspended = 0;\n")),
           ("erase_time_excludes_suspend",)),
    # reads after a failed erase while the device is still busy
    _m("prep_reads_busy", STORE, "\tif (nvm.erasing) {\n\t\tif (f->busy(f->ctx) != 0)\n\t\t\treturn;\n"
       "\t\tnvm.erasing = 0;\n\t}\n\tif (f->read(", "\tif (f->read(", "prep_failures"),
    # a program left running by a failed one is not waited for
    _m("owed_not_waited", STORE, "\tif (nvm.suspended || nvm.owed) {", "\tif (nvm.suspended) {", "media_failures"),
    # a delta that fails while it holds the erase suspended leaves it so
    _m("failed_save_keeps_suspend", STORE, "\tif (nvm.suspended || nvm.owed) {", "\tif (nvm.owed) {",
       "erase_resumed_after_failure"),
    # decision 5: the save waits for the erase instead of suspending it
    _m("save_waits_for_erase", STORE,
       "\tif (nvm.erasing && !nvm.suspended) {\n\t\tnvm.st.phase = NVM_P_SUSPEND;\n\t\treturn;\n\t}",
       "\tif (nvm.erasing && !nvm.suspended) {\n\t\tif (f->busy(f->ctx) == 0)\n\t\t\tnvm.erasing = 0;\n"
       "\t\treturn;\n\t}", "erase_suspended"),
    _m("no_resume", STORE, "\t(void)nvm.flash->resume(nvm.flash->ctx);", "", "erase_suspended"),
    # A3: the slow suspend not counted, and the suspend not timed
    _m("slow_suspend_not_counted", STORE, "\tif (took > NVM_SUSPEND_ROOM_US)\n\t\tnvm.st.suspend_slow++;\n", "",
       "suspend_slow"),
    _m("suspend_untimed", STORE, "\tif (took > nvm.st.suspend_us_max)\n\t\tnvm.st.suspend_us_max = took;\n", "",
       "erase_suspended", "suspend_slow"),
    # a suspend not seen to take effect taken as never issued: one that
    # takes effect later is never resumed
    _m("late_suspend_kept", STORE, "\tif (nvm.st.phase == NVM_P_SUSPEND_WAIT)\n\t\tnvm.suspended = 1;\n", "",
       "suspend_slow"),
    # the erase found ended suspended all the same
    _m("ended_erase_suspended", STORE, "\tif (busy == 0) {\n\t\tnvm.erasing = 0;\n\t\tnvm.st.phase = NVM_P_PROGRAM;",
       "\tif (busy == 0 && 0) {\n\t\tnvm.erasing = 0;\n\t\tnvm.st.phase = NVM_P_PROGRAM;",
       "erase_ended_before_suspend"),
    _m("suspend_fault_ignored", STORE, "\tif (busy < 0 || f->suspend(f->ctx)) {\n\t\tnvm_fail(NVM_VD_ERASE);",
       "\tif (busy < 0 && f->suspend(f->ctx)) {\n\t\tnvm_fail(NVM_VD_ERASE);", "suspend_master_stall"),
    # the LiteSPI port's suspend sends nothing, or the wrong code
    _m("litespi_no_suspend", LITESPI, "\treturn ls_one(LS_CMD_PES);", "\treturn 0;", "erase_suspended"),
    _m("litespi_pes_wrong_code", LITESPI, "#define LS_CMD_PES  0x75u", "#define LS_CMD_PES  0xb0u",
       "erase_suspended"),
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
    # the guard admits today's journal, which this store must never write
    _m("litespi_guard_admits_klj2", LITESPI,
       "\treturn addr >= NVM_JOURNAL_OFFSET &&",
       "\treturn (addr >= MILAN_FLASH_JOURNAL_OFFSET && len <= MILAN_FLASH_JOURNAL_SIZE &&\n"
       "\t\taddr - MILAN_FLASH_JOURNAL_OFFSET <= MILAN_FLASH_JOURNAL_SIZE - len) ||\n"
       "\t       addr >= NVM_JOURNAL_OFFSET &&", "port_guard"),
    # time from the PHC, held on a backward step
    _m("phc_time", LITESPI, TIMER_NOW, PHC_NOW, "time_base"),
    _m("clock_not_accumulated", LITESPI,
       "\tls_ticks += (uint32_t)(ls_tick_last - v);\n\tls_tick_last = v;\n",
       "\tls_ticks = 0xffffffffu - v;\n\tls_tick_last = v;\n", "time_base"),
    # the round-3 port: a whole number of clocks per us, 83 at the Arty
    # shapes' 83.333 MHz, for the time base and the deadline (R500-3)
    Mutant("ticks_per_us_truncated",
           ((LITESPI, TO_US, "\treturn ls_ticks / (CONFIG_CLOCK_FREQUENCY / 1000000u);"),
            (LITESPI, CALL_TICKS, "const uint32_t nvm_flash_litespi_call_ticks = "
                                  "LS_CALL_US * (CONFIG_CLOCK_FREQUENCY / 1000000u);")),
           ("port_clock", "time_base"), ARTY),
    # a wait on the command master with no bound
    Mutant("xfer_unbounded",
           ((LITESPI, "\tfor (n = 0; n < LS_POLL_MAX; ++n) {", "\tfor (n = 0;; ++n) {"),
            (LITESPI, "\t\tif (ls_late())\n\t\t\treturn 0;\n", "")),
           ("port_stall",)),
    _m("open_unbounded", LITESPI, "\t\tif (++n > LS_POLL_MAX || ls_late())\n\t\t\treturn -1;\n", "",
       "port_stall"),
    # a call bounded per wait only: a master slow in every wait holds it
    _m("call_deadline_ignored", LITESPI,
       "\treturn (uint32_t)(ls_call_start - ls_timer()) > nvm_flash_litespi_call_ticks;",
       "\treturn 0;", "port_deadline", "port_drain_deadline"),
    # the drain bounded by its poll count alone
    _m("drain_deadline_ignored", LITESPI, "\t\tif (++n > LS_POLL_MAX || ls_late())\n\t\t\treturn -1;\n",
       "\t\tif (++n > LS_POLL_MAX)\n\t\t\treturn -1;\n", "port_drain_deadline"),
    # the port's own refusals, before the master is touched
    _m("read_runs_past_device", LITESPI, "\tif (addr >= SPIFLASH_SIZE || len > SPIFLASH_SIZE - addr)",
       "\tif (addr >= SPIFLASH_SIZE)", "port_read_range"),
    _m("program_across_page", LITESPI, " || (addr % LS_PAGE) + len > LS_PAGE ||", " ||",
       "port_write_refusals"),
    _m("deadline_per_wait", LITESPI, "\tuint32_t n;\n\n\tfor (n = 0; n < LS_POLL_MAX; ++n) {",
       "\tuint32_t n;\n\n\tls_call_begin();\n\tfor (n = 0; n < LS_POLL_MAX; ++n) {",
       "port_deadline"),
    _m("stall_ignored", LITESPI,
       "\tif (ls_window(&ls_wren, 1u, 0, 0u) || ls_window(cmd, 4u, src, len))\n\t\treturn -1;",
       "\t(void)ls_window(&ls_wren, 1u, 0, 0u);\n\t(void)ls_window(cmd, 4u, src, len);",
       "port_stall"),
)


def unnamed_checks(names: list[str]) -> list[str]:
    """Checks no mutant names: a check with no planted defect is unproven."""
    named = {k for m in MUTANTS for k in m.kills}
    return [n for n in names if n not in named]


def check_of(test: str) -> str:
    """The check a GoogleTest test is: Ports/NvmBoth.torn_falls_back/model
    and NvmModel.read_flip_boot are torn_falls_back and read_flip_boot."""
    return test.split(".", 1)[-1].split("/", 1)[0]


def listed_checks(listing: str) -> list[str]:
    """The checks a binary's --gtest_list_tests output names."""
    return sorted({ln.split()[0].split("/", 1)[0] for ln in listing.splitlines()
                   if re.match(r"^  [A-Za-z_]\w*(/\w+)?(\s|$)", ln)})


def plant(m: Mutant, dest: Path) -> None:
    """Copy the store's tree to `dest` and plant `m` into the copy."""
    shutil.copytree(TREE, dest, ignore=shutil.ignore_patterns("__pycache__"))
    for rel, old, new in m.seams:
        path = dest / rel
        text = path.read_text()
        if text.count(old) != 1:
            raise Refusal(f"mutant {m.name}: seam found {text.count(old)} times in {rel}")
        path.write_text(text.replace(old, new))


def survivors(m: Mutant, log: str) -> list[str]:
    """The checks `m` names whose test its graded run left green: no [FAIL]
    line names a test of that check, on either port."""
    failed = {check_of(test) for test in fw_gtest.failed_tests(log)}
    return [k for k in m.kills if k not in failed]
