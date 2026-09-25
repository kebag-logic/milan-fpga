#!/usr/bin/env bash
# Apply the runner's two pure shipping-workflow validators (the inputs of its
# selftest_shipping_workflows arms) to exported source and candidate trees,
# plus a planted untrusted-action control. No Docker, act, network or selftest.
set -euo pipefail
repo=$1; scratch=$2; py=${3:-python3}
rm -rf "$scratch"; mkdir -p "$scratch"
for sha in 022290e4c94a23b9ee97852b6c1c2ee2c1f25352 b74fb11162fba8f019110d9f2c21492300857da2; do
  mkdir -p "$scratch/$sha"
  git -C "$repo" archive "$sha" .github scripts/act_ci.py | tar -x -C "$scratch/$sha"
done
cp -r "$scratch/b74fb11162fba8f019110d9f2c21492300857da2" "$scratch/control"
printf '      - uses: someone/untrusted@v1\n' >> "$scratch/control/.github/workflows/docs.yml"
env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_CONFIG PYTHONDONTWRITEBYTECODE=1 \
  "$py" - "$scratch" <<'PY'
import importlib.util, pathlib, sys
scratch = pathlib.Path(sys.argv[1])
cand = scratch / "b74fb11162fba8f019110d9f2c21492300857da2"
spec = importlib.util.spec_from_file_location("act_ci_probe", cand / "scripts/act_ci.py")
m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m; spec.loader.exec_module(m)
expected = {"docs": "act-docs-", "elaborate": "act-elaborate-",
            "rtl-fast": "act-rtl-fast-", "rtl-full": "act-rtl-full-"}
for label in ("022290e4c94a23b9ee97852b6c1c2ee2c1f25352",
              "b74fb11162fba8f019110d9f2c21492300857da2", "control"):
    root = scratch / label
    try:
        m.validate_workflow_sandbox(root, tuple(m.WORKFLOWS)); sandbox = "PASS"
    except m.Refusal as exc:
        sandbox = f"REFUSED ({exc})"
    try:
        scope = m.workflow_job_volume_scope(root, tuple(m.WORKFLOWS))
        vol = "PASS" if scope == expected else f"MISMATCH {scope}"
    except m.Refusal as exc:
        vol = f"REFUSED ({exc})"
    print(f"{label}: sandbox-policy {sandbox}; job-volume-scope {vol}")
PY
