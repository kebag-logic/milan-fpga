#!/usr/bin/env python3
"""R583-6 independent firmware writer plants (disposable; review evidence only).

Each plant is one exact edit of one firmware source in a private copy of the
tree under review; the firmware gate (test_ctrl_firmware.py, its positive
arms) must then fail.  None of these is in ctrl_mutants.py or
srp_pub_mutants.py at the head under review.  Usage:

    fw_plants_r583_6.py TREE WORKDIR NAME

TREE is a scratch copy of the head with third_party/lwSRP checked out at its
pin; it is copied to WORKDIR/NAME and only that copy is edited.  Writes
WORKDIR/NAME.log and WORKDIR/NAME.rc; exit 0 when the plant was caught.
"""
import shutil
import subprocess
import sys
from pathlib import Path

PLANTS = {
    # The stream_id moving from one nonzero id to another: SID_VALID is no
    # longer cleared first, so SID_LO and SID_HI are rewritten under a set
    # SID_VALID and a half-written stream_id is visible to the datapath.
    "sid-move-no-clear": ("sw/firmware/ctrl/mbx/mbx.c",
                          "\tmbx_hal_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_BINDING), binding);\n"
                          "\tif (stream_id != 0u) {",
                          "\tif (stream_id == 0u) {\n"
                          "\t\tmbx_hal_write32(pub_sink_reg(interface, sink, MBX_PUB_SINK_REG_BINDING), binding);\n"
                          "\t}\n"
                          "\tif (stream_id != 0u) {"),
    # destroy reports each revocation before LICENCE closes on the datapath.
    "destroy-licence-after-reports": ("sw/firmware/ctrl/srp/srp_mbx.c",
                                      "        (void)mbx_pub_licence(n,0u);\n"
                                      "        for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {\n"
                                      "            if (revoked[k]) {\n"
                                      "                m->config.licence(m->config.ctx,n,k,false);\n"
                                      "            }\n"
                                      "        }\n",
                                      "        for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {\n"
                                      "            if (revoked[k]) {\n"
                                      "                m->config.licence(m->config.ctx,n,k,false);\n"
                                      "            }\n"
                                      "        }\n"
                                      "        (void)mbx_pub_licence(n,0u);\n"),
    # an owed stop publishes the stale (still active) licence, then reports the stop.
    "owed-stop-publishes-stale": ("sw/firmware/ctrl/srp/srp_mbx.c",
                                  "                i->active[s] = false;\n"
                                  "                ++m->stops;\n"
                                  "                publish_licence(i);\n",
                                  "                ++m->stops;\n"
                                  "                publish_licence(i);\n"
                                  "                i->active[s] = false;\n"),
    # a sink settled with a reservation (SETTLED_RSV_OK) publishes no stream_id.
    "rsv-ok-not-settled": ("sw/firmware/ctrl/acmp/acmp.c",
                           "bool settled = s->state == ACMP_SETTLED_NO_RSV || s->state == ACMP_SETTLED_RSV_OK;",
                           "bool settled = s->state == ACMP_SETTLED_NO_RSV;"),
    # the MAAP adapter refuses the contract's full 16 sources (boundary).
    "maap-refuses-16-sources": ("sw/firmware/ctrl/maap/maap_mbx.c",
                                "count > MBX_N_PUB_SOURCES",
                                "count >= MBX_N_PUB_SOURCES"),
}


def main() -> int:
    tree, work, name = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    path, old, new = PLANTS[name]
    copy = work / name
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree, copy, symlinks=True)
    target = copy / path
    text = target.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"{name}: fixture occurs {text.count(old)} times in {path}"
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    done = subprocess.run([sys.executable, "-B", "sw/firmware/ctrl/test/test_ctrl_firmware.py", "--require-rv32",
                           "--jobs", "2"], cwd=copy, capture_output=True, text=True, check=False)
    (work / f"{name}.log").write_text(done.stdout + done.stderr, encoding="utf-8")
    (work / f"{name}.rc").write_text(f"{done.returncode}\n", encoding="utf-8")
    caught = done.returncode != 0
    first = next((ln.strip() for ln in (done.stdout + done.stderr).splitlines() if "[FAIL]" in ln), "no [FAIL] line")
    print(f"[{'ok' if caught else 'BAD'}] {name}: gate rc={done.returncode}; first: {first[:220]}")
    shutil.rmtree(copy, ignore_errors=True)
    return 0 if caught else 1


if __name__ == "__main__":
    sys.exit(main())
