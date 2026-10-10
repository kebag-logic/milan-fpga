#!/usr/bin/env python3
"""R584-3 boundary probes: each plant is written into a disposable copy of the
checkout at the exact head, the boundary gate (ctrl_boundary.py --require-rv32)
is run on it, and the copy is restored. Usage:
    boundary_probes.py <disposable-checkout-copy> <probe-id> [...]
A probe expecting `caught` must exit 1 with a finding holding its needle; a probe
expecting `escape` records whether the gate passes it (a gap)."""
import subprocess, sys
from pathlib import Path

ST = "third_party/tsn-c-stack"
PROBES = {
 "shape-sinks-gt1": ("caught", "test/rv32_image/image_main.c includes tsn-c-stack/examples/adp_port.h", [
   ("sw/firmware/ctrl/test/rv32_image/image_main.c", "#include <stdbool.h>\n",
    "#include <stdbool.h>\n#if IMAGE_SINKS > 1u\n#include \"adp_port.h\"\n#endif\n")]),
 "shape-sources-eq1": ("caught", "test/rv32_image/image_main.c includes tsn-c-stack/src/adp.c", [
   ("sw/firmware/ctrl/test/rv32_image/image_main.c", "#include <stdbool.h>\n",
    "#include <stdbool.h>\n#if defined(IMAGE_SOURCES) && IMAGE_SOURCES == 1u\n"
    "#include \"../../../../../third_party/tsn-c-stack/src/adp.c\"\n#endif\n")]),
 "shape-9x9-only": ("caught", "test/rv32_image/image_main.c includes tsn-c-stack/src/maap.c", [
   ("sw/firmware/ctrl/test/rv32_image/image_main.c", "#include <stdbool.h>\n",
    "#include <stdbool.h>\n#if IMAGE_SINKS == 9u && IMAGE_SOURCES == 9u\n"
    "#include \"../../../../../third_party/tsn-c-stack/src/maap.c\"\n#endif\n")]),
 "cplusplus-adp-mbx-h": ("caught", "firmware c++: adp/adp_mbx.h includes tsn-c-stack/tests/acmp_fake.hpp", [
   ("sw/firmware/ctrl/adp/adp_mbx.h", "#include \"adp.h\"\n",
    "#include \"adp.h\"\n#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\n#endif\n")]),
 "cplusplus-aecp-h": ("caught", "aecp/aecp.h includes tsn-c-stack/src/acmp.c", [
   ("sw/firmware/ctrl/aecp/aecp.h", "#include \"aecp_model.h\"\n",
    "#include \"aecp_model.h\"\n#if defined(__cplusplus)\n#include \"../../../../third_party/tsn-c-stack/src/acmp.c\"\n#endif\n")]),
 "cplusplus-new-header-named-test": ("caught", "maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp", [
   ("+sw/firmware/ctrl/maap/maap_r584.h", "",
    "#ifndef MAAP_R584_H\n#define MAAP_R584_H\n#ifdef __cplusplus\n"
    "#include \"../../../../third_party/tsn-c-stack/tests/acmp_fake.hpp\"\n#endif\n#endif\n"),
   ("sw/firmware/ctrl/test/test_maap_mbx.cpp", "#include \"maap_mbx.h\"\n",
    "#include \"maap_mbx.h\"\n#include \"../maap/maap_r584.h\"\n")]),
 "cplusplus-new-header-maap-differential": ("caught", "maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp", [
   ("+sw/firmware/ctrl/maap/maap_r584.h", "",
    "#ifndef MAAP_R584_H\n#define MAAP_R584_H\n#ifdef __cplusplus\n"
    "#include \"../../../../third_party/tsn-c-stack/tests/acmp_fake.hpp\"\n#endif\n#endif\n"),
   ("sw/firmware/ctrl/test/test_maap_differential.cpp", "#include \"maap.h\"\n",
    "#include \"maap.h\"\n#include \"../maap/maap_r584.h\"\n")]),
 "two-arg-D-list": ("caught", "host [-DR584_TWO_ARG]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h", [
   ("sw/firmware/ctrl/test/ctrl_arms.py", "\n\ndef ", "\n\nR584_PROBE = [\"cc\", \"-D\", \"R584_TWO_ARG\"]\n\n\ndef "),
   (ST + "/src/adp.c", "#include <assert.h>\n", "#include <assert.h>\n#ifdef R584_TWO_ARG\n#include \"mbx_hal.h\"\n#endif\n")]),
 "two-arg-D-call": ("caught", "[-DR584_CALL]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h", [
   ("sw/firmware/ctrl/test/ctrl_arms.py", "\n\ndef ", "\n\nR584_PROBE = print(\"-D\", \"R584_CALL\") if False else None\n\n\ndef "),
   (ST + "/src/maap.c", "#include \"maap.h\"\n", "#include \"maap.h\"\n#ifdef R584_CALL\n#include \"ctrl_loop.h\"\n#endif\n")]),
 "two-arg-D-makefile-value": ("caught", "[-DR584_MK=3]: adp/adp_mbx.c includes tsn-c-stack/src/adp.c", [
   ("tb/verilator/mbx/Makefile", "\nclean:\n", "\nr584-probe:\n\t$(CC) -D R584_MK=3 -U R584_MK2 -c r584.c\n\nclean:\n"),
   ("sw/firmware/ctrl/adp/adp_mbx.c", "#include \"adp_mbx.h\"\n",
    "#include \"adp_mbx.h\"\n#if R584_MK == 3\n#include \"../../../../third_party/tsn-c-stack/src/adp.c\"\n#endif\n")]),
 "two-arg-U-tuple": ("modes", "R584_UNDEF (-DR584_UNDEF -UR584_UNDEF)", [
   ("sw/firmware/ctrl/test/ctrl_arms.py", "\n\ndef ", "\n\nR584_PROBE = (\"-DR584_UNDEF\", \"-U\", \"R584_UNDEF\")\n\n\ndef ")]),
 "multiword-string-flag": ("escape", "R584_MULTI", [
   ("sw/firmware/ctrl/test/ctrl_arms.py", "\n\ndef ", "\n\nR584_PROBE = \"-O2 -DR584_MULTI\".split()\n\n\ndef "),
   (ST + "/src/adp.c", "#include <assert.h>\n", "#include <assert.h>\n#ifdef R584_MULTI\n#include \"mbx_hal.h\"\n#endif\n")]),
 "makefile-new-target-unpinned": ("caught", "r584-probe builds against tsn-c-stack without the pin check", [
   ("tb/verilator/mbx/Makefile", "\nclean:\n", "\nr584-probe:\n\t$(CC) $(FW_INC) -c r584.c\n\nclean:\n")]),
 "makefile-run-cosim-unpinned": ("caught", "run-cosim builds against tsn-c-stack without the pin check", [
   ("tb/verilator/mbx/Makefile", "run-cosim: obj_fw/libctrlfw.a | stack-pin\n", "run-cosim: obj_fw/libctrlfw.a\n")]),
 "makefile-checkout-path": ("caught", "builds the checkout's tsn-c-stack", [
   ("tb/verilator/mbx/Makefile", "\nclean:\n",
    "\nr584-probe: | stack-pin\n\t$(CC) -I$(ROOT)/third_party/tsn-c-stack/include -c r584.c\n\nclean:\n")]),
 "makefile-pin-errors-ignored": ("escape", "", [
   ("tb/verilator/mbx/Makefile", "\tpython3 -B $(FW_DIR)/test/ctrl_build.py --stack-pin $(STACK_DIR)\n",
    "\t-python3 -B $(FW_DIR)/test/ctrl_build.py --stack-pin $(STACK_DIR)\n")]),
 "fw-two-arg-D-list": ("caught", "[-DR584_TWO_ARG]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c", [
   ("sw/firmware/ctrl/test/ctrl_arms.py", "\n\ndef ", "\n\nR584_PROBE = [\"cc\", \"-D\", \"R584_TWO_ARG\"]\n\n\ndef "),
   ("sw/firmware/ctrl/maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
    "#include \"maap_mbx.h\"\n#ifdef R584_TWO_ARG\n#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n#endif\n")]),
 "fw-two-arg-D-call": ("caught", "[-DR584_CALL]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c", [
   ("sw/firmware/ctrl/test/ctrl_arms.py", "\n\ndef ", "\n\nR584_PROBE = print(\"-D\", \"R584_CALL\") if False else None\n\n\ndef "),
   ("sw/firmware/ctrl/maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
    "#include \"maap_mbx.h\"\n#ifdef R584_CALL\n#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n#endif\n")]),
 "fw-multiword-string-flag": ("escape", "R584_MULTI", [
   ("sw/firmware/ctrl/test/ctrl_arms.py", "\n\ndef ", "\n\nR584_PROBE = \"-O2 -DR584_MULTI\".split()\n\n\ndef "),
   ("sw/firmware/ctrl/maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
    "#include \"maap_mbx.h\"\n#ifdef R584_MULTI\n#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n#endif\n")]),
 "fw-two-arg-D-nonmode-shape": ("caught", "[-DR584_TWO_ARG=2]: test/rv32_image/image_main.c includes tsn-c-stack/src/adp.c", [
   ("sw/firmware/ctrl/test/ctrl_image.py", "\n\ndef ", "\n\nR584_PROBE = (\"-D\", \"R584_TWO_ARG=2\")\n\n\ndef "),
   ("sw/firmware/ctrl/test/rv32_image/image_main.c", "#include <stdbool.h>\n",
    "#include <stdbool.h>\n#if R584_TWO_ARG == 2\n#include \"../../../../../third_party/tsn-c-stack/src/adp.c\"\n#endif\n")]),
}

