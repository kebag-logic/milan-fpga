"""Scratch: plant the round-1 console logic (and a wipe refused while held)
into a copy of the head firmware and show grade_hold_console reddening.

usage: console_plants.py REPO CONFIG WORK
"""
import sys
from pathlib import Path

repo, cfg, work = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as t  # noqa: E402

PLANTS = {
    # the f54dbe3e console: the hold named whenever a slot is unread
    "console_names_unread_on_retire": [
        ('nvm_ready ? "writer live" : (nvm_held ? "writer HELD',
         'nvm_ready ? "writer live" : (nvm_unread ? "writer HELD'),
        ("\t\tif (nvm_held)\n\t\t\tprintf(", "\t\tif (!nvm_ready && nvm_unread)\n\t\t\tprintf("),
    ],
    # a wipe refused while held (the behaviour the docs now say does not happen)
    "wipe_refused_while_held": [
        ("\tif (nb_params == 1 && nvm_arg_is(params[0], \"wipe\")) {\n",
         "\tif (nb_params == 1 && nvm_arg_is(params[0], \"wipe\") && nvm_held) {\n"
         "\t\treturn;\n\t}\n\tif (nb_params == 1 && nvm_arg_is(params[0], \"wipe\")) {\n"),
    ],
}
fw = t.FIRMWARE.read_text()
work.mkdir(parents=True, exist_ok=True)
base = t.make_bench(cfg, work / "base", fw)
print(f"HEAD {cfg.stem}: grade_hold_console -> {t.grade_hold_console(base)}")
for label, pairs in PLANTS.items():
    text = fw
    for old, new in pairs:
        assert text.count(old) == 1, (label, old)
        text = text.replace(old, new)
    got = t.grade_hold_console(t.replant(base, work / label, text))
    print(f"PLANT {cfg.stem} {label}: {len(got)} finding(s)")
    for x in got:
        print(f"PLANT   {x[:300]}")
