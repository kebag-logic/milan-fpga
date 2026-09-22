This packet belongs to reviewer R252, round R252-1, for exact head `e0c43b03f31d6c1220dd05a110e4bb30029233a0`. Run commands from the packet directory, or supply its absolute script paths. All shell invocations are prefixed with `rtk`; scripts also prefix their subprocess calls with `rtk proxy`. No script posts or modifies GitHub state.

The actual focused build argv, working directory, UTC start/end, exit and stream hashes are in [raw/pp-top-full.stdout.log.command.json](raw/pp-top-full.stdout.log.command.json). Its fully expanded recipe is in [raw/pp-top-dry-run.log](raw/pp-top-dry-run.log). The only Makefile runtime override beyond the installed tool selector is `VFLAGS` with the existing `-j 0` changed to `-j 8`; no source file is edited.

The packet is relocatable: scripts derive the packet root from their own path. For a different exact-head clone, set `R252_CHECKOUT` for the invocation. `R252_PARENT` identifies a read-only clone containing the immutable parent policy objects; it is needed only when reacquiring those objects. `R252_VERILATOR` may select the same pinned installed-tool shell-selector layout at another location. The recorded machine paths in raw logs are original evidence and have not been rewritten.

Independent required parser controls, using already captured and hash-verified immutable parent code:

```sh
rtk proxy env R252_CHECKOUT=/path/to/exact-head-clone python3 -B scripts/parser_controls.py
```

Independent complete pp_top target, including fixture guards and locale regression, capped at eight compile jobs:

```sh
rtk proxy env R252_CHECKOUT=/path/to/exact-head-clone R252_VERILATOR=/path/to/pinned-tool-bin/verilator python3 -B scripts/focused_build.py
```

The supplied installed selector was `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`. The focused script reads and hashes it, resolves its driver/forwarder/final ELF, checks both version results, and never changes the installation. It writes only ignored build products in the chosen review clone and evidence in this packet. Use a fresh disposable exact-head clone for reproduction. The recorded build already passed; rerunning a complete donor, parent or Yosys bank is not part of this reviewer procedure.

Read-only reacquisition, in dependency order, when fresh public downloads are needed:

```sh
rtk proxy python3 -B scripts/collect.py public
rtk proxy env R252_PARENT=/path/to/read-only-parent-clone python3 -B scripts/collect.py policy
rtk proxy python3 -B scripts/collect.py evidence
rtk proxy python3 -B scripts/collect.py source
rtk proxy python3 -B scripts/collect.py hosted
rtk proxy python3 -B scripts/hosted_logs.py
```

`collect.py public` stores the issue/PR/assignment/history and exact public trees. `policy` verifies trusted Git bytes against public Git blobs. `evidence` downloads only the selected public factual native receipts/logs and integrity records. `source` records immutable donor files, diff and history. `hosted` and `hosted_logs.py` inspect actual runs only. Every API request is GET. Raw job logs use gh's explicit `--allow-escape-sequences` output option and are saved as files, without rendering terminal control codes. The earlier refused request is retained separately.

Audit the supplied manager/native evidence, actual hosted execution and checkout integrity without rerunning those banks:

```sh
rtk proxy env R252_CHECKOUT=/path/to/exact-head-clone python3 -B scripts/audit_evidence.py
rtk proxy python3 -B scripts/hosted_audit.py
rtk proxy env R252_CHECKOUT=/path/to/exact-head-clone python3 -B scripts/integrity.py reproduced-final
```

The manager's exact nine commands are in [evidence/source/manager/full-native.json](evidence/source/manager/full-native.json), under the recorded scoped environment; their original exits/times are in `full-native/results.json`. Their publication uses portable `$VALIDATION`, `$VALIDATION_STORAGE`, `$WORKSPACE_HOME` placeholders. They were inspected, not executed by R252. Native logs `01` through `09` correspond in order to tool identity, historical PR13 fetch, HDL lint, all suites, make check, matrix, full donor Yosys, nvm figures, and base/head whitespace.

Original parent gate receipt and output were acquired from exact public tree `ff1ebf16263590b0cdca32a1e74ffc4195f0aa9e`, under `review-evidence/400-403-r1/author/idiom-cpp-final.{json,log}`. The public directory response and per-blob command receipts are stored in `public/`. Only these factual original native records were read; no author implementation notes were consumed.

Final packet creation and verification:

```sh
rtk proxy python3 -B scripts/finish_bundle.py
rtk proxy sha256sum --check MANIFEST.sha256
```

`finish_bundle.py` rechecks exact source bytes/kinds/modes/index, builds the reviewer-owned ledger, removes only this packet's generated Python caches, and hashes every delivered regular artifact. `MANIFEST.json` excludes itself and `MANIFEST.sha256` to avoid recursion; `MANIFEST.sha256` also authenticates `MANIFEST.json`. Reproduction updates receipts/manifests, so copy the packet first if the delivered originals must be retained unchanged. `focused_build.initial.py` preserves the initial tool-resolution attempt and is archival only.
