#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run and grade the saved-state snapshot-ownership co-simulation.

This is the suite's runner. It builds the SHIPPING
``hdl/milan/KL_nvm_backend.sv`` and the SHIPPING
``sw/firmware/milan_baremetal/milan_baremetal.c`` -- the writer compiled for
the host, its two CSR primitives routed to the model, exactly as
``sw/firmware/nvm_hosttest`` routes them -- against the REAL donor producer
path at the pinned revision, and runs every EXECUTED case of section 9 of
``docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`` over them.

Three things it does that a plain Verilator suite does not:

* **The firmware is in the loop.** The writer's own boot, capture, seal,
  program and acknowledge sequence drives the RTL, so what is graded is the
  pair, not the module. `cosim_host.c` models the flash, the DDR window and
  the clock; every PP_NVM access reaches the Verilated backend.
* **Each case is graded by NAMED checks** over a dumped journal, decoded with
  the repository's own ``scripts/nvm_klj2.py`` and compared against records
  this file frames independently. `cosim_cases.cpp` is stimulus only.
* **Every mutant the page names is killed by its named check** (``mutate.py``),
  and the three historical defects are run RED against a pre-contract backend
  and writer to show the checks are not vacuous in either direction.

WHAT IT DOES NOT MODEL, stated plainly: CPU instruction time, DDR and bus
latency and arbitration, clock-domain crossings, the product's clock rate and
real flash timing. The backend clock is 1 MHz of MODEL time, so one cycle is
one microsecond and the deadlines, the hold and the heartbeat are counted in
it. See README.md.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import dataclasses
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STUBS = HERE / "stubs"
BUILD = HERE / "build"
RUNS = HERE / "runs"

PP = "protocol-processor/hdl"
#: the donor sources the model compiles: the binding record manager, the
#: device-face initiator, the AECP dynamic-state store and their package
DONOR_SV = [f"{PP}/acmp/pp_acmp_pkg.sv", f"{PP}/aecp/KL_aecp_dyn_state.sv",
            f"{PP}/acmp/KL_acmp_nvm_shadow.sv", f"{PP}/packet_engine/KL_pp_nvm_port.sv"]
BACKEND = "hdl/milan/KL_nvm_backend.sv"
WRITER = "sw/firmware/milan_baremetal/milan_baremetal.c"
SHAPES = {"1x1": "configs/endstation_ax7101_1x1_tdm8.yaml",
          "8x8": "configs/endstation_ax7101_8x8.yaml"}
#: `fence rw, rw` statements in the shipping writer: the capture, the window
#: load and the AEM image check. A writer from before the contract has one.
FENCES_CONTRACT, FENCES_LEGACY = 3, 1

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "sw" / "firmware" / "nvm_hosttest"))
import test_nvm_firmware as ref   # noqa: E402  (the repository's own host gate)
from cosim_oracle import CLK_HZ, Run, ShapeInfo, T_HOLD_MS   # noqa: E402
from cosim_case_map import (     # noqa: E402
    CHECKS, CONTRACT_ONLY, CORE_8X8, DEPENDENT, POWER_CYCLE, PROD_MUST_FAIL,
    grade)


