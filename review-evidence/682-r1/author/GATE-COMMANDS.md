# Gate commands and receipts

Commands below are the executed shell text. Log contents remain outside this packet; each receipt gives their digest and byte size.

## markdown 01: markdown-docs

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/markdown/01-markdown-docs.log`; 128 bytes; SHA-256 `1855ea65a42d5b44e13f41fb7a5b000756bd1fe553a3cc382594c5bbfddf7b19`.

## markdown 02: markdown-toc-controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/markdown/02-markdown-toc-controls.log`; 38 bytes; SHA-256 `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32`.

## markdown 03: markdown-anchor-check

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --verify-anchors
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/markdown/03-markdown-anchor-check.log`; 64 bytes; SHA-256 `f91f24231f091b6e2dbd4098a9eb4c521a2b1b21ef0718fef2b429eb732e5482`.

## markdown 04: markdown-toc-check

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/markdown/04-markdown-toc-check.log`; 94 bytes; SHA-256 `bfc48b94454dee4821468e961b93a636054c123d2c62c18aa266b386e638eab8`.

## parent 01: render-full

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 2.

Working directory: `$LANES/682-pp-pin3/tb/verilator/milan_dp_render`.

```sh
make -j8 VERILATOR_JOBS=2 tdm8render-mutants
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/parent/01-render-full.log`; 141,993 bytes; SHA-256 `c321acd49c949874c40b6f57127b49acc0b033964a4dc7185bd6571f719635fe`.

## parent 02: parent-sweep-cancelled

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 143.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash scripts/run_all_suites.sh $VALIDATION_STORAGE/682-a554/parent-suite-logs
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/parent/02-parent-sweep.log`; 471 bytes; SHA-256 `90728c84be50db98e6b12d414c7e1e9dd239b1eb7d084c4b24a6c0dd6c0a2bc0`.

## patch 01: notification-patch

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=2 notify
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/patch/01-notification-patch.log`; 103,057 bytes; SHA-256 `b5eaa0aff09b0054da6ae31583edc4cb637dc9f3b24b0dd6bf32fc6229eb6474`.

## processors 01: processor-sweep

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
PATH=$VALIDATION_STORAGE/661-a537/sv2v013/bin:$PATH bash protocol-processor/scripts/run_suites.sh
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/processors/01-processor-sweep.log`; 1,750 bytes; SHA-256 `b37107cafb110e9a76737445437ee30a81673f33ec403875c8c27b1f5840c64a`.

## processors 02: gptp

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
make -C gptp-processor -j8 contract tb lint
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/processors/02-gptp.log`; 42,747 bytes; SHA-256 `c7cba7372455f9a5c0cd31807ff1c50b1bb922ecb43247486a98eaee06beabde`.

## processors 03: bdd

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3/tests`.

```sh
behave --no-capture -f plain
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/processors/03-bdd.log`; 196,684 bytes; SHA-256 `708a8f56c3c43e12e0fc84bd63dbd0a135188a359a20312056dbf69106f9f61c`.

## processors 04: builder-elaboration

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/processors/04-builder-elaboration.log`; 101,688 bytes; SHA-256 `ac5c5fa8dd6edef09c7f75be7a1146e467a02a48f231e8a7f46a967f4655d33d`.

## resources 01: route-1x1

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/work/ax7101-clean/gateware --endpoint route-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/resources/01-route-1x1.log`; 592 bytes; SHA-256 `d01ac95849fa6f3bbac38dd338f42b1708646034da14bc274ca751201f18d677`.

## resources 02: ooc-1x1

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/work/ax7101-ooc --endpoint ooc-1x1
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/resources/02-ooc-1x1.log`; 371 bytes; SHA-256 `821d61a6c19bf76567ecfc5a6bdc4638fc29e174e7516d02d63f1a1caf79ad02`.

