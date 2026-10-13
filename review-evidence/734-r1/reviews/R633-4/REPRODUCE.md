Run from an isolated checkout at `59354ffe75697e17a16fd117d9ba853e104394bc`.
Set `packet` to the packet directory. All disposable work goes below its `scratch/` directory.
The scripts require Python, Git, a YAML parser, and unprivileged namespace support.

The boundary launcher exposes system binaries and the read-only checkout. It exposes no credentials and disables network access. Its `/tmp` is the selected packet scratch directory. The image commands additionally overlay generated configuration and CSR output directories with scratch copies. Candidate runner code must only execute inside this boundary.

Use a fresh label for each invocation. The exact commands and exits from this review are in the receipt JSON files. Independent commands may run concurrently; keep total concurrency below sixteen.

```sh
python3 "$packet/scripts/run_boundary.py" scope-rerun -- python3 scripts/ci_scope.py --selftest
python3 "$packet/scripts/run_boundary.py" events-rerun -- bash -euc 'python3 scripts/ci_events.py --check; python3 scripts/ci_events.py --selftest'
python3 "$packet/scripts/run_boundary.py" runner-rerun -- python3 -c 'import yaml,subprocess; d=yaml.safe_load(open(".github/workflows/docs.yml")); s=next(s["run"] for s in d["jobs"]["docs-check"]["steps"] if s.get("name")=="Local act runner contract gate"); print(s,flush=True); subprocess.run(["bash","--noprofile","--norc","-e","-o","pipefail","-c",s],check=True)'
python3 "$packet/scripts/run_boundary.py" r01-rerun -- python3 /review/runner_mutations.py R01
python3 "$packet/scripts/run_boundary.py" r02-rerun -- python3 /review/runner_mutations.py R02
python3 "$packet/scripts/run_boundary.py" r03-rerun -- python3 /review/runner_mutations.py R03
python3 "$packet/scripts/run_boundary.py" before-rerun -- python3 /review/runner_mutations.py before
python3 "$packet/scripts/run_boundary.py" prior1-rerun -- python3 /review/prior_and_current.py round1
python3 "$packet/scripts/run_boundary.py" prior2-rerun -- python3 /review/prior_and_current.py round2
python3 "$packet/scripts/run_boundary.py" external-rerun -- python3 /review/prior_and_current.py external
python3 "$packet/scripts/integrity.py"
python3 "$packet/scripts/audit_public.py"
```

The prior probes under scripts/prior are unmodified copies of the named public scripts. Their hashes match public-provenance.json. The wrapper explains and grades the historical-oracle differences; the original scripts are not rewritten.

The documentation check uses a private environment at scratch/deps, installed from the checkout's hash-pinned tools/markdown/requirements.txt. The boundary mounts it at /deps. The full command is in receipts/documentation.json.

For the focused image build, install the authenticated SDK into a new scratch/sdk destination using scripts/ci_rv32_sdk.py. The boundary mounts it at /sdk. Set MILAN_RV32_CC=/sdk/bin/riscv32-linux-gcc inside the boundary. The accepted image command and the separate audit-control command are in receipts/linked-images-accepted.json and receipts/image-controls-final.json. The image-build labels must begin with linked-images; audit labels begin with image-controls so the generated-output overlays are enabled. No full builder bank is needed.

scripts/compare_images.py compares the five ELF pairs from scratch/linked-images-accepted/images. After a fresh reproduction using another label, select that directory in a copy of the comparison script. The built images, SDK and temporary probe trees are intentionally not published.

Expected gate return code is zero. For mutation drivers, zero means the intended failures were observed: corrected ordinary/flat forms reject R01/R02/R03; predecessor ordinary accepts R02 and predecessor flat rejects it. The rejected child commands' raw output is retained.

Initial quoting/anchor and read-only-output setup failures remain in the receipt population. They are not accepted validation evidence. sdk-install.log replaces only the local packet prefix with <packet>; the complete original installation log stays in unpublished scratch.

MANIFEST.sha256 uses paths relative to this packet. Validate it with `sha256sum -c MANIFEST.sha256` from the packet root.
