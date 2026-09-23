# R248-2 portable scripts

Placeholders in published receipts and in `bank_static.txt`: `<clone>` is a
clone at the reviewed head, `<packet>` is this packet directory, `<shared-tmp>`
is a host scratch root, and `$HOME` is the user's home. Substitute them before
rerunning.

| script | purpose |
|---|---|
| `integrity.sh <clone> <head> <tree>` | HEAD/tree ids, index equals HEAD, every tracked blob's bytes and mode, clean status, and the three required submodule gitlinks at their pins |
| `run_bank.sh <clone> bank_static.txt <out> [jobs<=8]` | runs the focused command bank and keeps the output and exit status of each command |
| `yaml_comment_only.py <repo> <old> <new> <path>` | proves a workflow change is comment-only: parsed-YAML equality, non-comment lines, run bodies |
| `contents_meaning.py <repo> <old> <new> <page>` | Contents entries: labels, anchors, anchor resolution, separators, U+2014 outside labels, word-level description diff |
| `mutation_probe.py <clone> <scratch> <probe-id>` | one fault per disposable `cp -a` copy (M1-M8), then the shipping unit and real-gate controls |
| `empty_arm_probe.py <work>` | (cwd = checkout) shows which refusal text satisfies the empty-image arm (S1) |
| `pp_shadow_probe.py <work>` | (cwd = checkout, `PYTHONDONTWRITEBYTECODE=1`) KL_pp_shadow cold, warm, changed-ROM and uncached runs |
| `sanitize_receipts.py <packet> <clone> [prefix=label ...]` | replaces host paths in receipts with placeholders |
| `make_manifest.sh <packet>` | writes and verifies `MANIFEST.sha256` |
