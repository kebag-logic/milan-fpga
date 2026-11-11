#!/usr/bin/env python3
"""R822-2 disposable probes on a COPY of the reviewed head (never the review clone).

Usage: python3 -B r822_probes.py <probe-tree> <out-dir>

For each probe: restore ctrl_plat.c / aecp.c from the tree's own HEAD blob, apply one
textual edit (asserting the anchor occurs exactly once), build and run the host
platboot arm at one interface (and the AECP core arm where named), record rc and the
failing test lines, then restore the file from git and verify `git status` is clean.
"clean" runs with no edit. Exit 0 always; results in <out-dir>/results.json.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
TEST = ROOT / 'sw/firmware/ctrl/test'
sys.path.insert(0, str(TEST))
sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
import aecp_arms  # noqa: E402
import fw_gtest  # noqa: E402
import plat_arms  # noqa: E402
from ctrl_build import CTRL, STACK, Tree  # noqa: E402

PLAT = 'sw/firmware/ctrl/plat/ctrl_plat.c'
AECP = 'sw/firmware/ctrl/aecp/aecp.c'

PROBES = {
    'clean': [],
    # the receive gate left off the MAAP and SRP channels (B19 sends ADP, ACMP and AECP frames only)
    'gate-skips-maap-and-srp': [(PLAT, '\t\tif (p->rx[ch].fn != NULL) {\n',
                                 '\t\tif (p->rx[ch].fn != NULL && ch < MBX_CH_MAAP) {\n')],
    # the DEPARTING waits for ADP-adjacent rings only (B21 holds the ACMP ring only)
    'depart-ignores-maap-and-srp-rings': [(PLAT, '\t\t\tif (ch != MBX_CH_ADP && !drained(ch)) {\n',
                                           '\t\t\tif (ch != MBX_CH_ADP && ch < MBX_CH_MAAP && !drained(ch)) {\n')],
    # acceptance reported only from the poll after the SUCCESS (reboot 2), not at the SUCCESS itself
    'accepted-from-the-poll': [(AECP, '\treturn a->reboot != 0u;\n', '\treturn a->reboot >= 2u;\n')],
    # ADP's poll not run in state 2: the DEPARTING still sent? (the loop's last pass may have committed it)
    'no-adp-poll-in-state-2': [(PLAT, '\t\t\t(void)adp_poll(&p->app.adp.ifs[i].adp);\n', '')],
    # the store not serviced from the loop's stop to the port (only after it)
    'quiet-only-after-the-port': [(PLAT, 'static void depart(struct ctrl_plat *p)\n{\n\tquiet(p);\n',
                                   'static void depart(struct ctrl_plat *p)\n{\n\tif (p->reboot == 3u) quiet(p);\n')],
}
AECP_PROBES = {'accepted-from-the-poll'}


def git(*args: str) -> str:
    return subprocess.run(['git', '-C', str(ROOT), *args], check=True, capture_output=True, text=True).stdout


def restore() -> None:
    git('checkout', '--', PLAT, AECP)
    status = git('status', '--porcelain', '--untracked-files=no')
    if status.strip():
        raise SystemExit(f'probe tree not clean after restore: {status}')


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[3:] or list(PROBES)
    results = {}
    for name in only:
        restore()
        for path, old, new in PROBES[name]:
            f = ROOT / path
            text = f.read_text()
            if text.count(old) != 1:
                raise SystemExit(f'{name}: anchor occurs {text.count(old)} times in {path}')
            f.write_text(text.replace(old, new))
        where = OUT / name
        tree = Tree(CTRL, where / 'build', where / 'reuse', fw_gtest.Build(jobs=8), STACK)
        arms = {'platboot1': lambda: plat_arms.arm_platboot(tree, 1)}
        if name == 'clean':
            arms['platboot2'] = lambda: plat_arms.arm_platboot(tree, 2)
        if name in AECP_PROBES or name == 'clean':
            arms['aecp'] = lambda: aecp_arms.core_arm(tree, ROOT / 'configs/endstation_ax7101_1x1_tdm8.yaml', 2,
                                                      'app', 'Core.Reboot*')
        res = {}
        for arm, fn in arms.items():
            try:
                o = fn()
                rc, log = o.rc, o.log
            except Exception as exc:  # a refusal is a result too
                rc, log = 99, f'REFUSAL {type(exc).__name__}: {exc}'
            (where / f'{arm}.log').write_text(log)
            fails = sorted({ln.strip() for ln in log.splitlines() if '[FAIL]' in ln or '[  FAILED  ]' in ln})
            res[arm] = {'rc': rc, 'fails': fails[:30]}
            print(f'{name} {arm}: rc={rc} fails={len(fails)}', flush=True)
        results[name] = res
        restore()
    (OUT / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
