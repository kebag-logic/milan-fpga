#!/usr/bin/env python3
"""Check exact mutation outcomes and parameter values in published raw logs."""
import csv
import pathlib
import re
import sys
from collections import Counter
p = pathlib.Path(sys.argv[1])
e = p / "scratch/evidence"
expected = dict(N_STREAMS=1, ADP_TALKER_SRC_C=2, ADP_LISTENER_SINK_C=2,
 CRF_SNK_IDX_C=1, MILAN_CLK_FREQ_HZ=100000000, GPTP_PLANE_EN_P=0,
 TALKER_WIRE_CHANS_P=8, AUDIO_IF_SLOTS_P=8, AUDIO_IF_MASTER_P=1,
 AUDIO_IF_RENDER_SLOTS_P=0, AUDIO_IF_I2S_PAIR_P=0, AUDIO_IF_WORD_BITS_P=32,
 AUDIO_IF_FS_HZ_P=48000, AUDIO_IF_CLK_HZ_P=24576000, LOOPBACK_P=1,
 MCSERVO_P=1, LTAP_P=1, MAAP_P=1, I2SPB_P=0, RXFILT_P=1, LPF_P=0, DPROBES_P=1)
gap = "[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0"
sil = "[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0"
start = "[762-DP] 4 started gap: STREAM_INTERRUPTED +1"
for leg, failures in {"clean":[], "tie0":[gap,sil], "sink1":[gap,sil], "bound":[start]}.items():
    text = (e / f"r4-mutants/{leg}.run.log").read_text()
    lines = [s for s in text.splitlines() if "[i]    elaborated" in s]
    params = {k:int(v) for line in lines for k,v in re.findall(r"([A-Z][A-Z0-9_]+) (\d+)", line)}
    assert params == expected, (leg, params)
    actual = [re.split(r"\s+(?:=|got|expected)", s.split("[FAIL]",1)[1].strip())[0] for s in text.splitlines() if "[FAIL]" in s]
    assert actual == failures, (leg, actual)
    assert re.search(rf"checks: 199\s+failures: {len(failures)}\b", text)
    checks = [s for s in text.splitlines() if "[762-DP]" in s and ("[ok]" in s or "[FAIL]" in s)]
    assert len(checks) == 15, (leg,len(checks))
    build = (e / f"r4-mutants/{leg}.build.log").read_text()
    assert "endstation_ax7101_1x1_tdm8" in build
    assert "-DNSTREAMS_TB=1 -DDYNMAP_DEFAULT_TB=1" in build
    if leg != "clean":
        diff = (e / f"r4-mutants/{leg}.diff").read_text()
        removed = [s for s in diff.splitlines() if s.startswith("-") and not s.startswith("---")]
        added = [s for s in diff.splitlines() if s.startswith("+") and not s.startswith("+++")]
        assert len(removed)==len(added)==1 and ".stopped_i" in removed[0] and ".stopped_i" in added[0]
    print(f"{leg}: 22 exact parameters; 15 named checks; 199 total; {len(failures)} expected failures; PASS")
for name in ("checks-head", "checks-r3"):
    with (p / f"receipts/{name}.tsv").open() as stream:
        data = list(csv.DictReader(stream, delimiter="\t"))
    counts=Counter((j["status"],j["conclusion"]) for j in data)
    print(name, sorted(counts.items()))
    for j in data:
        if j["conclusion"] != "success" or j["name"] in ("rtl-fast", "verilator-suites", "yosys-portability", "docs-check"):
            print(j["name"],j["status"],j["conclusion"],j["url"])
print("All published-log assertions passed. No simulation was re-executed.")
