"""Plant each parent-side control alone in one clone of the scratch parent
snapshot, run the milan_dp gptp leg, and record every FAIL line.

usage: parent_mutants.py <clone> <out dir>
Each control is (name, file under the clone, pattern, replacement, the
named checks it must fail). The clone is restored after each control
(git checkout in the parent and in gptp-processor).
"""
import json
import subprocess
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
GEN = "gptp-processor/hdl/ucode/gen_gptp_ucode.py"
ENG = "gptp-processor/hdl/top/KL_gptp_engine.sv"
SHADOW = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
LINK = "#94 asCapable falls at link loss"
CEASE = "#94 a link loss inside the cease ends it: a Pdelay_Req within one interval of the return"
COUNT = "#94 the cease countdown exit is unchanged: 5 s from the last request"
CONTROLS = [
    ("the shadow ties the engine's port enabled", SHADOW,
     "      .port_enabled_i     (port_enabled_i),\n",
     "      .port_enabled_i     (1'b1),\n", [LINK, CEASE]),
    ("a portEnabled edge keeps the cease", GEN,
     "    for s in (S_CEASE, S_CEASECNT, S_MULTI):\n",
     "    for s in (S_CEASECNT, S_MULTI):\n", [CEASE]),
    ("the falling edge raises no event", ENG,
     "      if (port_seen_r && (port_enabled_i != port_en_r)) begin\n",
     "      if (port_seen_r && port_enabled_i && !port_en_r) begin\n", [LINK]),
    ("the countdown loads one beat less", GEN,
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=max(1, RUNTIME[\"cease_ms\"] // 1000))\n",
     "    p.emit(\"MOVE\", rd=RT, ra=0, imm=max(1, RUNTIME[\"cease_ms\"] // 1000 - 1))\n", [COUNT]),
]
ENV = {"PATH": "<scratch>/bin:<user-bin>:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       "VERILATOR_ROOT": "<verilator-5.050-root>",
       "TMPDIR": "<scratch>/tmp", "HOME": "<home>"}


def restore():
    subprocess.run(["git", "checkout", "--", "."], cwd=clone, check=True)
    subprocess.run(["git", "checkout", "--", "."], cwd=clone / "gptp-processor", check=True)


rows = []
for k, (name, rel, pat, rep, named) in enumerate(CONTROLS, 1):
    restore()
    path = clone / rel
    text = path.read_text()
    assert text.count(pat) == 1, name
    path.write_text(text.replace(pat, rep))
    log = out / f"pm{k}.log"
    with log.open("w") as stream:
        rc = subprocess.run(["make", "-C", "tb/verilator/milan_dp", "gptp"], cwd=clone,
                            env=ENV, stdout=stream, stderr=subprocess.STDOUT).returncode
    lines = log.read_text().splitlines()
    fails = [l for l in lines if l.startswith("FAIL ")]
    tally = [l for l in lines if "checks:" in l]
    missed = [n for n in named if not any(n in l for l in fails)]
    rows.append(dict(control=name, file=rel, rc=rc, tally=tally[-1] if tally else None,
                     named=named, missed=missed, fails=fails))
    print(name, "rc", rc, tally[-1] if tally else "no tally", "missed", missed, flush=True)
restore()
(out / "results.json").write_text(json.dumps(rows, indent=1) + "\n")
print("caught", sum(1 for r in rows if r["rc"] != 0 and not r["missed"]), "of", len(rows))
