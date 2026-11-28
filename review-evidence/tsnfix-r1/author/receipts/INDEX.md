# receipts index (tsnfix-a867)

Head a8551cdd3cf715c52cca164a57d6d7f022e62c00 on main-gate-fixes from 5a07d9b7d87298f04b15aa28f0304ec88b0aef81. First 16 hex digits of each sha256, and what each shows.

| File | sha256 (16) | Shows |
|---|---|---|
| `coverage/arcs-5a07d9b.txt` | `1d3459bff1d13223` | per-line adp.c arcs at main: same layout as c3bff8f |
| `coverage/arcs-a795471.txt` | `813e997a30a4ec60` | per-line adp.c arcs before #40 (rng==0 guards at 180, 234) |
| `coverage/arcs-c3bff8f.txt` | `1d3459bff1d13223` | per-line adp.c arcs after #40 (leave_down ternary at 108) |
| `coverage/measure-5a07d9b-main.txt` | `9d202a176659b142` | main: adp 215/95, acmp 877/468; coverage.py rc 0 against the old ratchet (fraction compare) |
| `coverage/measure-a795471.txt` | `9006115cab8fcbf1` | PR #38 merge, before #40: adp 205/207 lines, 97/104 arcs raw |
| `coverage/measure-c3bff8f.txt` | `a77c4f75a9f1743b` | PR #40 merge: adp 215/217, 95/102 raw |
| `coverage/measure-ea4af6f.txt` | `1c777e552af78d45` | PR #28 merge: reproduces the old ratchet (adp 205/97, acmp 813/424) |
| `privacy/branch.txt` | `72d5734f522fd17e` | privacy gate on the branch head: pass (rc 0); self-test 17 controls |
| `privacy/main-5a07d9b.txt` | `327fb4062522f6f2` | privacy gate at main: 5a07d9b7 refused (rc 1); self-test 14 controls |
| `privacy/plants.txt` | `c899c906f65846a2` | 5 of 5 planted defects in copies of check_privacy.py refused by --selftest |
| `tools/arcs.py.txt` | `d32cb57f038eca44` | script used (copied as .txt) |
| `tools/env.sh.txt` | `96a86e78c0646b27` | script used (copied as .txt) |
| `tools/measure.sh.txt` | `203fd503a941d4bd` | script used (copied as .txt) |
| `tools/privacy_plants.py.txt` | `eda2dcc1201b8315` | script used (copied as .txt) |
| `tools/validate.sh.txt` | `01038e1a628ce823` | script used (copied as .txt) |
| `validate/coverage-controls.log` | `7137827cdebea07c` | validate.py log of that gate |
| `validate/coverage.log` | `87cf41c76bc41daf` | validate.py log of that gate |
| `validate/gates.json` | `84f0dd54d03d8d6d` | validate.py gate table: 28 gates, all rc 0 |
| `validate/mutation-controls.log` | `8de44f407fc0e6de` | validate.py log of that gate |
| `validate/mutation.log` | `9aa01050c2baa59d` | validate.py log of that gate |
| `validate/privacy.log` | `e10bac487b0cd678` | validate.py log of that gate |
| `validate/privacy-selftest.log` | `28473abf8ebf1af0` | validate.py log of that gate |
| `validate/static-analysis.log` | `1cc5d3e84563666e` | validate.py log of that gate |
| `validate/validate.out` | `68631fe5b3151bd2` | validate.py --graphs on head: toolchain line and every gate rc 0 |
