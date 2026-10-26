# Census at head 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0

## runs-on writers (every place that emits or declares a job label)
```
.github/ci-templates/docs.yml:10:    runs-on: ubuntu-24.04
.github/ci-templates/docs.yml:496:    runs-on: ubuntu-24.04
.github/ci-templates/docs.yml:510:    runs-on: ubuntu-24.04
.github/ci-templates/elaborate.yml:71:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:26:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:80:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:122:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:137:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:259:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:334:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:383:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:417:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:451:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:500:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:539:    runs-on: ubuntu-24.04
.github/ci-templates/rtl-fast.yml:605:    runs-on: ubuntu-24.04
.github/ci-templates/rtl.yml:37:    runs-on: ubuntu-24.04
.github/ci-templates/rtl.yml:156:    runs-on: ubuntu-24.04
.github/ci-templates/rtl.yml:320:    runs-on: ubuntu-24.04
.github/ci-templates/rtl.yml:403:    runs-on: ubuntu-24.04
.github/ci-templates/rtl.yml:461:    runs-on: ubuntu-24.04
.github/ci-templates/rtl.yml:586:    runs-on: ubuntu-24.04
scripts/ci_gate_workflows.py:165:    return {"runs-on": "ubuntu-24.04", "timeout-minutes": 3,
scripts/ci_runtime_workflows.py:127:    return {"name": "Fail fast across this head", "runs-on": "ubuntu-24.04", "timeout-minutes": 120,
scripts/ci_runtime_workflows.py:145:    return {"name": "Cancel late CI failures", "runs-on": "ubuntu-24.04", "timeout-minutes": 3,
scripts/ci_runtime_workflows.py:159:    return {"name": "Collect CI manifest", "runs-on": "ubuntu-24.04", "timeout-minutes": 15,
scripts/ci_suite_workflows.py:44:        "runs-on": "ubuntu-24.04", "timeout-minutes": 2,
scripts/ci_suite_workflows.py:76:        "name": "Prepare pinned Yosys", "runs-on": "ubuntu-24.04", "timeout-minutes": 29,
```

## runs-on values in the generated workflows
```
.github/workflows/docs.yml: 9 ubuntu-24.04, 9 runs-on lines
.github/workflows/elaborate.yml: 6 ubuntu-24.04, 6 runs-on lines
.github/workflows/rtl-fast.yml: 15 ubuntu-24.04, 15 runs-on lines
.github/workflows/rtl.yml: 16 ubuntu-24.04, 16 runs-on lines
```

## every ubuntu-latest left in the tree (first-party; submodules excluded)
```
docs/testing/CI_WORKFLOWS.md:8:`ubuntu-24.04`, never on the floating `ubuntu-latest` (#784). The workflow
docs/testing/CI_WORKFLOWS.md:11:`ubuntu-latest` moved to the `ubuntu-26.04` image, where the pinned CPython
docs/testing/CI_WORKFLOWS.md:2038:`--platform` entry, and every other label, such as `ubuntu-latest`,
docs/testing/CI_WORKFLOWS.md:2040:`ubuntu-latest` is refused because hosted `ubuntu-latest` moved to the
docs/testing/CI_WORKFLOWS.md:2046:such as `ubuntu-latest` would run on act's default `node:16` image instead, so
docs/testing/TESTING.md:331:used a hosted `ubuntu-latest` runner, then the `ubuntu-24.04` image, and sequential `make -C` invocations.
scripts/act_ci.py:88:#: ``ubuntu-latest`` moved to the 26.04 image, where the pinned CPython 3.12
scripts/act_ci.py:89:#: wheels do not install, so ``ubuntu-latest`` is refused like any other label.
scripts/act_ci.py:90:#: act would run a built-in label such as ``ubuntu-latest`` on its own default
scripts/act_ci.py:6725:        for label in ("ubuntu-latest", "ubuntu-26.04", "ubuntu-22.04"):
scripts/act_ci.py:6752:    probes = ("ubuntu-latest", "ubuntu-24.04", "ubuntu-26.04", "ubuntu-22.04", "ubuntu-20.04", "self-hosted")
scripts/act_ci.py:6825:    for label in ("ubuntu-latest", "ubuntu-26.04"):
scripts/act_ci.py:13279:    #: fixture on a label the sandbox does not accept, such as ubuntu-latest
tb/verilator/follow_ring/Makefile:26:# hosted ubuntu-latest runner, run 37892515345, shard 0/5 job 113696564335.
tb/verilator/milan_dp_render/Makefile:42:# hosted ubuntu-latest runner, run 37892515345, shard 0/5 job 113696564335.
```

## ubuntu-latest under .github/, the templates and the generators
```
git grep exit status 1 (1 = no match)
```
