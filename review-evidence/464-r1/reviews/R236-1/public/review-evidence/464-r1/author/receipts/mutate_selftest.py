#!/usr/bin/env python3
"""Mutation receipts for #464: every retained self-test arm must FAIL against
the defect it names, and each repair the lane made must be load-bearing.

    mutate_selftest.py <checkout> <rev> [python]

For each mutant a fresh scratch tree is extracted from <rev> (`git archive`
of avdecc/ and hdl/common/csr/, the only paths the store generator reads),
one exact textual defect is planted (the harness refuses a patch whose target
text does not occur exactly once, so no mutant can silently no-op), and
`python -B avdecc/gen_aem_store.py --self-test` runs in that tree.

Expectation "red": the run must exit non-zero AND print every listed
fragment, which names the arm that caught it. Expectation "green" marks a
CONTROL: a mutant that also removes one repair and must then pass, proving
that repair is what catches the defect. The lane checkout is never written.
Exit 0 only when every mutant meets its expectation.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

CHECKOUT, REV = Path(sys.argv[1]).resolve(), sys.argv[2]
PY = sys.argv[3] if len(sys.argv) > 3 else sys.executable
MAPS, STORE, ASM, DESC = ("avdecc/aem_maps.py", "avdecc/gen_aem_store.py",
                          "avdecc/aem_assemble.py", "avdecc/aem_descriptors.py")

ORACLE_OFF = (STORE, "            if cause in str(e):\n",
              "            if True:\n")
REVERSE_OFF = (STORE, "    stale = sorted(set(KNOWN_MAP_DEVIATIONS) - set(got))\n",
               "    stale = []\n")
OLD_62_VECTOR = (STORE, "                1, [[0, c, c % 8, 0] for c in range(63)]),\n",
                 "                0, [[0, c % 8, c, 0] for c in range(63)]),\n")
NO_COUNT_BOUND = (MAPS, "    if len(rows) > SMAP_MAX_ROWS:\n",
                  "    if False and len(rows) > SMAP_MAX_ROWS:\n")
NO_CRF_REFUSAL = (MAPS, "    if not chans:\n", "    if False and not chans:\n")
WIDENED = (MAPS, "    for c in range(2, 8)\n}\n",
           "    for c in range(2, 8)\n}\nKNOWN_MAP_DEVIATIONS |= {d.replace("
           "'AUDIO_MAP[0]', 'AUDIO_MAP[1]') for d in KNOWN_MAP_DEVIATIONS}\n")

# (id, what the mutant plants, [(file, old, new)], "red"/"green", fragments)
MUTANTS = [
    ("M00", "pristine tree (control)", [], "green", ["self-test: PASS"]),
    ("M01", "Table 7-33 cluster_offset bound removed",
     [(MAPS, '    if co >= port["clusters"]:\n',
       '    if False and co >= port["clusters"]:\n')], "red",
     ["[FAIL] global cluster index where 7.2.19 wants a port-relative "
      "offset: built without complaint"]),
    ("M02", "7.2.13 base_map existence bound removed",
     [(MAPS, "    if not 0 <= bm < len(maps):\n",
       "    if False and not 0 <= bm < len(maps):\n")], "red",
     ["[ok  ] global cluster index", "rows = maps[bm]", "IndexError"]),
    ("M03", "number_of_maps == 1 bound removed",
     [(MAPS, '    if port["maps"] != 1:\n',
       '    if False and port["maps"] != 1:\n')], "red",
     ["[FAIL] number_of_maps != 1 on a static port (pages it cannot answer): "
      "built without complaint"]),
    ("M04", "7.2.16 cluster_channel bound removed",
     [(MAPS, "    if cc >= SMAP_CLUSTER_CHANNELS:\n",
       "    if False and cc >= SMAP_CLUSTER_CHANNELS:\n")], "red",
     ["[FAIL] cluster_channel past the cluster's channel_count (7.2.16): "
      "built without complaint"]),
    ("M05", "7.2.13 stream_index bound removed",
     [(MAPS, "    if si >= side.n_streams:\n",
       "    if False and si >= side.n_streams:\n")], "red",
     ["[ok  ] cluster_channel past", "side.stream_specs[si]", "IndexError"]),
    ("M06", "7.2.19 INPUT duplicate rule removed",
     [(MAPS, "        if (co, cc) in seen:\n",
       "        if False and (co, cc) in seen:\n")], "red",
     ["[FAIL] INPUT: two mappings onto the SAME cluster channel (7.2.19): "
      "built without complaint"]),
    ("M07", "CRF no-channel refusal removed (max() of nothing raises instead)",
     [NO_CRF_REFUSAL], "red",
     ["[FAIL] a mapping onto the CRF sink, which carries no audio channels: "
      "refused, but not for 'advertises no audio format with channels'"]),
    ("M07c", "control: M07 with the cause oracle removed",
     [NO_CRF_REFUSAL, ORACLE_OFF], "green", ["self-test: PASS"]),
    ("M08", "7.2.19 OUTPUT duplicate rule removed",
     [(MAPS, "        if (si, sc) in cfg_stream_ch:\n",
       "        if False and (si, sc) in cfg_stream_ch:\n")], "red",
     ['[FAIL] OUTPUT: the same (stream_index, stream_channel) twice (7.2.19 '
      '"across the entire Configuration"): built without complaint']),
    ("M09", "INPUT rule applied to both directions (the gate's first version)",
     [(MAPS, '    if side.direction == "INPUT":\n', "    if True:\n")], "red",
     ['[FAIL] OUTPUT: the same (stream_index, stream_channel) twice',
      '[FAIL] OUTPUT: the same cluster_offset twice IS allowed']),
    ("M09o", "OUTPUT rule applied to both directions",
     [(MAPS, '    if side.direction == "INPUT":\n', "    if False:\n")], "red",
     ["[FAIL] INPUT: two mappings onto the SAME cluster channel (7.2.19): "
      "refused, but not for 'for a STREAM_PORT_INPUT'"]),
    ("M10", "Table 7-32 mapping-count bound removed", [NO_COUNT_BOUND], "red",
     ["[FAIL] more mappings in one AUDIO_MAP than Table 7-32 allows (62): "
      "built without complaint"]),
    ("M10c", "control: M10 with the base-head 62-mapping vector, oracle removed",
     [NO_COUNT_BOUND, OLD_62_VECTOR, ORACLE_OFF], "green", ["self-test: PASS"]),
    ("M10g", "M10 with the oracle removed: the new geometry alone catches it",
     [NO_COUNT_BOUND, ORACLE_OFF], "red",
     ["[FAIL] more mappings in one AUDIO_MAP than Table 7-32 allows (62): "
      "built without complaint"]),
    ("M10o", "M10 on the base-head vector: the oracle alone catches it",
     [NO_COUNT_BOUND, OLD_62_VECTOR], "red",
     ["[FAIL] more mappings in one AUDIO_MAP than Table 7-32 allows (62): "
      "refused, but not for 'has 63 mappings'"]),
    ("M11", "allowlist back at the stale AUDIO_MAP[1] index (the base head)",
     [(MAPS, '"STREAM_PORT_OUTPUT[0] AUDIO_MAP[0] mapping',
       '"STREAM_PORT_OUTPUT[0] AUDIO_MAP[1] mapping')], "red",
     ["[FAIL] a NEW deviation appeared",
      "[FAIL] recorded deviation(s) the deployed model does not carry"]),
    ("M12", "allowlist widened: the stale entries kept beside the new ones",
     [WIDENED], "red",
     ["[FAIL] recorded deviation(s) the deployed model does not carry"]),
    ("M12c", "control: M12 with the reverse exactness check removed",
     [WIDENED, REVERSE_OFF], "green", ["self-test: PASS"]),
    ("M13", "assert_no_map_deviations neutered",
     [(MAPS, "    if new:\n", "    if False and new:\n")], "red",
     ["[FAIL] the deviation allowlist is not asserting anything"]),
    # A refused DEPLOYED model never reaches the arms: importing the
    # generator builds it (aem_assemble `_M`), so the run fails closed there.
    ("M14d", "static serving path refuses the deployed one-map output port",
     [(MAPS, '    if port["maps"] != 1:\n', '    if port["maps"] == 1:\n')],
     "red", ["_M = build_model(builtin_spec())",
             "ValueError: STREAM_PORT_OUTPUT[0] declares number_of_maps=1"]),
    ("M14", "static INPUT maps refused outright (the fixture, not the model)",
     [(MAPS, '    if port["maps"] != 1:\n',
       '    if port["maps"] != 1 or tag.startswith("STREAM_PORT_INPUT"):\n')],
     "red", ["[ok  ] the deployed model still builds",
             "[FAIL] the two-map fixture the vectors mutate builds"]),
    ("M15", "fixture shared across vectors (no fresh copy per vector)",
     [(STORE, "\n\ndef _selftest_map_bounds():\n",
       "\n_SHARED = _map_fixture()\n_map_fixture = lambda: _SHARED\n\n\n"
       "def _selftest_map_bounds():\n")], "red",
     ["[FAIL] INPUT: two mappings onto the SAME cluster channel (7.2.19): "
      "refused, but not for"]),
    ("M16", "fixture replaced by the deployed geometry (the #464 failure)",
     [(STORE, "    return spec\n\n\ndef _selftest_map_bounds():\n",
       "    return builtin_spec()\n\n\ndef _selftest_map_bounds():\n")], "red",
     ["IndexError: list assignment index out of range"]),
    ("T01", "two-level directory gate disabled (runs, indices, equivalence)",
     [(ASM, "        elif prev_t != t:\n", "        elif False:\n"),
      (ASM, "        if i != runs[t][1]:\n", "        if False:\n"),
      (ASM, "        if got != want:\n", "        if False:\n")], "red",
     ["[FAIL] a shuffled directory entry (contiguity): accepted without "
      "complaint", "[FAIL] same-type entries out of index order: accepted "
      "without complaint", "[FAIL] an off-by-one level-1 row base was "
      "accepted"]),
    ("T02", "structural name gate neutered",
     [(ASM, "        if got != exp:\n", "        if False:\n")], "red",
     ["[FAIL] a mask bit on the unnamed STRINGS type was accepted"]),
    ("T03", "Base-family cover can no longer say no",
     [(MAPS, "    return got\n", "    return set(MILAN_BASE_CHANNELS)\n")],
     "red", ["[FAIL] the family check passes without the ut entry"]),
    ("T04", "builtin FORMATS loses its ut entry",
     [(DESC, "FORMATS = [0x0205022000806000, 0x0215022002006000]",
       "FORMATS = [0x0205022000806000]")], "red",
     ["[FAIL] FORMATS (STREAM_INPUT): 48 kHz Base channel count(s)"]),
]


def extract(dst: Path) -> None:
    """The committed tree at REV, only the paths the generator reads."""
    arc = subprocess.run(["git", "-C", str(CHECKOUT), "archive", REV,
                          "avdecc", "hdl/common/csr"],
                         check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dst)], input=arc, check=True)


def plant(tree: Path, patches: list[tuple[str, str, str]]) -> None:
    """Apply each exact replacement once; refuse an ambiguous or absent one."""
    for rel, old, new in patches:
        path = tree / rel
        text = path.read_text()
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"HARNESS: {rel}: target occurs {count} times: "
                             f"{old!r}")
        path.write_text(text.replace(old, new))


def main() -> int:
    """Run every mutant and print one verdict row per mutant."""
    sha = subprocess.run(["git", "-C", str(CHECKOUT), "rev-parse", REV],
                         check=True, capture_output=True, text=True).stdout
    ver = subprocess.run([PY, "--version"], capture_output=True,
                         text=True).stdout.strip()
    print(f"mutation receipts at {sha.strip()} with {ver}\n")
    bad = 0
    for mid, what, patches, want, fragments in MUTANTS:
        with tempfile.TemporaryDirectory(prefix=f"aem464-{mid}-") as tmp:
            tree = Path(tmp)
            extract(tree)
            plant(tree, patches)
            run = subprocess.run([PY, "-B", "avdecc/gen_aem_store.py",
                                  "--self-test"], cwd=tree,
                                 capture_output=True, text=True)
        out = run.stdout + run.stderr
        missing = [f for f in fragments if f not in out]
        exit_ok = (run.returncode != 0) if want == "red" else (run.returncode == 0)
        met = exit_ok and not missing
        bad += not met
        lines = [ln.strip() for ln in out.splitlines()]
        evidence = next((ln for ln in lines if ln.startswith("[FAIL]")),
                        next((ln for ln in reversed(lines) if "Error" in ln),
                             lines[-1] if lines else ""))
        print(f"{mid:5} {'MET ' if met else 'MISS'} exit={run.returncode} "
              f"want={want:5} {what}\n      evidence: {evidence[:170]}")
        for f in missing:
            print(f"      MISSING fragment: {f!r}")
    print(f"\n{len(MUTANTS) - bad}/{len(MUTANTS)} mutants met their "
          "expectation")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