def cmd(argv: list[str], log: Path, cwd: Path = ROOT) -> subprocess.CompletedProcess:
    """Run one build command, log it, and refuse on a non-zero exit.

    NO WALL CLOCK HERE. `scripts/run_all_suites.sh` already guards every suite
    with one `timeout` around the whole make, so a second, per-command
    deadline would only be a host-time judgement this suite has no business
    making -- and a build that is merely slow on a loaded box would read as a
    failure."""
    log.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(argv, cwd=cwd, text=True, capture_output=True,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    log.write_text(p.stdout + p.stderr)
    if p.returncode:
        raise SystemExit(f"FAILED ({p.returncode}): {' '.join(map(str, argv))}\n  see {log}")
    return p


# -------------------------------------------------------------------- shapes


def shape(name: str) -> ShapeInfo:
    """One shape, built from the repository's own generators: the record
    table from the record-space gate, the constants header and the expected
    payloads from the host gate, and the name bound from the generated RTL
    header, which must agree with the AEMI image's."""
    cfg = ROOT / SHAPES[name]
    work = BUILD / f"shape-{name}"
    work.mkdir(parents=True, exist_ok=True)
    names, dc, spi, spo = ref.build(cfg, work / "builder")
    shp = ref.Shape(cfg=cfg, names=names, dc=dc, spi=spi, spo=spo)
    donor = ref.Donor(base=ref.binding_base(), layout=ref.layout_version())
    overlay = json.loads((work / "builder" / cfg.stem / "aem_overlay.json").read_text())
    ident = ref.Ident(seq=0, entity_id=int(overlay["adp"]["entity_id"], 16),
                      model_id=int(overlay["entity"]["entity_model_id"], 16))
    table = work / "records.txt"
    cmd([sys.executable, "-B", "scripts/check_nvm_record_space.py", "--emit-record-table",
         str(cfg), "-o", str(table)], BUILD / "logs" / f"shape-{name}-record-table.log")
    recs, img_len = {}, 0
    for ln in table.read_text().splitlines():
        f = ln.split()
        if f and f[0] == "imglen":
            img_len = int(f[1])
        if f and f[0] == "rec":
            recs[int(f[1], 16)] = (int(f[2]), int(f[3]))
    svh = (ROOT / "configs/generated" / cfg.stem / "gen/adp_shape_defaults.svh").read_text()
    n_name = int(re.search(r"AEM_NAME_ENTRIES_C = (\d+);", svh).group(1))
    if n_name != names:
        raise SystemExit(f"shape {name}: the AEMI header says {names} names, the generated "
                         f"RTL header {n_name}")
    params = dict(N_STREAM_IN_P=dc["STREAM_INPUT"], N_STREAM_OUT_P=dc["STREAM_OUTPUT"],
                  N_SPORT_IN_P=dc["STREAM_PORT_INPUT"], N_SPORT_OUT_P=dc["STREAM_PORT_OUTPUT"],
                  N_AUDIO_UNIT_P=dc["AUDIO_UNIT"], N_CLK_DOM_P=dc["CLOCK_DOMAIN"],
                  N_NAME_P=names)
    return ShapeInfo(name, ref.constants_header(shp, donor, ident), table, params, donor,
                     ident, ref.expected_payloads(shp), img_len, recs)


def legacy_header(current: str) -> str:
    """The generator from BEFORE the contract, for the non-vacuity control:
    MILAN_NVM_LIVE_BASE, MILAN_NVM_STAGE_BASE and MILAN_NVM_CONTRACT are the
    contract-3 generator's (section 14), so a pre-contract writer is compiled
    against the constant it names, MILAN_NVM_IMAGE_BASE, and against nothing
    else this generator added."""
    out = []
    for ln in current.splitlines():
        if ln.startswith("#define MILAN_NVM_LIVE_BASE"):
            out.append(ln.replace("MILAN_NVM_LIVE_BASE", "MILAN_NVM_IMAGE_BASE"))
        elif ln.startswith(("#define MILAN_NVM_STAGE_BASE", "#define MILAN_NVM_CONTRACT")):
            continue
        else:
            out.append(ln)
    assert "MILAN_NVM_IMAGE_BASE" in "\n".join(out)
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ firmware
FW_SUBS = [
    ("static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn *milan_reg(offset);\n}",
     "static inline uint32_t milan_read(unsigned int offset)\n{\n\treturn nvm_host_csr_read(offset);\n}"),
    ("\t*milan_reg(offset) = value;\n\t__asm__ volatile(\"fence iorw, iorw\" ::: \"memory\");\n",
     "\tnvm_host_csr_write(offset, value);\n"),
]
FENCE_RW = "__asm__ volatile(\"fence rw, rw\" ::: \"memory\");"


def host_firmware(text: str, fences: int) -> str:
    """The host build of the writer: the two CSR access primitives route to
    the model and the remaining fences are blanked, the same adapter the
    repository's host gate applies -- COUNTED, so a seam that moves stops the
    build rather than silently compiling a different program."""
    for old, new in FW_SUBS:
        if text.count(old) != 1:
            raise SystemExit(f"firmware seam count {text.count(old)}: {old[:50]!r}")
        text = text.replace(old, new)
    if text.count(FENCE_RW) != fences:
        raise SystemExit(f"expected {fences} rw fences, found {text.count(FENCE_RW)}")
    return text.replace(FENCE_RW, "(void)0;")


#: the writer's file-scope state and its initial value: what a CPU-only reset
#: gives back (the C start-up zeroes .bss and reloads .data)
WRITER_STATICS = {"nvm_ready": "0", "nvm_retired": "0", "nvm_in_commit": "0", "nvm_seq": "0",
                  "nvm_auth_slot": "NVM_SLOT_NONE", "nvm_verdict_a": "0",
                  "nvm_verdict_b": "0", "nvm_last_verdict": "0", "nvm_commits_ok": "0",
                  "nvm_commits_failed": "0", "nvm_captures_refused": "0",
                  "nvm_acks_refused": "0", "nvm_hb_last": "0", "nvm_dirty_since": "0"}


def host_restart(text: str) -> str:
    """HOST MODEL ONLY, appended to the host build of the writer: a CPU-only
    reset, the writer's restart without a fabric reset. Refuses unless it
    names every file-scope variable of the writer, so a new one cannot
    survive the modelled reset unnoticed. NOTHING ELSE of a CPU reset is
    modelled -- not the boot code's memory initialisation, not the memory
    holding the live window, not the bus fabric -- so W1 to W4 ASSUME
    obligation O4 of the contract page and cannot test it."""
    found = set(re.findall(r"^static (?:int|uint32_t|uint64_t|unsigned int) (nvm_\w+)(?: = [^;(]+)?;$",
                           text, re.M))
    if found != set(WRITER_STATICS):
        raise SystemExit(f"writer statics {sorted(found)} != restart model {sorted(WRITER_STATICS)}")
    body = "".join(f"\t{k} = {v};\n" for k, v in WRITER_STATICS.items())
    return ("\n/* HOST MODEL ONLY, appended by run_cases.py: a CPU-only reset of the\n"
            " * writer. The fabric, the backend and the media keep their state; every\n"
            " * static of the writer returns to its initial value and the writer boots\n"
            " * again. */\n"
            "void nvm_host_writer_restart(void);\n"
            "void nvm_host_writer_restart(void)\n{\n" + body +
            "\tset_idle_hook(0);\n\tnvm_boot();\n}\n")


# -------------------------------------------------------------------- builds
@dataclasses.dataclass
class Build:
    name: str
    shape: str
    contract: bool = True       # the shipping backend and writer
    rtl_mut: str = ""           # a mutate.py mutation name
    fw_mut: str = ""
    glue_mut: str = ""
    cap_id_w: int = 16
    binary: Path | None = None
    #: where the PRE-CONTRACT sources live, on the control build alone
    legacy: Path | None = None


def mutate(kind: str, name: str, src: Path, dst: Path) -> None:
    """Write `src` to `dst` with the named defect planted in it."""
    cmd([sys.executable, "-B", str(HERE / "mutate.py"), kind, name, str(src), str(dst)],
        BUILD / "logs" / f"mutate-{name}.log", cwd=HERE)


def do_build(b: Build, shapes: dict[str, ShapeInfo], jobs: int) -> Build:
    """Build one co-simulation: the writer compiled for the host against the
    generator's constants, the backend (shipping, pre-contract or mutated),
    the wrapper and the donor, into one executable."""
    s = shapes[b.shape]
    work = BUILD / b.name
    if work.exists():
        shutil.rmtree(work)
    (work / "generated").mkdir(parents=True)
    (work / "generated" / "soc.h").write_text(
        s.header if b.contract else legacy_header(s.header))
    fw_src = ROOT / WRITER if b.contract else b.legacy / "milan_baremetal.c"
    fw_path = work / "writer.c"
    if b.fw_mut:
        mutate("fw", b.fw_mut, fw_src, fw_path)
    else:
        fw_path.write_text(Path(fw_src).read_text())
    host = host_firmware(fw_path.read_text(),
                         FENCES_CONTRACT if b.contract else FENCES_LEGACY)
    if b.contract:
        host += host_restart(fw_path.read_text())
    (work / "milan_baremetal.host.c").write_text(host)
    be_src = ROOT / BACKEND if b.contract else b.legacy / "KL_nvm_backend.sv"
    if b.rtl_mut:
        mutate("rtl", b.rtl_mut, be_src, work / "KL_nvm_backend.sv")
    else:
        (work / "KL_nvm_backend.sv").write_text(Path(be_src).read_text())
    if b.glue_mut:
        mutate("glue", b.glue_mut, HERE / "cosim_top.sv", work / "cosim_top.sv")
    else:
        (work / "cosim_top.sv").write_text((HERE / "cosim_top.sv").read_text())
    defs = [f"-DNVM_HOST_JOURNAL_OFFSET=0x{ref.JOURNAL:x}u",
            f"-DNVM_HOST_AEM_OFFSET=0x{ref.AEM_OFFSET:x}u",
            f"-DNVM_HOST_IMAGE_OFF=0x{ref.IMAGE_OFF:x}u"]
    cc = ["gcc", "-std=gnu11", "-O2", "-g", "-Wall", "-Wextra", "-Werror",
          f"-I{work}", f"-I{HERE}", f"-I{STUBS}"]
    cmd(cc + defs + ["-c", str(HERE / "cosim_host.c"), "-o", str(work / "host.o")],
        BUILD / "logs" / f"{b.name}-host.log")
    cmd(cc + ["-Wno-format", "-c", str(work / "milan_baremetal.host.c"),
              "-o", str(work / "fw.o")], BUILD / "logs" / f"{b.name}-fw.log")
    gparams = [f"-G{k}={v}" for k, v in s.params.items()] + [f"-GCLK_HZ_P={CLK_HZ}"]
    if b.contract:
        gparams += [f"-GT_HOLD_MS_P={T_HOLD_MS}", f"-GCAP_ID_W_P={b.cap_id_w}"]
    #! -Werror-USERERROR beside -Wno-fatal, never -Wno-fatal alone: the
    #! backend states its legal parameter ranges as elaboration $errors
    #! (KL_nvm_backend.sv, the g_refuse_* guards), and -Wno-fatal on its own
    #! demotes a $error to a warning nothing here reads, so a build outside
    #! a declared range would elaborate, simulate and be GRADED. Every -G
    #! this function passes is therefore checked by the module itself. The
    #! rule is docs/development/CODE_QUALITY.md, rule 6, "Where the contract
    #! is enforced, and where it is not".
    vl = ["verilator", "--cc", "--exe", "--build", "-j", str(jobs), "--top-module", "cosim_top",
          "--Mdir", str(work / "obj"), "-Wall", "-Wno-fatal", "-Werror-USERERROR",
          "-Wno-UNUSEDSIGNAL",
          "-Wno-UNUSEDPARAM", "--x-assign", "unique", "--x-initial", "unique"]
    if b.contract:
        vl.append("+define+NVM_CONTRACT_3")
    vl += gparams
    vl += ["-CFLAGS", f"-std=c++17 -O2 -I{HERE} -I{STUBS} {' '.join(defs)}",
           "-LDFLAGS", f"{work / 'host.o'} {work / 'fw.o'}"]
    vl += [str(ROOT / p) for p in DONOR_SV]
    vl += [str(work / "KL_nvm_backend.sv"), str(work / "cosim_top.sv"),
           str(HERE / "cosim_bridge.cpp"), str(HERE / "cosim_cases.cpp"), "-o", "cosim"]
    cmd(vl, BUILD / "logs" / f"{b.name}-verilator.log")
    b.binary = work / "obj" / "cosim"
    return b


# ------------------------------------------------------------------- running


def run_case(b: Build, shapes: dict[str, ShapeInfo], case: str, variant: str = "",
             extra: tuple = ()) -> Run:
    """Run one case on one build and collect what it printed: the named
    observations, the notes, the event trace and the writer's console."""
    s = shapes[b.shape]
    tag = case + (f"~{variant}" if variant else "")
    out = RUNS / b.name / tag
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    argv = [str(b.binary), "--case", case, "--out", str(out), "--records", str(s.records),
            *extra]
    p = subprocess.run(argv, text=True, capture_output=True)
    (out / "stdout.log").write_text(p.stdout)
    (out / "stderr.log").write_text(p.stderr)
    obs, notes, evts, fw, done, pending = {}, {}, [], [], False, False
    for ln in p.stdout.splitlines():
        if ln.startswith("OBS "):
            o = json.loads(ln[4:])
            obs[o["tag"]] = o
        elif ln.startswith("NOTE "):
            n = json.loads(ln[5:])
            notes[n["key"]] = n
        elif ln.startswith("EVT "):
            evts.append(json.loads(ln[4:]))
        elif ln.startswith("Milan NVM:"):
            fw.append(ln)
        elif ln.startswith("CASE_DONE"):
            done = True
            pending = ln.endswith("hooks_pending=1")
    return Run(case, b.name, variant, p.returncode, obs, notes, evts, fw,
               done, pending, out)



# -------------------------------------------------------------------- phases
#: Every mutant the contract page names, with the CHECK that must kill it.
#: A mutant whose named killer passes means that check is VACUOUS, and this
#: suite fails on it; a mutant that is killed only by some OTHER check is a
#: mutant aimed at the wrong place, and fails the same way.
MUTANTS = {
    # name: (which source, the case that runs it, its variant,
    #        and THE ONE CHECK the contract page names as its killer)
    'A01_composite_durable_bit':
        ('rtl', 'E1_dyn_change_ack_then_second_change', "", 'pending_drives_no_commit@end'),
    'F01_attestation_not_checked':
        ('fw', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'last_verified_kept@after:0x21'),
    'F02_copies_open_records':
        ('fw', 'B1_erase_error_full_span', "", 'last_verified_kept@end:0x20'),
    'F03_prefill_from_blank':
        ('fw', 'B1_erase_error_full_span', "", 'last_verified_kept@end:0x20'),
    'F04_ack_without_identity':
        ('fw', 'A1_stable_no_change', "", 'stable_no_churn'),
    'F05_device_busy_gate_kept':
        ('fw', 'B9_abandoned_write_stream', "", 'later_record_persists@abandoned:0x20'),
    'F06_ack_after_failed_slot':
        ('fw', 'F2_reported_flash_failure', "", 'converged@end'),
    'F07_reload_refusal_ignored':
        ('fw', 'R1_reload_after_failed_erase', "", 'converged@end'),
    'F08_restart_reloads_window':
        ('fw', 'W1_writer_restart_reattaches', "", 'converged@end'),
    'F10_retired_writer_keeps_heartbeating':
        ('fw', 'U9_four_window_loads_refused', "", 'writer_absent_when_retired@end'),
    'F11_restart_reattaches_without_load':
        ('fw', 'W2_restart_after_refused_loads', "", 'restart_stays_retired_without_load@restarted'),
    'F12_repeat_ignores_window_live':
        ('fw', 'U12_window_live_stops_the_repeat', "", 'window_live_stops_the_repeat@boot'),
    'G01_edge_detected_change':
        ('glue', 'E1_dyn_change_ack_then_second_change', "", 'no_durable_claim_unmaterialized@end'),
    'M01_open_at_erase_completion':
        ('rtl', 'B1_erase_error_full_span', "", 'last_verified_kept@end:0x20'),
    'M02_close_on_any_completion':
        ('rtl', 'C1g_real_port_copy_inside_erase_write_gap', "", 'never_torn_or_erased@after:0x21'),
    'M03_close_on_partial_write':
        ('rtl', 'B10_partial_write_never_closes', "", 'later_record_persists@end:0x21'),
    'M04_ack_ignores_identity':
        ('rtl', 'A6_late_ack_while_new_capture_open', "", 'stale_identity_refused@stray'),
    'M05_ack_retires_live_work':
        ('rtl', 'A2_write_between_verify_and_ack', "", 'ack_retires_only_slot@post_ack:0x20'),
    'M06_hold_does_not_defer':
        ('rtl', 'C1_request_during_hold_is_deferred', "", 'deferred_until_attestation:0x21'),
    'M07_hold_never_expires':
        ('rtl', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'hold_bounded:0x21'),
    'M08_attestation_ignores_grant':
        ('rtl', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'last_verified_kept@after:0x21'),
    'M09_second_arm_accepted':
        ('rtl', 'C5_concurrent_arm_refused', "", 'concurrent_arm_refused@stray'),
    'M10_release_forgets_work':
        ('rtl', 'C2_hold_expiry_then_erase_with_stale_mask', "", 'later_record_persists@after:0x20'),
    'M11_dirty_from_accepted_bytes':
        ('rtl', 'A12_last_byte_before_arm_done_after', "", 'converged@end'),
    'M12_alarm_not_revoking':
        ('rtl', 'B1_erase_error_full_span', "", 'alarm_revokes@end'),
    'M13_report_not_revoking':
        ('rtl', 'F2_reported_flash_failure', "", 'failure_revokes'),
    'M14_pending_bit_misses_producer':
        ('rtl', 'E1_dyn_change_ack_then_second_change', "", 'no_durable_claim_unmaterialized@end'),
    'M15_pending_bit_misses_open_record':
        ('rtl', 'B5_erase_then_no_write_yet', "", 'no_durable_claim@gap'),
    'M17_hold_expiry_voids_capture':
        ('rtl', 'C3_hold_expiry_without_producer', "", 'slow_copy_attests'),
    'M18_pending_bit_stuck':
        ('rtl', 'A1_stable_no_change', "", 'converged@end'),
    'M19_arm_edge_grant_not_deferred':
        ('rtl', 'U4_grant_request_on_arm_edge', "", 'arm_edge_request_deferred:0x20'),
    'M20_arm_accepted_while_request_deferred':
        ('rtl', 'U10_arm_refused_while_request_deferred', "", 'hold_bounded_across_captures:0x21'),
    'R01_reload_ignores_inflight':
        ('rtl', 'U5_reload_refused_inflight_at_rebase', "", 'reload_refused_inflight_at_rebase@after:0x20'),
    'R02_reload_ignores_grant_since_rebase':
        ('rtl', 'R1_reload_after_failed_erase', "", 'last_verified_kept@end:0x20'),
    'R03_reload_not_once_per_reset':
        ('rtl', 'U6_reload_refused_after_boot', "", 'held_work_survives_post_boot_reload@reload'),
    'R04_rebase_wins_over_same_edge_grant':
        ('rtl', 'U8_grant_on_rebase_edge', "", 'grant_wins_over_rebase_edge@after:0x20'),
    'R05_boot_load_stays_pending_when_live':
        ('rtl', 'U9_four_window_loads_refused', "", 'boot_load_closed_when_live@boot'),
    'R06_revision_b_load_rule':
        ('rtl+fw', 'W2_restart_after_refused_loads', "", 'change_landed_or_reported@end:0x21'),
    'R07_arm_without_accepted_load':
        ('rtl', 'U11_arm_refused_without_accepted_load', "", 'arm_refused_without_accepted_load@stray'),
}
#: ---- the identity WRAP arm (issue #484, round 2) --------------------------
#: The backend's capture identity is a PLAIN WRAPPING counter -- section 5.4
#: states the wrap and treats it as an ordinary event -- so one capture in
#: every 2**CAP_ID_W_P carries the identity 0. What is graded is that the
#: WIDTH changes nothing the writer reports: the capture whose identity is 0
#: is attested, acknowledged and never counted as refused.
#:
#: The narrow width is 2, the MINIMUM the backend's own elaboration contract
#: admits (KL_nvm_backend.sv, g_refuse_capid: CAP_ID_W_P in 2..16), and it is
#: the only narrow width built. A build outside that range is refused at
#: elaboration by -Werror-USERERROR in do_build(), so this arm cannot grade
#: the shipping module in a shape the module disclaims (#484 round 3, found
#: by review of round 2's own test arm).
#:
#: At 2 bits the identity is 0 on the FOURTH accepted arm, where the shipping
#: 16 bits would need 65,536 of them. Most of these cases commit two or three
#: times on their own, so each carries a COMMIT TAIL (`--commits`, run after
#: the case body and all of its observations) that takes it past the wrap.
#: The tail is applied identically to both members of a pair, so the identity
#: width remains the only thing that moves between the two runs. C2 reaches a
#: fourth capture unaided and is also the one case here with a capture the
#: backend genuinely does NOT attest, so the arm cannot be satisfied by a
#: writer that has simply stopped refusing.
WRAP_CASES = {
    "A4_write_after_ack": 3,
    "A9_updates_during_slow_erase": 3,
    "B1_erase_error_full_span": 3,
    "C8_ack_refused_after_verified_slot": 3,
    "C2_hold_expiry_then_erase_with_stale_mask": 0,
}
#: the narrow identity width this arm runs, and the ONLY narrow width built:
#: the minimum the backend's elaboration contract admits
WRAP_WIDTH = 2
#: the writer's own report of a run, compared field by field across widths
WRAP_FIELDS = ("acknowledged", "not attested", "commits ok=", "failed=",
               "captures refused=", "acks refused=")


def writer_report(r: Run) -> dict:
    """What the WRITER said about its captures in one run: how many
    acknowledgements it strobed and which identity each quoted, how many
    commits it deferred for an unattested capture, and the counters its own
    status line carries (`--status`, asked for after the case body).

    `stray == 0` is required, not incidental: a case may INJECT an
    acknowledgement at the device face, and one of those counted here would
    let the arm's "at least one acknowledgement quoted the identity 0" guard
    be satisfied by the harness rather than by the writer."""
    acks = [e["v"] >> 16 for e in r.evts
            if e["k"] == "strobe" and e["v"] & 0x2 and not e["stray"]]
    status = [ln for ln in (r.outdir / "stdout.log").read_text().splitlines()
              if "captures refused=" in ln]
    if not status:
        raise SystemExit(f"{r.case} on {r.build}: the writer printed no status line")
    rep = {"acknowledged": len(acks),
           "not attested": sum("not attested" in ln for ln in r.fw)}
    for field in WRAP_FIELDS[2:]:
        rep[field] = status[-1].split(field)[1].split()[0]
    rep["ids"] = acks
    return rep


def grade_wrap(builds: list[Build], shapes: dict[str, ShapeInfo],
               pool: int) -> int:
    """Every wrap case, at a narrow identity, against ITSELF at the shipping
    width. The identity width is the only thing that moves between the two
    runs, so every difference is the writer reading the identity's VALUE as
    an answer it does not carry."""
    rc, zeroes = 0, 0
    w = WRAP_WIDTH
    print("---- identity wrap: a capture whose identity is 0 is a capture -------")
    base = next(b for b in builds if b.name == "contract-1x1")
    b = next(x for x in builds if x.name == f"idw{w}-1x1")
    for case, tail in WRAP_CASES.items():
        #! the SAME tail on both members of the pair: the identity width must
        #! stay the only thing that differs between the two runs
        extra = ("--status",) + (("--commits", str(tail)) if tail else ())
        want = writer_report(run_case(base, shapes, case, "wrap", extra))
        got = writer_report(run_case(b, shapes, case, "wrap", extra))
        zeroes += got["ids"].count(0)
        bad = [f"{f}: {got[f]} (width {w}) against {want[f]} (width 16)"
               for f in WRAP_FIELDS if got[f] != want[f]]
        if bad:
            print(f"  SELF-TEST FAILED: {case} at CAP_ID_W_P={w} reports "
                  f"what it does not report at 16 -- {'; '.join(bad)}. "
                  f"Identities acknowledged: {got['ids']} against "
                  f"{want['ids']}.")
            rc = 1
        else:
            print(f"  {case} at CAP_ID_W_P={w} (+{tail} committing changes): "
                  f"identities {got['ids']}, "
                  f"{got['acknowledged']} acknowledged, "
                  f"{got['not attested']} deferred as unattested, "
                  f"captures refused={got['captures refused=']} -- the "
                  f"same report as at 16")
    #! and the arm is only worth anything if the wrap was REACHED: a case
    #! list that stopped short of the fourth capture would pass every
    #! comparison above without ever quoting the identity this is about
    if not zeroes:
        print("  SELF-TEST FAILED: no run acknowledged a capture whose "
              "identity is 0, so this arm never reached the wrap.")
        rc = 1
    else:
        print(f"  {zeroes} acknowledgement(s) quoted the capture identity 0")
    return rc


def one_shape_cases(shape: str, contract: bool) -> list[str]:
    """Which cases run at this shape on this kind of build."""
    if shape == "8x8":
        return list(CORE_8X8)
    cases = sorted(CHECKS)
    if not contract:
        cases = [c for c in cases if c not in CONTRACT_ONLY]
    return cases


def jobs_for(b: Build, shapes: dict[str, ShapeInfo]) -> list[tuple]:
    """The case runs this build owns, before its follow-ups."""
    out = []
    for case in one_shape_cases(b.shape, b.contract):
        if case in DEPENDENT:
            continue
        if case == "E3_binding_inside_manager_debounce":
            out += [(b, case, f"d1={d}", ("--d1", d)) for d in ("0", "1")]
        else:
            out.append((b, case, "", ()))
    return out


def run_build(b: Build, shapes: dict[str, ShapeInfo], pool: int,
              only: list[tuple] | None = None) -> list[Run]:
    """Run a build's cases, then the power-cycle and dependent follow-ups of
    whatever it ran -- each on the slots its parent case left."""
    jobsq = only if only is not None else jobs_for(b, shapes)
    with cf.ThreadPoolExecutor(max_workers=pool) as ex:
        runs = list(ex.map(lambda j: run_case(j[0], shapes, j[1], j[2], j[3]), jobsq))
    extra = [(b, "R_power_cycle", f"{r.case}@end",
              ("--slot-a", str(r.outdir / "end-slotA.bin"),
               "--slot-b", str(r.outdir / "end-slotB.bin")))
             for r in runs if r.case in POWER_CYCLE and "end" in r.obs]
    extra += [(b, dep, "",
               ("--slot-a", str(r.outdir / "end-slotA.bin"),
                "--slot-b", str(r.outdir / "end-slotB.bin")))
              for dep, parent in DEPENDENT.items() for r in runs
              if r.case == parent and "end" in r.obs
              and dep in one_shape_cases(b.shape, b.contract)]
    if extra:
        with cf.ThreadPoolExecutor(max_workers=pool) as ex:
            runs += list(ex.map(lambda j: run_case(j[0], shapes, j[1], j[2], j[3]), extra))
    return runs


def report(runs: list[Run], shapes: dict[str, ShapeInfo], label: str,
           expect_fail: dict, control: bool = False) -> tuple[int, int, int]:
    """Print every graded check of a build and count what it did.

    On the CONTROL build -- a backend and a writer from before the contract --
    a failing check is the point: it is the defect the contract answers,
    reproduced on the source it was reported against. Those are printed as
    REPRODUCED and do not fail the suite; what fails the suite there is a
    check of PROD_MUST_FAIL that does NOT go red, which main() tests."""
    npass = nfail = nna = 0
    for r in sorted(runs, key=lambda x: (x.case, x.variant)):
        s = shapes[next(b.shape for b in ALL_BUILDS if b.name == r.build)]
        for name, (verdict, detail) in grade(r, s).items():
            key = (r.case, r.variant, name)
            if key in expect_fail:
                if verdict == "fail":
                    print(f"  EXPECTED-FAIL {label} {r.case}{'~' + r.variant if r.variant else ''} "
                          f": {name} -- {expect_fail[key]}")
                    npass += 1
                    continue
                #! ... and the label must not OUTLIVE the limitation. A check
                #! this suite says cannot pass here, passing, means the
                #! limitation is gone or the case stopped reaching it; either
                #! way the expectation is stale and the suite says so rather
                #! than counting the run green and keeping the label
                print(f"  UNEXPECTED-PASS {label} "
                      f"{r.case}{'~' + r.variant if r.variant else ''} "
                      f": {name} reads {verdict}, and it is labelled as a "
                      f"known failure -- retire the label ({expect_fail[key]})")
                nfail += 1
                continue
            if verdict == "fail":
                print(f"  {'REPRODUCED' if control else 'FAIL'} {label} "
                      f"{r.case}{'~' + r.variant if r.variant else ''} "
                      f": {name} -- {detail}")
                nfail += 1
            elif verdict == "n/a":
                nna += 1
            else:
                npass += 1
    return npass, nfail, nna


ALL_BUILDS: list[Build] = []


def plan(a: argparse.Namespace, want: list[str]) -> list[Build]:
    """Every build this invocation needs: the shipping ones, the identity
    control, the pre-contract control when one was asked for, and one per
    mutant."""
    builds = [Build(f"contract-{n}", n) for n in want]
    if "1x1" in want:
        # ONE narrow identity build, which two arms share: a 2-bit identity
        # MUST alias, which is what shows the 16-bit one is doing work (A8),
        # and it wraps inside a case, which is what grade_wrap() grades. Two
        # bits is the MINIMUM the backend's elaboration contract admits, and
        # a build outside 2..16 is refused by do_build()'s -Werror-USERERROR
        # rather than graded.
        builds.append(Build(f"idw{WRAP_WIDTH}-1x1", "1x1", cap_id_w=WRAP_WIDTH))
    if a.legacy_dir:
        builds.append(Build("legacy-1x1", "1x1", contract=False,
                            legacy=Path(a.legacy_dir).resolve()))
    if not a.skip_mutants and not a.wrap_only:
        for name, (kind, _case, _variant, _check) in MUTANTS.items():
            kw = {f"{k}_mut": name for k in kind.split("+")}
            builds.append(Build(f"mut-{name}", "1x1", **kw))
    return builds


def grade_builds(builds: list[Build], shapes: dict[str, ShapeInfo],
                 pool: int) -> tuple[int, list[int]]:
    """Run and report every build that is not a control: the shipping ones,
    and the pre-contract one, whose failures ARE the evidence."""
    rc, totals = 0, [0, 0, 0]
    for b in builds:
        if b.name.startswith(("mut-", "idw")):
            continue
        expect = {}
        if b.contract:
            expect = {("E3_binding_inside_manager_debounce", "d1=0",
                       "no_durable_claim@in_debounce"):
                      "KNOWN LIMITATION: without donor scope D1 (filed as "
                      "protocol-processor-control-plane-avb-milan issue 90) "
                      "the parent cannot see a binding the manager is "
                      "debouncing"}
        runs = run_build(b, shapes, pool)
        p, f, n = report(runs, shapes, b.name, expect, control=not b.contract)
        if b.contract:
            totals = [totals[0] + p, totals[1] + f, totals[2] + n]
            #! NOT in a shape scripts/suite_tally.py counts: only the ONE
            #! closing line of main() is the suite's tally, or the per-build
            #! lines would be added to it and the sweep would quote a number
            #! two and a half times the checks this suite ran
            print(f"[{b.name}] {len(runs)} case run(s): {p} ok, {f} bad, "
                  f"{n} not expressible")
            rc = rc or (1 if f else 0)
            continue
        print(f"[{b.name}] the pre-contract source reproduces {f} failing "
              f"check(s) over {len(runs)} case run(s); {p} ok and {n} not "
              f"expressible there (it has no arm, attestation or identity)")
        # the non-vacuity control, in the direction a mutant cannot give: the
        # three historical defects MUST reproduce on a pre-contract source
        graded = {(r.case, k): v for r in runs
                  for k, v in grade(r, shapes[b.shape]).items()}
        for case, check, why in PROD_MUST_FAIL:
            got = graded.get((case, check), ("absent", ""))[0]
            if got != "fail":
                print(f"  SELF-TEST FAILED: {case} : {check} reads {got} on "
                      f"the pre-contract source; it must FAIL there ({why}).")
                rc = 1
            else:
                print(f"  non-vacuity control: {case} : {check} RED as "
                      f"required -- {why}")
    return rc, totals


def grade_mutants(builds: list[Build], shapes: dict[str, ShapeInfo],
                  pool: int) -> int:
    """Every mutant, against the ONE check the contract page names for it. A
    mutant killed only by some other check is a mutant aimed at the wrong
    place, and fails here the same way a surviving one does."""
    rc, killed = 0, 0
    print("---- mutants: each MUST be killed by its NAMED check -----------------")
    for name, (_kind, case, variant, check) in MUTANTS.items():
        b = next(x for x in builds if x.name == f"mut-{name}")
        extra = ("--d1", variant.split("=")[1]) if variant.startswith("d1=") else ()
        todo = [(b, case, variant, extra)]
        if case in DEPENDENT:
            runs = run_build(b, shapes, pool,
                             only=[(b, DEPENDENT[case], "", ())])
            todo = [(b, case, variant,
                     ("--slot-a", str(runs[0].outdir / "end-slotA.bin"),
                      "--slot-b", str(runs[0].outdir / "end-slotB.bin")) + extra)]
        runs = run_build(b, shapes, pool, only=todo)
        #! run_build also runs the power-cycle and dependent follow-ups of
        #! whatever it ran, so the killer's own run is selected by NAME, never
        #! by position: taking the last would grade a follow-up and report
        #! every such mutant as surviving a check that never ran
        target = next(r for r in runs if r.case == case)
        got = grade(target, shapes["1x1"]).get(
            check, ("absent", "the named check did not run"))
        if got[0] == "fail":
            killed += 1
            print(f"  {name}: killed by {check} -- {got[1]}")
        else:
            print(f"  SELF-TEST FAILED: {name} survives its named check "
                  f"{check} ({got[0]}: {got[1]}). That check is vacuous.")
            rc = 1
    print(f"{killed} of {len(MUTANTS)} mutant(s) killed by their named check")
    return rc


def main() -> int:
    """Build, run, grade and report; non-zero on any failing check."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--shapes", default="1x1,8x8")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--pool", type=int, default=8)
    ap.add_argument("--skip-mutants", action="store_true",
                    help="grade the shipping builds only (a fast local loop)")
    ap.add_argument("--wrap-only", action="store_true",
                    help="the identity-wrap arm alone: the narrow-identity "
                         "build and the cases that reach the wrap")
    ap.add_argument("--legacy-dir", default="",
                    help="a directory holding KL_nvm_backend.sv and milan_baremetal.c from "
                         "BEFORE the contract; with it the suite also runs the non-vacuity "
                         "control that must reproduce the three historical defects")
    a = ap.parse_args()
    want = [s.strip() for s in a.shapes.split(",") if s.strip()]
    shapes = {n: shape(n) for n in want}
    builds = plan(a, want)
    ALL_BUILDS.extend(builds)

    print(f"building {len(builds)} build(s)")
    with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs // 2)) as ex:
        list(ex.map(lambda b: do_build(b, shapes, 2), builds))

    rc, totals = (0, [0, 0, 0]) if a.wrap_only else \
        grade_builds(builds, shapes, a.pool)

    if "1x1" in want and (a.wrap_only or not a.skip_mutants):
        rc = grade_wrap(builds, shapes, a.pool) or rc

    if "1x1" in want and not a.skip_mutants and not a.wrap_only:
        b = next(x for x in builds if x.name == f"idw{WRAP_WIDTH}-1x1")
        runs = run_build(b, shapes, a.pool,
                         only=[(b, "A8_identity_wrap", "", ())])
        v = grade(runs[0], shapes["1x1"]).get(
            "ack_retires_only_slot@end:0x20", ("absent", ""))
        if v[0] != "fail":
            print(f"  SELF-TEST FAILED: a 2-bit capture identity reads {v[0]} "
                  f"on A8; it must alias and FAIL, or the 16-bit identity "
                  f"proves nothing.")
            rc = 1
        else:
            print("  identity control: a 2-bit identity aliases on A8 as required")
        rc = grade_mutants(builds, shapes, a.pool) or rc

    #! THE suite tally, in the shape scripts/suite_tally.py reads first. NOT
    #! printed by --wrap-only, which grades one arm and no case's checks: a
    #! tally of zero is not this suite's result
    if not a.wrap_only:
        print(f"nvm_cosim: {totals[0] + totals[1]} checks: {totals[0]} PASS, "
              f"{totals[1]} FAIL ({totals[2]} not expressible)")
    print("RESULT: PASS" if rc == 0 else "RESULT: FAIL")
    return rc



if __name__ == "__main__":
    raise SystemExit(main())