## resources 03: ooc-8x8

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check $VALIDATION_STORAGE/682-a554/work/ax8x8-ooc --endpoint ooc-8x8
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/resources/03-ooc-8x8.log`; 370 bytes; SHA-256 `3e3bdf6207b3261d3744277838c505d9b261286aa6ee6ed09dc4e0b3379d91a3`.

## resources 04: policy

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/resources/04-policy.log`; 27 bytes; SHA-256 `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0`.

## stable-header 01: yosys-stable-header

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --top milan_csr --top milan_datapath --results $VALIDATION_STORAGE/682-a554/yosys-stable-results
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/stable-header/01-yosys-stable-header.log`; 3,778 bytes; SHA-256 `7dd0a6c4404a61b3f913455926cdbbb8b8910d393f1eda27321d64c3f25fa6f2`.

## stable-header 02: fast-elaboration-stable-header

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/stable-header/02-fast-elaboration-stable-header.log`; 369 bytes; SHA-256 `31e3d34013f6ed2aaedfbe0548c5b96406835e8a410b2e4ab355fdb6ae5ae6bf`.

## stable-header 03: render-four-cases-stable-header

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 1.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 $VALIDATION_STORAGE/682-a554/render-recheck.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/stable-header/03-render-four-cases-stable-header.log`; 437 bytes; SHA-256 `2626f1c1a06e51ff3a5556a8723907878270ff191cfe05386159b689cf219729`.

## synthesis 01: lint

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/lint_rtl.py --check --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/01-lint.log`; 14,888 bytes; SHA-256 `fdfaa1c6d9058fd1f1d30ef75e8590d1e633c21b21ff6fb7455e0542dc99123a`.

## synthesis 02: pp-sources

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/pp_srcs.py --check --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/02-pp-sources.log`; 955 bytes; SHA-256 `fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a`.

## synthesis 03: scope

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_scope.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/03-scope.log`; 6,517 bytes; SHA-256 `077525191c73646a55517ab5e2ae89895e6067da0538bd13cf7ad3d3d556d7b7`.

## synthesis 04: yosys

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --results $VALIDATION_STORAGE/682-a554/yosys-results
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/04-yosys.log`; 6,182 bytes; SHA-256 `12e1d99e0369de504a263daadaa6ac28b4d14badd2b34cbc485cd58d8ba3d290`.

## synthesis 05: yosys-tally

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --list > $VALIDATION_STORAGE/682-a554/yosys-expected.txt
python3 scripts/yosys_tally.py $VALIDATION_STORAGE/682-a554/yosys-results --expected $VALIDATION_STORAGE/682-a554/yosys-expected.txt --require-structural
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/05-yosys-tally.log`; 49 bytes; SHA-256 `ca886fa4ca355ab8ad0ad261ad5d583dc524bc0f89466f52032de7cfc3d667c4`.

## synthesis 06: fast-elaboration

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
bash syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/06-fast-elaboration.log`; 369 bytes; SHA-256 `31e3d34013f6ed2aaedfbe0548c5b96406835e8a410b2e4ab355fdb6ae5ae6bf`.

## synthesis 07: dp-source-controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/dp_srcs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/07-dp-source-controls.log`; 36 bytes; SHA-256 `d1d5a4fa150962bc8cd53e563cde50da65cc8cfeee212d82e10bc293848bd428`.

## synthesis 08: ooc-tcl-controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/ooc_tcl_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/08-ooc-tcl-controls.log`; 45 bytes; SHA-256 `c8115f5fe4b9eadf2c9d635505578b1b267023a61a32f8aebff7ad568f0b21eb`.

## synthesis 09: baseline-controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/09-baseline-controls.log`; 3,552 bytes; SHA-256 `7b572de360c65012b592df86bf736a48292cb67c06ffd782eb32b0f1dc61d0ed`.

