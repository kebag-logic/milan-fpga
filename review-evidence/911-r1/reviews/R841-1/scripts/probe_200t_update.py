#!/usr/bin/env python3
"""Reviewer probe (#911): the deployment guide's "Update a flashed board" step
for the XC7A200T variant, `INSTALLED_BUILD=<A> build.sh flash ax7a200t:<B>`,
run against a stub programmer on two image sets shaped like the 200T release
(bitstream budget 0xA00000, AEM at 0xA00000, a 9,730,652-B payload).

usage: probe_200t_update.py <repo clone> <scratch dir> <python with litex>
Prints one line per arm and exits 0 only if every arm behaves as expected.
No cable is opened: the programmer on PATH is the stub written here.
"""
import json
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

REPO, SCRATCH, LITEX_PY = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(REPO / "sw" / "litex"))
import qspi_owner_transition as q  # noqa: E402

PAYLOAD_BYTES = 9_730_652
STUB = r'''#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.environ["PROBE_SOC_DIR"])
import qspi_owner_transition as q
args = sys.argv[1:]
log = os.environ["PROBE_LOG"]; qspi = os.environ["PROBE_QSPI"]
def value(flag, default=None):
    return args[args.index(flag) + 1] if flag in args else default
with open(log, "a") as t:
    t.write(" ".join(a for a in args) + "\n")
if "--detect" in args:
    print("index 0:\n\tidcode 0x3636093\n\tmanufacturer xilinx\n\tfamily artix a7 200t\n"
          "\tmodel  " + os.environ.get("PROBE_MODEL", "xc7a200") + "\n\tirlength 6")
    if "-f" in args:
        j = os.environ.get("PROBE_JEDEC", "20ba18")
        print(" ".join(f"{b:x}" for b in bytes.fromhex(j)) + f" read {int(j, 16):x}")
    sys.exit(0)
if "--dump-flash" in args:
    with open(qspi, "rb") as f, open(args[-1], "wb") as o:
        f.seek(int(value("-o", "0"), 0)); o.write(f.read(int(value("--file-size"), 0)))
    sys.exit(0)
if "--verify" not in args:
    sys.exit(90)
src = args[-1]
if value("-o") is None:
    data, off = q.bit_payload(src), 0
else:
    data, off = open(src, "rb").read(), int(value("-o"), 0)
with open(qspi, "r+b") as f:
    f.seek(off); f.write(data)
with open(log, "a") as t:
    t.write(f"WRITE\t{off}\t{len(data)}\n")
'''


