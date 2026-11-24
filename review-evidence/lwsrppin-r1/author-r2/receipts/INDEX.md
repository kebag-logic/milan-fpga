# Receipts index, round 2 (head ed7df79c6f87a4172c885f268ad67629bd56c4eb)

Every file here is under 200 KB, and none is compressed. The raw logs carry local paths. Two logs over 200 KB are
trimmed to head and tail, with the full size and sha256 noted in place (`twin/build-trimmed.log`,
`docs/docs-gates-2__15-trimmed.log`). Scripts are in `../scripts/`: `census.py`, `r1_faults.py` and
`docs_gates_r2.py`. The reviewers' scripts were run unchanged from their packets, except `probe_twin_11.py`, whose
one-line change is `selftest/probe_twin-adapt.diff`.

- `selftest/`, at ed7df79c (`head`: the sha, then the count of modified tracked files, 0):
  - `twin_mrp-selftest.txt`: `OK (11 checks)`.
  - `twin-mutants.txt`: R913-1's `twin_mutants.py`, 9 of 9 CAUGHT.
  - `r1-faults.txt`: round 1's 5 planted faults.
  - `census.txt`: outside count against the printed count.
  - `probe_twin-unchanged.txt` and `probe_twin-11.txt`: R914-1's probe as published, and with its pinned 9 set
    to 11.
  - `txlaf-registrar-probe.txt`: R913-1's probe.
  - `py-idiom*.txt`: the Python idiom gate and its self-test.
- `twin/`, Verilator 5.050:
  - `build-trimmed.log`: `make -j24 build-twin`.
  - `twin.log`: `make twin`.
  - `plants-full.log`: `make -j2 twin-plants`, one invocation, the receipt of record.
  - `plants-a.log` and `plants-b.log`: the same rule split into two invocations.
  - `times.txt`: rc, start and end, head, Verilator.
- `docs/`, the `docs.yml` steps at ed7df79c:
  - `summary.txt`: 44 steps, each rc 0.
  - `<job>__<step>.log`: each step's output, with `-md` for the pinned-renderer runs.
  - `head`.
- `images/`:
  - `diff-stat.txt`: the image-input diff, empty, and the full delta.
  - `elf-hashes.txt`: sha256 of every ELF/bin/hex in the two `plat_ledger.py` builds; 28 IDENTICAL, 0
    DIFFERENT.
  - `plat_ledger-*.log` and `times.txt`.
- `pr-body-live-before.md`: the live PR #992 body at dbba60e6, read before writing `../PR-BODY.md`.

