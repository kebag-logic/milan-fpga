Review R227-1 reproduction at source 3d90958f3a82ca2a9617112c107a22f332117e17.

Use the isolated clone with all three required submodules at their gitlinks. Scripts contain explicit review paths; neutralize those paths when publishing. `scripts/run.py` records argv, source head, UTC start, duration, status and logs under `raw/`. It sets only bytecode suppression, a disposable temporary directory and an eight-job ceiling. It never changes HOME, PATH or the real compiler selector. Every command below starts with `rtk`.

Run these commands from the source clone:

```sh
rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/504-r1-r227/scripts/verify_archive.py
rtk proxy python3 -B scripts/ci_rv32_sdk_selftest.py
rtk proxy python3 -B sw/builder/test_firmware_compiler.py --selftest
rtk proxy python3 -B scripts/ci_events.py --check
rtk proxy python3 -B scripts/ci_events.py --selftest
rtk proxy python3 -B scripts/check_baremetal_only.py --check
rtk proxy python3 -B scripts/check_baremetal_only.py --selftest
```

For the real SDK runs, use `scripts/run.py LABEL COMMAND ARGS...` as recorded in each `raw/LABEL.json`. The commands in `fresh-install.json`, `cache-verify.json`, `gate-compiled.json`, `gate-absent.json`, `store-probes.json` and `real-cache-probes.json` are exact reproductions. The fresh prefix must not already exist. The local archive is verified before use, and the installer verifies it again. The disposable SDK was removed after measurements; only its receipt/inventory and command logs are retained. Reinstall it before replaying compiler or real-cache probes.

Independent probes are executable Python under `scripts/`: `workflow_probes.py` mutates parsed workflow copies, `installer_probes.py` mutates an installer module in memory, `store_probes.py` captures the actual gate closures after the pristine baseline and compiles five additional firmware variants, and `real_cache_probes.py` corrupts/restores only the disposable installation. They never edit repository source. `source_boundary.py` checks existing executable gate semantics against the base and the downloaded hosted gate. `integrity.py` proves bytes, kinds, executable modes, index records and required gitlinks independently of Git's clean-status cache.

The public source evidence was fetched only from immutable 7ada4134707514f5622246e535b98e66a005e98d, under review-evidence/504-r1/manager. `public/evidence-tree.json` provides the Git blob identities. Every fetched manager blob was recomputed using SHA1("blob " + length + NUL + content). Source and issue records are under `public/`; no other review reports or private author material were opened.

Hosted logs came from read-only `gh api` endpoints, with `--allow-escape-sequences` for log bodies, for docs-check job 106851428580 and elaborate job 106851429374. Run metadata and job records are retained. Both jobs belong to source head 3d90958f3a82ca2a9617112c107a22f332117e17 but check out merge c0b2b7cc067ece28e3124f94ccd9ee45c91b85e3. The observed hosted tree and the differing builder file are retained. `raw/source-boundary.json` names the compared artifacts. `raw/hosted-*-selected.log` carries line-numbered excerpts; complete two-job logs are in `public/`. These are read-only receipts, not scripts to execute.

The first hosted log retrieval was refused by gh's terminal-escape filter and was repeated with its explicit output flag. The initial hosted blob comparison found the base-side #478 additions to test_builder.py; the subsequent comparison preserves that difference and proves gate 1b itself unchanged. Neither observation was hidden or relabeled as a source failure.
