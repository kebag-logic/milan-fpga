#!/usr/bin/env python3
"""Disposable fault probes: does the packet's own summarize.py refuse a bad verdict?

usage: mutation_probes.py <packet_author_dir> <scratch_dir>

Each probe copies the published packet into <scratch_dir>/mut-<name>, applies
one fault, and runs the packet's tools/summarize.py there. A probe is KILLED
when summarize.py exits non-zero; SURVIVED means the fault went unnoticed. The
unmutated copy is run first as the control and must exit 0.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def edit_json(path, fn):
    j = json.loads(path.read_text())
    fn(j)
    path.write_text(json.dumps(j, indent=4))


def m_flags_ieee_only(d):
    edit_json(d / "run-2.entity.json", lambda j: j.__setitem__("compatibility_flags", ["IEEE17221"]))


def m_flags_milan_warning(d):
    edit_json(d / "run-3.entity.json",
              lambda j: j.__setitem__("compatibility_flags", ["IEEE17221", "MILAN", "MILAN_WARNING"]))


def m_compat_event(d):
    edit_json(d / "run-1.entity.json", lambda j: j.__setitem__(
        "compatibility_events", [{"previous_flags": ["IEEE17221", "MILAN"], "new_flags": ["IEEE17221"],
                                  "spec_clause": "probe", "message": "probe"}]))


def m_complaint(d):
    p = d / "run-1.log"
    p.write_text(p.read_text().replace("complaints=0", "complaints=1"))


def m_query_error(d):
    p = d / "run-3.log"
    p.write_text(p.read_text().replace("query-errors 0", "query-errors 2"))


def m_rc(d):
    p = d / "run-2.log"
    p.write_text(p.read_text().replace("rc=0", "rc=5"))


def m_static_drift(d):
    def fn(j):
        cfg = j["entity_model"]["entity_descriptor"]["configuration_descriptors"][0]
        cfg["audio_unit_descriptors"][0]["static"]["sampling_rates"] = [44100]
    edit_json(d / "run-3.entity.json", fn)


def m_drop_cluster(d):
    def fn(j):
        au = j["entity_model"]["entity_descriptor"]["configuration_descriptors"][0]["audio_unit_descriptors"][0]
        for key in ("stream_port_input_descriptors", "stream_port_output_descriptors"):
            for sp in au.get(key) or []:
                if sp.get("audio_cluster_descriptors"):
                    sp["audio_cluster_descriptors"].pop()
                    return
    edit_json(d / "run-2.entity.json", fn)


def m_wrong_entity(d):
    edit_json(d / "run-1.entity.json", lambda j: j.__setitem__("entity_model_id", "0x001BC5C40236BA0F"))


def m_diagnostics(d):
    edit_json(d / "run-2.entity.json",
              lambda j: j["diagnostics"].__setitem__("redundancy_warning", True))


def m_diagnostics_all_runs(d):
    for n in (1, 2, 3):
        edit_json(d / f"run-{n}.entity.json",
                  lambda j: j["diagnostics"].__setitem__("redundancy_warning", True))


PROBES = [m_flags_ieee_only, m_flags_milan_warning, m_compat_event, m_complaint, m_query_error,
          m_rc, m_static_drift, m_drop_cluster, m_wrong_entity, m_diagnostics, m_diagnostics_all_runs]


def run(src, dst, mutate):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    if mutate:
        mutate(dst)
    r = subprocess.run([sys.executable, str(dst / "tools/summarize.py")], capture_output=True, text=True, timeout=60)
    tail = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or [""])[-1]
    return r.returncode, tail


def main():
    src, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    control_rc, tail = run(src, scratch / "mut-control", None)
    print(f"CONTROL rc={control_rc} {tail[:120]}")
    survived = 0
    for m in PROBES:
        rc, tail = run(src, scratch / f"mut-{m.__name__}", m)
        state = "KILLED" if rc else "SURVIVED"
        survived += 0 if rc else 1
        print(f"PROBE {m.__name__} {state} rc={rc} {tail[:140]}")
    print(f"SUMMARY control_rc={control_rc} survived={survived} of {len(PROBES)}")
    return 1 if control_rc else 0


if __name__ == "__main__":
    sys.exit(main())