| File | Bytes | sha256 (first 16) |
|---|---:|---|
| `docs/docs-check-no-git__3.log` | 225 | `00c4cd62094de1fd` |
| `docs/docs-gates-0__11.log` | 128 | `0483501771f7edf2` |
| `docs/docs-gates-0__12-md.log` | 139 | `5ab607aa47f3967c` |
| `docs/docs-gates-0__13.log` | 167 | `06dde9a3bc8e4ad9` |
| `docs/docs-gates-0__14.log` | 242 | `79dce4dc64e4d578` |
| `docs/docs-gates-0__15.log` | 146 | `1f719750a8609052` |
| `docs/docs-gates-0__16.log` | 227 | `88d83848aecf8145` |
| `docs/docs-gates-0__17.log` | 241 | `af9493d0e4acd65e` |
| `docs/docs-gates-0__18.log` | 125 | `17d1d2360a98e818` |
| `docs/docs-gates-0__19.log` | 1,568 | `b703a4a6f525637d` |
| `docs/docs-gates-0__20.log` | 118 | `99cb09ed317195a6` |
| `docs/docs-gates-0__22.log` | 2,752 | `c8f09b54284ebf9f` |
| `docs/docs-gates-0__23.log` | 3,293 | `862838344ece59e4` |
| `docs/docs-gates-0__26.log` | 115 | `621eed75d781be28` |
| `docs/docs-gates-0__29.log` | 51,493 | `8789832f85a5af15` |
| `docs/docs-gates-0__3.log` | 964 | `b0e263f59cb9541d` |
| `docs/docs-gates-0__30.log` | 20,246 | `8dc5ba0d3ea8973a` |
| `docs/docs-gates-0__31.log` | 1,192 | `644dbaf9db7fc996` |
| `docs/docs-gates-0__32.log` | 52,046 | `9364b7776a3bbafc` |
| `docs/docs-gates-0__33.log` | 4,794 | `d3e9263bebd26fb0` |
| `docs/docs-gates-0__34.log` | 3,453 | `f978e53937335528` |
| `docs/docs-gates-0__35.log` | 40,599 | `417ab22513910597` |
| `docs/docs-gates-0__36.log` | 5,040 | `cd027477f9fdbe55` |
| `docs/docs-gates-0__37.log` | 12,531 | `5fb874bb636730c9` |
| `docs/docs-gates-0__38.log` | 2,745 | `d2f50d329a7d5ca6` |
| `docs/docs-gates-0__39.log` | 29,814 | `fd66f6d74af5c261` |
| `docs/docs-gates-0__40.log` | 3,972 | `7c1d8db5986b41c4` |
| `docs/docs-gates-0__41.log` | 3,173 | `cf68b72f86b70cef` |
| `docs/docs-gates-0__42.log` | 4,735 | `df9f1e6d666f4b4b` |
| `docs/docs-gates-0__43.log` | 2,992 | `2d47eb10efad523e` |
| `docs/docs-gates-0__44.log` | 2,696 | `a57f331056f1f93e` |
| `docs/docs-gates-0__45.log` | 101 | `a79d872b27a36c20` |
| `docs/docs-gates-0__46.log` | 128 | `1a15e66a07892f54` |
| `docs/docs-gates-0__47-md.log` | 196 | `0644dd11044a1a36` |
| `docs/docs-gates-0__48.log` | 129 | `185c9f506448e385` |
| `docs/docs-gates-0__49.log` | 3,596 | `9f126bf9dfc7cb55` |
| `docs/docs-gates-0__50.log` | 26,735 | `061ec02e853d0ebc` |
| `docs/docs-gates-0__51.log` | 10,344 | `da8820ae7f0263bd` |
| `docs/docs-gates-0__52.log` | 29,010 | `e174e6e39fc1fac6` |
| `docs/docs-gates-0__53.log` | 3,749 | `be979dd5dcdee951` |
| `docs/docs-gates-0__55.log` | 139,623 | `208529965b0b729a` |
| `docs/docs-gates-2__15-trimmed.log` | 4,204 | `e0ad91adfb87714c` |
| `docs/docs-gates-2__16.log` | 131,281 | `f2bebd6b0fd752dc` |
| `docs/head` | 41 | `bd51844114247d4d` |
| `docs/summary.txt` | 2,305 | `038da3836f29aa79` |
| `docs/wire-accountability__4.log` | 5,076 | `de066064fa209d5a` |
| `images/diff-stat.txt` | 888 | `e257862358e671ac` |
| `images/elf-hashes.txt` | 4,163 | `4f387838f2a33f45` |
| `images/plat_ledger-dbba60e6.log` | 14,111 | `c5b8e0a71eb5840d` |
| `images/plat_ledger-ed7df79c.log` | 14,111 | `eea3b75d4eeabd3e` |
| `images/times.txt` | 224 | `9a435896952fb4af` |
| `pr-body-live-before.md` | 8,817 | `9637fed479d69601` |
| `selftest/census.txt` | 457 | `279944cf0a920a1c` |
| `selftest/head` | 43 | `addbf83d50779940` |
| `selftest/probe_twin-11.txt` | 1,035 | `3790484d1151e1a4` |
| `selftest/probe_twin-adapt.diff` | 99 | `47a21f137308d6c9` |
| `selftest/probe_twin-unchanged.txt` | 602 | `af470a66ebf61788` |
| `selftest/py-idiom-selftest.txt` | 2,536 | `68a882038dd04b97` |
| `selftest/py-idiom.txt` | 466 | `37268786694c11ab` |
| `selftest/r1-faults.txt` | 681 | `3b3f6ae18b9965c5` |
| `selftest/twin-mutants.txt` | 1,262 | `a686473b988dfeb8` |
| `selftest/twin_mrp-selftest.txt` | 39 | `e682cf81f8630354` |
| `selftest/txlaf-registrar-probe.txt` | 53 | `f850dbfdf9c92ecf` |
| `twin/build-trimmed.log` | 63,428 | `dfc7a00db7eb9e06` |
| `twin/plants-a.log` | 27,785 | `3ebc456acf3c48a4` |
| `twin/plants-b.log` | 61,360 | `61f04e3adc0f89c7` |
| `twin/plants-full.log` | 66,238 | `8a2bd123732f94ab` |
| `twin/times.txt` | 569 | `d94355cdee2fc6a7` |
| `twin/twin.log` | 23,498 | `7460dd614aa9cace` |
