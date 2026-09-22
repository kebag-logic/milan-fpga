"""Portable, bounded I440 sensitivity on disposable copies, never tracked edits."""
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
files = ["gen_toc.py", "gen_toc_cases.py", "gen_toc_guards.py", "gen_toc_closer_cases.py", "check_em_dash.py"]
originals = {name: (repo / "scripts" / name).read_bytes() for name in files}
closing = 'return bool(re.search(r"</(?:%s)>" % "|".join(RAW_HTML_TAGS), line, ASCII_FOLD))'
mutations = [
    ("I440-M01-fence-python-strip", [("gen_toc.py", 'not m.group(2).strip(CLASSES["blank"])', 'not m.group(2).strip()')]),
    ("I440-M02-fence-wide-named-class", [("gen_toc.py", 'not m.group(2).strip(CLASSES["blank"])',
                                        'not m.group(2).strip(CLASSES["tag blank"])')]),
    ("I440-M03-fence-no-tab", [("gen_toc.py", 'not m.group(2).strip(CLASSES["blank"])',
                               'not m.group(2).strip(CLASSES["indent"])')]),
    ("I440-M04-inner-blanks", [("gen_toc.py", closing,
        'return bool(re.search(r"</(?:%s)%s*>" % ("|".join(RAW_HTML_TAGS), _cc("blank")), line, ASCII_FOLD))')]),
    ("I440-M05-matching-name-only", [
        ("gen_toc.py", 'def _type_1_end(line: str) -> bool:', 'def _type_1_end(line: str, tag: str) -> bool:'),
        ("gen_toc.py", closing, 'return bool(re.search(r"</%s>" % tag, line, ASCII_FOLD))'),
        ("gen_toc.py", '_type_1_end(line) else HTML', '_type_1_end(line, tag) else HTML'),
        ("gen_toc.py", 'closed = _type_1_end(line)', 'closed = _type_1_end(line, tag)')]),
    ("I440-M06-unicode-fold", [("gen_toc.py", closing, closing.replace("ASCII_FOLD", "re.IGNORECASE"))]),
    ("I440-M07-case-sensitive", [("gen_toc.py", closing, closing.replace("ASCII_FOLD", "0"))]),
    ("I440-M08-drop-opening-line-close", [("gen_toc.py", 'closed = _type_1_end(line)', 'closed = False')]),
    ("I440-M09-drop-later-close", [("gen_toc.py", '(TEXT if _type_1_end(line) else HTML)', '(TEXT if False else HTML)')]),
    ("I440-M10-anchor-closer", [("gen_toc.py", closing, closing.replace('r"</', 'r"^</'))]),
    ("I440-M11-restore-old-type1", [
        ("gen_toc.py", 'def _type_1_end(line: str) -> bool:', 'def _type_1_end(line: str, tag: str) -> bool:'),
        ("gen_toc.py", closing, 'return bool(re.search(r"</%s\\s*>" % tag, line, ASCII_FOLD))'),
        ("gen_toc.py", '_type_1_end(line) else HTML', '_type_1_end(line, tag) else HTML'),
        ("gen_toc.py", 'closed = _type_1_end(line)', 'closed = _type_1_end(line, tag)')]),
]
records = []
dest = root / "sensitivity"
dest.mkdir(exist_ok=True)
for name, replacements in mutations:
    with tempfile.TemporaryDirectory(prefix="i440.mutation.") as tmp:
        scripts = Path(tmp) / "scripts"
        scripts.mkdir()
        changed = {file: data.decode() for file, data in originals.items()}
        for file, old, new in replacements:
            assert changed[file].count(old) == 1, (name, file, old)
            changed[file] = changed[file].replace(old, new)
        patch = []
        for file, text in changed.items():
            (scripts / file).write_text(text)
            patch += list(difflib.unified_diff(originals[file].decode().splitlines(True), text.splitlines(True),
                                             fromfile="a/scripts/"+file, tofile="b/scripts/"+file))
        (dest / (name + ".patch")).write_text("".join(patch))
        record = dict(id=name, commands=[])
        for file in ("gen_toc.py", "check_em_dash.py"):
            command = [sys.executable, "-B", str(scripts / file), "--selftest"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = result.stdout.decode()
            (dest / (name + "-" + file + ".log")).write_text(output)
            failed = [line for line in output.splitlines() if "I440" in line and ("FAIL" in line or line.lstrip().startswith("-"))]
            record["commands"].append(dict(script=file, arguments=["--selftest"], exit=result.returncode,
                                           I440_failures=len(failed), example=failed[:2]))
        # Every property must fail behavioral controls, not only a guard/tally.
        assert record["commands"][0]["exit"] == 1 and record["commands"][0]["I440_failures"] > 0, record
        records.append(record)
for file, data in originals.items():
    assert (repo / "scripts" / file).read_bytes() == data, file
(dest / "source-sha256.json").write_text(json.dumps({f: hashlib.sha256(b).hexdigest() for f,b in originals.items()}, indent=2)+"\n")
(dest / "results.json").write_text(json.dumps(records, indent=2)+"\n")
for r in records:
    print(r["id"], [(c["script"], c["exit"], c["I440_failures"]) for c in r["commands"]])
print("Tracked sources preserved byte-for-byte; all 11 mutants failed behavioral I440 controls")