## synthesis 10: baseline-mutants

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline_mutants.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/10-baseline-mutants.log`; 1,262 bytes; SHA-256 `c61da14188c61f28ddce19916a58bcf07e368851751321f9f498dcc6385d2dc4`.

## synthesis 11: baseline-reports

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_baseline_reports_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/11-baseline-reports.log`; 96 bytes; SHA-256 `e2b4102612b453b76c0af51f99091bbb1e1a36adafecc9f6c6b8eb345bbc81fe`.

## synthesis 12: resource-controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/12-resource-controls.log`; 25,156 bytes; SHA-256 `160855c6f5d252fde05cf983fe3dd19877501d6587e740deb60fe5ddf7017800`.

## synthesis 13: resource-mutants

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate_mutants.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/13-resource-mutants.log`; 5,862 bytes; SHA-256 `e566898c471e0694e1e7c16accc1c1e30b6b7187dbf9b3282829a8dfd3e4fdf4`.

## synthesis 14: resource-baseline

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/14-resource-baseline.log`; 27 bytes; SHA-256 `2114d909e60add091220b415987d4409a611d70c9e84f1bb9e0ae12d6a2f14a0`.

## synthesis 15: dp-sources

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null
python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/15-dp-sources.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## synthesis 16: yosys-ooc-controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/yosys/ooc_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/16-yosys-ooc-controls.log`; 43 bytes; SHA-256 `d4febc14ba490cf79a72567d657e1653d21792043ae463564d52c831f69179e0`.

## synthesis 17: yosys-cache-controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 syn/yosys/cache_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/synthesis/17-yosys-cache-controls.log`; 190 bytes; SHA-256 `d8e090cf8c0c656d14381ecbb41901c83ad1870f0f38fed8b382815197e4dfa5`.

## vendor 01: xvlog

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
test "$(git -C protocol-processor rev-parse --show-toplevel)" = "$PWD/protocol-processor"
python3 scripts/xvlog_gate.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/acceptance/vendor/01-xvlog.log`; 721 bytes; SHA-256 `1c0d7a7bf120fe6c8d00aee69f966596e243b137fea381269c3dc1435c82e8d6`.

## docs-workflow 01: Build the validated HDL reference

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 -m pip install --quiet --require-hashes \
  -r tools/hdl_reference/requirements.txt
python3 scripts/gen_hdl_reference.py --selftest
python3 scripts/gen_hdl_reference.py \
  --output "$RUNNER_TEMP/milan-hdl-reference"
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/01.log`; 802 bytes; SHA-256 `8c67dd5552eb6fa9b1ab4097af616dba9f7da1ef6a1668d173ef2461cf5cac37`.

## docs-workflow 02: Install the python gate dependencies

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/02.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 03: Install the pinned Markdown renderer

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet --cache-dir ~/.cache/milan-markdown-pip \
  --require-hashes -r tools/markdown/requirements.txt
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/03.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 04: Install diagram gate dependencies

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends librsvg2-bin
python3 -m pip install --quiet wavedrom==2.0.3.post3
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/04.log`; 2,325 bytes; SHA-256 `df8eb0d10673d7555cab4c4b8ac7dff1b6e8e4e09ebbe3ea9f76bcf1791d247e`.

## docs-workflow 05: Link health, wording, dead-reference and local-info gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/docs_check.py
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/05.log`; 128 bytes; SHA-256 `1855ea65a42d5b44e13f41fb7a5b000756bd1fe553a3cc382594c5bbfddf7b19`.

## docs-workflow 06: Added-line em-dash gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
case "$EVENT_NAME" in
  pull_request)
    if [ -z "$PR_BASE_REF" ]; then
      echo "the pull_request event names no base branch"; exit 2
    fi
    git fetch --quiet origin "$PR_BASE_REF"
    base="$(git merge-base HEAD FETCH_HEAD || true)"
    ;;
  push) base="$PUSH_BEFORE_SHA" ;;
  *) echo "a $EVENT_NAME event carries no base to judge from"; exit 2 ;;
esac
if [ -z "$base" ] || [ "$base" = 0000000000000000000000000000000000000000 ]; then
  echo "the $EVENT_NAME event names no base commit"; exit 2
