"""Print each run step of one workflow job as a numbered shell fragment file."""
import sys, yaml, pathlib
wf, job, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
steps = yaml.safe_load(open(wf))["jobs"][job]["steps"]
for i, s in enumerate(steps):
    if "run" in s:
        (out / f"{i:02d}.sh").write_text(f"# {s.get('name','')}\n" + s["run"])
        print(f"{i:02d} {s.get('name','')}")
