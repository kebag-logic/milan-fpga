#!/usr/bin/env python3
"""Run focused read-only gates concurrently; all child commands are awaited."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
out=pathlib.Path(sys.argv[1]).resolve(); py=sys.argv[2]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",TMPDIR=str(out/"scratch"),MAKEFLAGS="-j16")
base="c6bd08c6f52632c6d33d834ce842ac3cf63f29cc"
checks={
 "docs-check":[py,"scripts/docs_check.py"],
 "docs-selftest":[py,"scripts/docs_check.py","--selftest"],
 "em-dash":[py,"scripts/check_em_dash.py","--base",base],
 "doc-style":[py,"scripts/check_doc_style.py"],
 "toc":[py,"scripts/gen_toc.py","--check"],
 "anchors":[py,"scripts/gen_toc.py","--verify-anchors"],
 "doc-paths":[py,"scripts/check_doc_paths.py"],
 "ci-scope":[py,"-I","scripts/ci_scope.py","--selftest"],
 "ci-scope-memory":[py,"scripts/ci_scope.py","docs/design/SPLIT_CONTROL_MEMORY.md"],
 "ci-events":[py,"scripts/ci_events.py","--check"],
 "ci-events-selftest":[py,"scripts/ci_events.py","--selftest"],
 "py-idiom":[py,"scripts/check_py_idiom.py"],
 "test-evidence":[py,"scripts/measure_test_evidence.py","--check"],
 "test-evidence-selftest":[py,"scripts/measure_test_evidence.py","--selftest"],
 "module-matrix":[py,"docs/traceability/gen_module_matrix.py","--check"],
 "memory-baseline":[py,"syn/ooc/pp_resource_gate.py","check-baseline"],
 "diff-check":["git","diff","--check",base,"HEAD"],
 "litex-runner-selftest":["bash","scripts/run_litex_sims.sh","--selftest"],
}
def run(item):
 name,argv=item; start=time.monotonic()
 with (out/(name+".log")).open("w") as log:
  log.write("argv: "+json.dumps(argv)+"\n"); log.flush()
  rc=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,env=env).returncode
 (out/(name+".rc")).write_text(str(rc)+"\n")
 return dict(name=name,argv=argv,rc=rc,seconds=round(time.monotonic()-start,2))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 rows=list(pool.map(run,checks.items()))
(out/"checks.json").write_text(json.dumps(rows,indent=2)+"\n")
for row in rows: print(row["name"],row["rc"],row["seconds"],flush=True)
sys.exit(int(any(row["rc"] for row in rows)))