fi
git cat-file -e "$base^{commit}" 2>/dev/null || git fetch --quiet --depth=1 origin "$base"
python3 scripts/check_em_dash.py --base "$base"
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/06.log`; 140 bytes; SHA-256 `fe5258cea2c6c320a26a215ea1fd5689856322fc5fe16e0b0f03e45ac62889bb`.

## docs-workflow 07: Concise audience documentation gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_gptp_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/07.log`; 167 bytes; SHA-256 `05d6ef2302a6c0467ad437209233733e93bcb2941539103e26c51b988a28637a`.

## docs-workflow 08: Audience diagram no-drift gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/DOC_MAP.gen.py --check
python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/08.log`; 242 bytes; SHA-256 `79dce4dc64e4d57851e37c5bac0a829304d65207659bb65049e11b7d0683f069`.

## docs-workflow 09: Product solution source-fact gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_solution_docs.py
python3 scripts/check_solution_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/09.log`; 146 bytes; SHA-256 `9ef43cc924919e10ccb30a9419819d20b849d787a8f37fcabba22e2159d3167d`.

## docs-workflow 10: Verified submodule documentation gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/10.log`; 227 bytes; SHA-256 `cd9f3e7404ce8e884eded8567a1b2560dc22cc7a4b5796601edb295cb725cc64`.

## docs-workflow 11: HDL timing diagram no-drift gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_wavedrom.py --selftest
python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/11.log`; 241 bytes; SHA-256 `af9493d0e4acd65eb64ba2bbe7103a2c6f957ecca650a938cdc18d70396a57ea`.

## docs-workflow 12: Published diagram PNG gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/12.log`; 125 bytes; SHA-256 `17d1d2360a98e818f8706a8165affff7c873cb06b4fe8db4c48300e103e51c1e`.

## docs-workflow 13: Milan feature-status consistency gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_feature_status.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/13.log`; 1,500 bytes; SHA-256 `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184`.

## docs-workflow 14: Traceability matrix no-drift gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 docs/traceability/gen_module_matrix.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/14.log`; 118 bytes; SHA-256 `d0be3b6428ae2079134f2a21b2972c524a26103b0e9c8b64039bb24ae22797dc`.

## docs-workflow 15: Fetch the builder source dependencies

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/15.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 16: Imported gPTP documentation gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_gptp_docs.py --with-submodule
make -C gptp-processor docs
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/16.log`; 2,736 bytes; SHA-256 `2ee7c1389f730f5d60e04123c4e7b04cd555da58393dccf27b73d1265fc5d481`.

## docs-workflow 17: Code-quality measurement self-tests

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/17.log`; 3,293 bytes; SHA-256 `862838344ece59e4179fd4bcfe04f85ee320f0601c325014b2509717db13368b`.

## docs-workflow 18: Install the pinned sv2v release

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
ver=v0.0.12
sha256=ff8c9eea5bc029b372fb4953427625cddb7cf7e58c1240623ac9f260818d5a00
url="https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip"
curl -fsSL "$url" -o /tmp/sv2v.zip
echo "${sha256}  /tmp/sv2v.zip" | sha256sum -c -
unzip -q -o /tmp/sv2v.zip -d /tmp/sv2v
sudo install -m755 "$(find /tmp/sv2v -name sv2v -type f | head -1)" \
  /usr/local/bin/sv2v
sv2v --version
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/18.log`; 31 bytes; SHA-256 `176b5effd5ab230db92a3088fc5e8a688744dc1203991c6e71b25f2a29925e0d`.

## docs-workflow 19: Bare-metal scope gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/19.log`; 115 bytes; SHA-256 `a2aa0a6e8e4cffd50e40ee5208c5b9e98ab667f9fb8f89ca930c8274c4ac13ea`.

