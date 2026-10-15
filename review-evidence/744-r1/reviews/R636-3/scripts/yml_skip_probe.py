"""Plant each unindented declared line (skipped by the cross-file arms) into .github/workflows/rtl-fast.yml,
alone and under 'run: |', and report the gate's findings. Usage: python3 -I yml_skip_probe.py <tree with scripts/>"""
import importlib.util, pathlib, subprocess, sys, tempfile
spec = importlib.util.spec_from_file_location("bm", pathlib.Path(sys.argv[1]) / "scripts/check_baremetal_only.py")
bm = importlib.util.module_from_spec(spec); spec.loader.exec_module(bm)
for path, lines in bm.HOST_MEMORY_READS.items():
    for i, line in enumerate(lines):
        if line[:1] == " " or path.endswith(".yml"):
            continue
        for shape, text in (("alone", line + "\n"), ("after-run", "run: |\n" + line + "\n")):
            with tempfile.TemporaryDirectory() as d:
                root = pathlib.Path(d)
                subprocess.run(["git", "-C", d, "init", "-q"], check=True)
                doc = root / bm.PRODUCT_DOCS[0]; doc.parent.mkdir(parents=True)
                doc.write_text("The full FPGA solution uses bare-metal firmware.\n")
                t = root / ".github/workflows/rtl-fast.yml"; t.parent.mkdir(parents=True); t.write_text(text)
                subprocess.run(["git", "-C", d, "add", "-A"], check=True)
                try:
                    findings, _ = bm.check(root)
                except bm.InventoryError as exc:
                    findings = ["[inventory] " + str(exc)]
                print(f"{path}[{i}] {shape}: {'REFUSED' if findings else 'ACCEPTED'}: {findings}")
