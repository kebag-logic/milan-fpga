"""Reproduce #501 K16 and boundary evidence against immutable #500 sources.
Only temporary evidence copies are adapted. Product and donor sources are read.
"""
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path.cwd()
OUTPUT = Path(__file__).resolve().parent
SHA = "a21b165ac1c671d10cba7255beaf75cea0f81d18"

with tempfile.TemporaryDirectory(prefix="501-d3.") as tmp:
    scratch = Path(tmp)
    archive = subprocess.run(["git", "archive", SHA, "design-evidence/500-materialization"],
                             check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        tf.extractall(scratch, filter="data")
    here = scratch / "design-evidence/500-materialization/proposal-evidence"
    runner = here / "run.py"
    runner.write_text(runner.read_text().replace("ROOT = HERE.parents[2]", f"ROOT = Path({str(ROOT)!r})"))
    os.environ["D3_OUT"] = str(scratch / "build")
    spec = importlib.util.spec_from_file_location("d3_evidence", runner)
    d3 = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = d3
    spec.loader.exec_module(d3)
    d3.check_m0_encoding()
    shape = d3.prep_shape("8x8")
    overlay = json.loads(next((shape.work / "builder").glob("*/aem_overlay.json")).read_text())
    clusters = [p["clusters"] for p in overlay["stream_ports"]["output"]]
    # The historical harness equated capacity with clusters. Separate these:
    # record capacities stay in the prototype parameters, physical clusters
    # stay in the model's edit validator and initial mappings.
    cases = here / "harness/d3_cases.cpp"
    text = cases.read_text()
    text = text.replace("cls_out.push_back(r.second.plen / 8);",
                        "cls_out.push_back(std::vector<unsigned>{" +
                        ",".join(map(str, clusters)) + "}[r.first - 0x70]);")
    text = text.replace("    idle(3000);                                  // several debounce windows\n    snap(\"over\");\n    map_remove(true, 0, {extra.back()});         // the controller shrinks it to fit\n    converge();",
                        "    converge();\n    snap(\"over\");")
    text = text.replace("void register_cases() {", """void register_cases() {
  cases["K501_save_boundary"] = [] {
    boot();
    for (unsigned p = 0; p < map_out.size(); ++p) {
      const auto old = map_out[p].cur;
      map_remove(true, p, old);
      settle();
    }
    std::vector<Map> all;
    for (unsigned s = 0; s < n_so; ++s)
      for (unsigned ch = 0; ch < fmt_channels(def_fmt_out[s]) && ch < 8; ++ch)
        all.push_back(Map{uint16_t(s), uint16_t(ch), 0, 0});
    map_add(true, 0, all);
    converge();
    note("saved_keys", map_out[0].cur.size());
    snap("end");
  };
  cases["K501_restore"] = [] {
    for (auto &p : map_out) { p.cur.clear(); p.def.clear(); }
    for (auto &p : map_in) { p.cur.clear(); p.def.clear(); }
    snap("cleared");
    boot();
    idle(200);
    snap("restored");
  };
""")
    text = text.replace("  default_maps();", """  for (unsigned p = 0; p < map_out.size(); ++p) map_out[p].capacity = recs.at(0x70 + p).plen;
  for (unsigned p = 0; p < map_in.size(); ++p) map_in[p].capacity = recs.at(0x60 + p).plen;
  // The full storage-key test is explicitly synthetic: the CRF descriptor
  // reserves keys but is not an AAF mapping source in the product.
  if (variant == "storage_keys") def_fmt_out.back() = def_fmt_out.front();
  default_maps();""")
    cases.write_text(text)
    header = here / "harness/d3_bridge.h"
    header.write_text(header.read_text().replace("struct MapPort {", "struct MapPort {\n  unsigned capacity = 0;"))
    bridge = here / "harness/d3_bridge.cpp"
    bridge.write_text(bridge.read_text().replace("8u * p.clusters) v.push_back", "p.capacity) v.push_back"))
    try:
        build = d3.do_build(d3.Build("base-8x8", "8x8"), shape, 8)
    except BaseException:
        for log in (scratch / "build/logs").glob("*.log"):
            (OUTPUT / ("d3-" + log.name)).write_text(log.read_text())
        raise
    results = []
    for label, case, variant in (("K16", "K16_map_set_larger_than_its_record", ""),
                                 ("boundary_audio", "K501_save_boundary", ""),
                                 ("boundary_storage", "K501_save_boundary", "storage_keys")):
        saved = d3.run_case(build, shape, case, variant)
        assert saved.rc == 0 and saved.done, (label, saved.rc, saved.out)
        grade = d3.Grade(saved, shape)
        grade.converged("end")
        grade.value_in_slot("end", 0x70)
        grade.durability()
        grade.written_values()
        decoded = grade.tag_slots("end")
        payload = decoded[0x70]
        entries = [payload[i:i+8] for i in range(0, len(payload), 8) if payload[i:i+8] != b"\xff"*8]
        expected = clusters[0] + 1 if label == "K16" else sum(
            min(8, (f >> 22) & 0x3ff) if (f >> 56) == 2 else 0
            for f in (shape.def_fmt_out[:-1] + [shape.def_fmt_out[0]]
                      if variant else shape.def_fmt_out))
        grade.check("all_expected_keys_saved", len(entries) == expected, f"{len(entries)} / {expected}")
        slots = (saved.out / "end-slotA.bin", saved.out / "end-slotB.bin")
        restored = d3.run_case(build, shape, "K501_restore", variant, slots)
        grade.check("restore_process", restored.rc == 0 and restored.done, str(restored.rc))
        cleared = restored.obs["cleared"]["maps_out"]
        grade.check("cleared_first_every_output", all(set(bytes.fromhex(x)) <= {255} for x in cleared),
                    f"{len(cleared)} ports empty before boot")
        for port, got in enumerate(restored.obs["restored"]["maps_out"]):
            want = decoded.get(0x70 + port, b"\xff" * shape.recs[0x70 + port][2])
            grade.check(f"restored_port_{port}", bytes.fromhex(got) == want,
                        f"compared {len(want)} bytes against decoded journal")
        grade.check("restore_not_failed", restored.obs["restored"]["d3_fail"] == 0,
                    str(restored.obs["restored"]["d3_fail"]))
        result = dict(label=label, keys=len(entries), checks=grade.checks)
        results.append(result)
        for phase, run in (("save", saved), ("restore", restored)):
            (OUTPUT / f"d3-{label}-{phase}.log").write_text((run.out / "stdout.log").read_text())
        print(json.dumps(result), flush=True)
    (OUTPUT / "d3-results.json").write_text(json.dumps(results, indent=2) + "\n")
    assert all(ok for result in results for ok, detail in result["checks"].values()), "D3 checks failed"