## docs-workflow 20: Install and verify the pinned RV32 SDK

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/20.log`; 8,119 bytes; SHA-256 `b29bf9682b6fce52b4a58d42797aac5532d03328b8550fc1c08b4db39ba0aa16`.

## docs-workflow 21: Compiler-absent firmware controls

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
set -euo pipefail
python3 sw/builder/test_firmware_compiler.py --selftest
python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/21.log`; 52,026 bytes; SHA-256 `31311091195e0b2febb4e424c21b307a8f91e755701f82bd6de6dc23053eecc3`.

## docs-workflow 22: End-station builder gates

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 sw/builder/test_builder.py --require-rv32
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/22.log`; 101,744 bytes; SHA-256 `0c963e5da85e7e56493a2015463867526c2e538c62f3a3624d509abb2813e5e6`.

## docs-workflow 23: NVM record-space gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_record_space.py
python3 scripts/check_nvm_record_space.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/23.log`; 9,588 bytes; SHA-256 `7969fb65ae1ea9d608146bed63d697587402331dc1efa2c128e61861a7f6493e`.

## docs-workflow 24: Capture measurement census and clock gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_nvm_capture.py
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/24.log`; 324 bytes; SHA-256 `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439`.

## docs-workflow 25: Saved-state writer gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/25.log`; 5,189 bytes; SHA-256 `cba18482dbf27c70ee56b28a8fbbe7bfdc2cc49b4644a42daa5ad4db8f6d4972`.

## docs-workflow 26: SoC source-list gate (Vivado would fail 40 min in without this)

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_soc_sources.py
python3 scripts/check_soc_sources.py --selftest
command -v tclsh >/dev/null || {
  sudo apt-get update -qq
  sudo apt-get install -y --no-install-recommends tcl
}
python3 sw/litex/iob_pack_selftest.py
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/26.log`; 4,733 bytes; SHA-256 `7c34f57b723fa707a2eadc1915b61980ed407fd0cf480238032e391030f053f9`.

## docs-workflow 27: RTL source-list drift gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_rtl_source_lists.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/27.log`; 3,453 bytes; SHA-256 `be8805dc2fee50eddcf0b966ea5728febdeed2e7b9f288ba358f41c1fe4b7041`.

## docs-workflow 28: Boundary-unit naming ratchet

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_naming.py --check
python3 scripts/measure_naming.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/28.log`; 40,634 bytes; SHA-256 `3d6d291b5e41999df546421642ddf9cc98237dcdea8d047c54edf0e9a7089f3e`.

## docs-workflow 29: Port contract gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_port_contracts.py
python3 scripts/check_port_contracts.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/29.log`; 5,040 bytes; SHA-256 `ce53539b1c4806c705ca06eead5c465effd50782d8393272c91afcbdd93d59d1`.

## docs-workflow 30: Fail-fast ratchet

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_fail_fast.py --check
python3 scripts/measure_fail_fast.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/30.log`; 12,682 bytes; SHA-256 `3fbed56aa0724496465ce6f185d931ddb1a3ee49bb28a1ff77e1051981a700dd`.

## docs-workflow 31: TODO ownership gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_todo_ownership.py
python3 scripts/check_todo_ownership.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/31.log`; 2,745 bytes; SHA-256 `c7cebf27e539cbe5d0295ecba605c3ce8e0a1f8bf9778e4b8cba9a88dc320148`.

## docs-workflow 32: Test-evidence ratchet

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/32.log`; 20,294 bytes; SHA-256 `6b2fe505e18858187f5af6b8239b9a7b45802285938772b34cec08e7409cdfad`.

## docs-workflow 33: Mechanical hygiene ratchet

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_hygiene.py --check
python3 scripts/check_hygiene.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/33.log`; 3,845 bytes; SHA-256 `6714a11ec896bb22f0d4fb29db313e326d7422ca958e7bafe50bdc875752b045`.