def make_set(root: Path, name: str, seed: int, aem_offset: int) -> dict:
    """One image set in the delivered directory layout."""
    d = root / name
    (d / "gateware").mkdir(parents=True)
    rnd = random.Random(seed)
    body = rnd.randbytes(PAYLOAD_BYTES - 20)
    payload = b"\xff" * 16 + b"\xaa\x99\x55\x66" + body
    bit = d / "gateware" / "alinx_ax7101.bit"
    q._fake_bit(bit, payload, name.encode(), b"7a200tfbg484\0")
    aem = d / "aem_desc.bin"
    aem.write_bytes(b"AEMI" + rnd.randbytes(7508))
    layout = {"manifest": "baremetal", "gptp_owner": "fabric", "complete": False,
              "cpu_xlen": 32, "flash_device": "n25q128a13", "flash_jedec_id": 0x20BA18,
              "images": [{"name": "bitstream", "offset": 0, "addr": 0, "budget": aem_offset},
                         {"name": "aem", "offset": aem_offset, "addr": 0, "budget": 0x10000}],
              "reserved": {"journal": {"offset": 0xEE0000, "size": 0x20000},
                           "user": {"offset": 0xF00000, "size": 0x100000}}}
    layout.update(q.bitstream_binding(bit))
    layout.update(q.aem_image_binding(aem))
    (d / "flashboot_layout.json").write_text(json.dumps(layout), encoding="utf-8")
    return {"dir": d, "payload": payload, "aem": aem.read_bytes(), "aem_offset": aem_offset}


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    (SCRATCH / "bin").mkdir(parents=True)
    stub = SCRATCH / "bin" / "openFPGALoader"
    stub.write_text(STUB.replace("#!/usr/bin/env python3", "#!" + sys.executable, 1))
    stub.chmod(0o755)
    a = make_set(SCRATCH, "A", 1, 0xA00000)
    b = make_set(SCRATCH, "B", 2, 0xA00000)
    stale = make_set(SCRATCH, "S", 3, 0x400000)   # a 200T set on the AX7101 map
    qspi, log = SCRATCH / "qspi.bin", SCRATCH / "ofl.log"
    tmp = SCRATCH / "tmp"
    tmp.mkdir()
    env = dict(os.environ, PATH=f"{SCRATCH / 'bin'}:{os.path.dirname(LITEX_PY)}:{os.environ['PATH']}",
               PYTHON=LITEX_PY, PROBE_SOC_DIR=str(REPO / "sw" / "litex"),
               PROBE_QSPI=str(qspi), PROBE_LOG=str(log), AX_FTDI="PROBE-SERIAL",
               TMPDIR=str(tmp))
    for k in ("INSTALLED_LAYOUT", "INSTALLED_BIT", "LAYOUT", "BIT", "FPGA_PART"):
        env.pop(k, None)

    def load(s):
        with open(qspi, "wb") as f:
            f.truncate(16 << 20); f.seek(0); f.write(s["payload"])
            f.seek(s["aem_offset"]); f.write(s["aem"])
        log.unlink(missing_ok=True)

    def run(installed, target, recipe="ax7a200t", **over):
        e = dict(env, INSTALLED_BUILD=str(installed["dir"]), **over)
        return subprocess.run(["bash", str(REPO / "sw/litex/build.sh"), "flash",
                               f"{recipe}:{target['dir']}"], cwd=REPO, env=e,
                              text=True, capture_output=True, timeout=600)

    def writes():
        if not log.exists():
            return []
        return [l.split("\t")[1] for l in log.read_text().splitlines() if l.startswith("WRITE")]

    ok = True

    def arm(name, good, detail):
        nonlocal ok
        ok &= good
        print(f"{'PASS' if good else 'FAIL'} {name}: {detail}")

    load(a)
    r = run(a, b)
    flash = qspi.read_bytes()
    good = (r.returncode == 0 and writes() == [str(0xA00000), "0"]
            and flash[:len(b["payload"])] == b["payload"]
            and flash[0xA00000:0xA00000 + len(b["aem"])] == b["aem"])
    arm("update A->B (200T map)", good, f"rc {r.returncode}, writes {writes()}")
    if not good:
        print(r.stdout[-2000:], r.stderr[-2000:])
    load(b)
    r = run(b, b)
    arm("identical refresh refused", r.returncode != 0 and not writes(), f"rc {r.returncode}, writes {writes()}")
    load(a)
    r = run(a, b, PROBE_MODEL="xc7a100")
    arm("200T set on a 100T die refused", r.returncode != 0 and not writes()
        and "does not match" in r.stderr, f"rc {r.returncode}, writes {writes()}")
    load(a)
    r = run(a, b, PROBE_JEDEC="20ba19")
    arm("other flash refused", r.returncode != 0 and not writes()
        and "JEDEC ID 0x20ba19" in r.stderr, f"rc {r.returncode}, writes {writes()}")
    load(a)
    r = run(a, b, recipe="ax7101")
    arm("ax7101 recipe refuses a 200T set", r.returncode != 0 and not writes(),
        f"rc {r.returncode}, writes {writes()}")
    load(stale)
    r = run(stale, b)
    arm("stale 4-MiB-map installed set", True,
        f"rc {r.returncode}, writes {writes()}; {(r.stderr.strip().splitlines() or [''])[-1][:160]}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