def apply(repo: Path, edits) -> None:
    for rel, old, new in edits:
        if rel.startswith("+"):
            (repo / rel[1:]).write_text(new, encoding="utf-8"); continue
        path = repo / rel
        text = path.read_text(encoding="utf-8")
        if old not in text:
            raise SystemExit(f"anchor missing in {rel}: {old!r}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

def restore(repo: Path) -> None:
    for d in (repo, repo / ST):
        subprocess.run(["git", "-C", str(d), "checkout", "-q", "--", "."], check=True)
        subprocess.run(["git", "-C", str(d), "clean", "-qfd", "--", "."], check=True)

def main() -> int:
    repo = Path(sys.argv[1]).resolve()
    bad = 0
    for pid in sys.argv[2:]:
        expect, needle, edits = PROBES[pid]
        restore(repo); apply(repo, edits)
        res = subprocess.run([sys.executable, "-B", "sw/firmware/ctrl/test/ctrl_boundary.py", "--require-rv32"],
                             cwd=repo, capture_output=True, text=True)
        out = res.stdout + res.stderr
        restore(repo)
        fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l or l.startswith("REFUSED")]
        hit = next((l for l in fails if needle and needle in l), None)
        modes = next((l for l in out.splitlines() if l.startswith("build modes read")), "")
        if expect == "modes":
            verdict = "DERIVED" if needle in modes else "ESCAPED"
        elif expect == "caught":
            verdict = "CAUGHT" if res.returncode == 1 and hit else "ESCAPED"
        else:
            verdict = "GAP-CONFIRMED" if res.returncode == 0 else f"NOT-A-GAP"
        bad += verdict in ("ESCAPED",)
        print(f"[{verdict}] {pid}: exit {res.returncode}; {hit or (fails[0] if fails else 'no finding')}", flush=True)
        modes = next((l for l in out.splitlines() if l.startswith("build modes read")), "")
        if "R584" in modes:
            print("    modes: " + "; ".join(p for p in modes.split("; ") if "R584" in p), flush=True)
        print("    summary: " + next((l.strip() for l in out.splitlines() if l.startswith("ctrl_boundary:")), "none"),
              flush=True)
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