## docs-workflow 34: SystemVerilog idiom gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sv_idiom.py
python3 scripts/check_sv_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/34.log`; 3,173 bytes; SHA-256 `ccd900273b796fdfcf74e586f952eadfc9f6f6b1ad448b891183f939a49df728`.

## docs-workflow 35: C and C++ idiom gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_cpp_idiom.py
python3 scripts/check_cpp_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/35.log`; 3,908 bytes; SHA-256 `0a5f98004e7aa896ac8aa982d57894040d9d5bc3580eed03f05715d73205125f`.

## docs-workflow 36: Python idiom gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/36.log`; 2,992 bytes; SHA-256 `c6f12b3648d5aad5380db456640c8793209c9d6467e7f99cbb3e640477704b96`.

## docs-workflow 37: Shell idiom gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sh_idiom.py
python3 scripts/check_sh_idiom.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/37.log`; 2,696 bytes; SHA-256 `a57f331056f1f93e369a05fc919fd7d91a98638253282a970a118711a46e20e1`.

## docs-workflow 38: CI event and SHA contract gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/38.log`; 142,457 bytes; SHA-256 `fc0f707815e677bcb6f52767edce2507cd0e94f89b4f68c1f55d9c6645a79a25`.

## docs-workflow 39: Local act runner contract gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/act_ci.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/39.log`; 36,483 bytes; SHA-256 `876a6eca5975005e4e1d1ddddad9f74d2443039a10df8b7f590e4c781632fdab`.

## docs-workflow 40: Doc cited-path gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_doc_paths.py
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/40.log`; 85 bytes; SHA-256 `851fa6d9e1f2a70f98dfd1933a7cf29b5a16789776298616cbd35d6eb71c618f`.

## docs-workflow 41: Archive integrity gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_archive.py
python3 scripts/check_archive.py --selftest
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/41.log`; 128 bytes; SHA-256 `1a15e66a07892f544c4b9bee75201ff9acaf3edd2c37963a780f8473466d50cb`.

## docs-workflow 42: Per-page contents gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/42.log`; 196 bytes; SHA-256 `93344619a65ef755568802b04dd611d97b36f99e351716ae913a1306d640ac2d`.

## docs-workflow 43: AEM store generator self-test

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 avdecc/gen_aem_store.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/43.log`; 3,596 bytes; SHA-256 `9f126bf9dfc7cb552a2414b98d2792449dc4ae126395997750d5039cb896f022`.

## docs-workflow 44: Sweep/build shape gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_sweep_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/44.log`; 19,682 bytes; SHA-256 `4ad86678c9873950f7e461c77357a91f24eed77099297b3c40d4944b1ff5746e`.

## docs-workflow 45: Deploy shape gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_deploy_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/45.log`; 9,270 bytes; SHA-256 `6e4bb815d4a015fc437da1e1584f8755b4feba5ab5272421126ca193b0a58610`.

## docs-workflow 46: Entity shape gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 scripts/check_entity_shape.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/46.log`; 25,694 bytes; SHA-256 `7c1cc4d5ce778537bd27790e075eb0d8159cf6c1281870eb96142e9465eff19c`.

## docs-workflow 47: Fetch the engine authority the builder derives from

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
git submodule update --init gptp-processor
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/47.log`; 0 bytes; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## docs-workflow 48: Advertised-vs-emitted gate (green since 2026-07-28, item 00)

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$LANES/682-pp-pin3`.

```sh
python3 -m pip install --quiet pyyaml
python3 scripts/check_wire_accountability.py --self-test
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/48.log`; 4,965 bytes; SHA-256 `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4`.

## docs-workflow 49: Strip git metadata, then run the docs gate

Head: `1e99ad217f0747c33e03238f7d1c633c07ce572c`. GNU Make 4.3. Exit: 0.

Working directory: `$VALIDATION_STORAGE/682-a554/docs-no-git`.

```sh
rm -rf .git
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py
```

Log: `$VALIDATION_STORAGE/682-a554/docs-workflow/49.log`; 225 bytes; SHA-256 `9321a0cced93c97fa319ffd0f72492c1302169e38c79ab2e9b6b772494bb97ec`.

