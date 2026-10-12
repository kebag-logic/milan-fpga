"""Build ctrl_nvm_seal.c against the unchanged Mark II store for each shape
and run it: two distinct sealed refusals of slot A (an entity byte, then a
record-area byte), then a clean read, and a clean control.
python3 -I ctrl_nvm_seal.py REPO WORK SHAPE..."""
import subprocess
import sys
from pathlib import Path

repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
here = Path(__file__).resolve().parent
tree = repo / "sw/firmware/ctrl_nvm"
sys.dont_write_bytecode = True
sys.path.insert(0, str(tree / "test"))
import nvm_bench as nb  # noqa: E402

for stem in sys.argv[3:]:
    w = work / stem
    w.mkdir(parents=True, exist_ok=True)
    inputs = nb.shape_inputs(repo / "configs" / f"{stem}.yaml", w)
    bench = nb.make_bench(inputs)
    gen = w / "gen"
    nb.write_headers(gen, nb.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)
    exe = w / "ctrl_nvm_seal"
    sources = [here / "ctrl_nvm_seal.c", tree / "nvm_store.c", tree / "nvm_klj2.c",
               tree / "host/nvm_fmodel.c", tree / "host/nvm_smodel.c"]
    subprocess.run(["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", *nb.includes(tree, gen),
                    *map(str, sources), "-o", str(exe)], check=True)
    image = bench.assemble(bench.frames, 0x5A5A5)
    (w / "a.bin").write_bytes(image)
    body = 40 + (len(image) - 44) // 2
    print(f"== {stem}: container {len(image)} B at seq 0x5a5a5; record-area byte {body}")
    for label, at, count in (("clean control", body, 0), ("entity byte, two sealed reads", 20, 2),
                             ("record-area byte, two sealed reads", body, 2)):
        r = subprocess.run([str(exe), str(w / "a.bin"), str(at), str(count)], capture_output=True,
                           text=True, check=True)
        print(f"-- {label}\n{r.stdout}", end="")
