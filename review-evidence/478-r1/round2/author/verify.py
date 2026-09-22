"""A169 bounded correction reproduction; never modifies the source lane."""
import base64
import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tarfile

PACKET = Path(__file__).resolve().parent
META = json.loads((PACKET / "head.json").read_text())
LANE = Path(META["source_lane"])
RECEIPTS = PACKET / "receipts"
SCRATCH = PACKET / "scratch"
OLD = b"../protocol-processor/docs/architecture/07_memory_maps.md"
NEW = b"https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/424c688fa2205b934a7689a58f2aa766420f2326/docs/architecture/07_memory_maps.md"
DOC = "docs/ENDSTATION_BUILDER.md"


def run(label, args, cwd=LANE, expected=0, state="corrected committed tree"):
    command = ["rtk", "proxy", *args]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    record = dict(META, label=label, command=command,
                  command_shell=shlex.join(command), cwd=str(cwd),
                  state=state, expected_exit=expected, exit_code=result.returncode,
                  started_utc=started,
                  finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  stdout=result.stdout, stderr=result.stderr)
    (RECEIPTS / f"{label}.json").write_text(json.dumps(record, indent=2) + "\n")
    (RECEIPTS / f"{label}.log").write_text(result.stdout + result.stderr)
    print(f"{label}: exit {result.returncode} (expected {expected})", flush=True)
    assert result.returncode == expected, result.stdout + result.stderr
    return result.stdout


def verify_population(root, label):
    entries = []
    pins = {}
    for row in run(label + "-tree", ["git", "ls-tree", "-r", META["head"]]).splitlines():
        metadata, name = row.split("\t", 1)
        mode, kind, oid = metadata.split()
        path = root / name
        if mode == "160000":
            assert not path.exists() or (path.is_dir() and not any(path.iterdir())), name
            pins[name] = oid
            continue
        assert not path.is_symlink(), name
        data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == oid, name
        assert bool(path.stat().st_mode & 0o111) == (mode == "100755"), name
        entries.append({"path": name, "mode": mode, "blob": oid})
    assert not (root / "protocol-processor/docs/architecture/07_memory_maps.md").exists()
    (RECEIPTS / f"{label}-population.json").write_text(json.dumps(
        dict(META, root=str(root), checked_files=len(entries), entries=entries,
             uninitialized_gitlinks=pins, all_blobs_and_modes_match=True), indent=2) + "\n")
    print(f"{label}: {len(entries)} committed blobs/modes match; {len(pins)} submodules empty/absent", flush=True)


def prepare():
    SCRATCH.mkdir(exist_ok=False)
    gitcopy = SCRATCH / "git"
    archivecopy = SCRATCH / "no-git"
    run("02-clone", ["git", "clone", "--no-local", "--no-checkout", "--depth", "2",
                      "--single-branch", "--branch", META["branch"], str(LANE), str(gitcopy)])
    run("03-checkout", ["git", "checkout", "--detach", META["head"]], gitcopy)
    assert run("04-git-head-tree", ["git", "rev-parse", "HEAD", "HEAD^{tree}"], gitcopy).splitlines() == [META["head"], META["tree"]]
    assert run("05-git-clean", ["git", "status", "--porcelain=v1", "--untracked-files=all"], gitcopy) == ""
    submodules = run("06-git-submodules", ["git", "submodule", "status"], gitcopy)
    assert len(submodules.splitlines()) == 4 and all(line.startswith("-") for line in submodules.splitlines())
    archive = SCRATCH / "corrected.tar"
    run("07-archive", ["git", "archive", "--format=tar", "--output=" + str(archive), META["head"]])
    archivecopy.mkdir()
    with tarfile.open(archive) as bundle:
        bundle.extractall(archivecopy, filter="data")
    (RECEIPTS / "07-archive-sha256.txt").write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + "  corrected.tar\n")
    run("08-no-git-proof", ["git", "rev-parse", "--is-inside-work-tree"], archivecopy, expected=128)
    assert not any(path.name == ".git" for path in archivecopy.rglob(".git"))
    verify_population(gitcopy, "09-git-before")
    verify_population(archivecopy, "10-no-git-before")


def docs():
    for mode in ("git", "no-git"):
        root = SCRATCH / mode
        output = run(f"11-{mode}-docs-corrected", ["python3", "scripts/docs_check.py"], root)
        inventory = "[git ls-files]" if mode == "git" else "[filesystem walk (no git)]"
        assert inventory in output and "0 finding(s)" in output
        path = root / DOC
        corrected = path.read_bytes()
        assert corrected.count(NEW) == 1 and OLD not in corrected
        restored = corrected.replace(NEW, OLD)
        assert hashlib.sha256(restored).hexdigest() == "9352133e96e0002f2ec5896273eba9a4b285e8435e18d78c2ec98ca1b0fb3ef8"
        try:
            path.write_bytes(restored)
            output = run(f"12-{mode}-docs-old-link", ["python3", "scripts/docs_check.py"], root,
                         expected=1, state="negative control: corrected committed tree with only original link restored; not corrected-head evidence")
            assert output.splitlines() == [
                "docs/ENDSTATION_BUILDER.md:963: broken link -> ../protocol-processor/docs/architecture/07_memory_maps.md",
                next(line for line in output.splitlines() if line.startswith("docs_check: 1 finding(s)"))]
            assert inventory in output
        finally:
            path.write_bytes(corrected)
        verify_population(root, f"13-{mode}-after-restore")


def focused():
    root = SCRATCH / "git"
    for label, args in [
        ("14-doc-paths", ["python3", "scripts/check_doc_paths.py"]),
        ("15-doc-style", ["python3", "scripts/check_doc_style.py"]),
        ("16-toc-check", ["python3", "scripts/gen_toc.py", "--check"]),
        ("17-toc-anchors", ["python3", "scripts/gen_toc.py", "--verify-anchors"]),
        ("18-em-dash", ["python3", "scripts/check_em_dash.py", "--base", META["parent"]]),
        ("19-issue478-validator-selftest", ["python3", "-B", "-c", "import sys; sys.path.insert(0, 'sw/builder'); import test_builder; test_builder.test_pp_shadow_audio_unit_rates_match_config()"]),
        ("20-diff-check", ["git", "diff", "--check", META["parent"], META["head"]]),
    ]:
        run(label, args, root)
    assert run("21-final-copy-clean", ["git", "status", "--porcelain=v1", "--untracked-files=all"], root) == ""
    assert run("22-final-lane-clean", ["git", "status", "--porcelain=v1", "--untracked-files=all"]) == ""
    assert run("23-final-lane-head-tree", ["git", "rev-parse", "HEAD", "HEAD^{tree}"]).splitlines() == [META["head"], META["tree"]]
    assert run("24-changed-paths", ["git", "diff", "--name-only", META["parent"], META["head"]]).splitlines() == [DOC]
    run("25-final-commit", ["git", "show", "-s", "--format=fuller", META["head"]])


def target():
    response = run("26-pinned-target", ["gh", "api", "repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/contents/docs/architecture/07_memory_maps.md?ref=424c688fa2205b934a7689a58f2aa766420f2326"])
    resource = json.loads(response)
    data = base64.b64decode(resource["content"])
    oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert oid == resource["sha"] == "5be7a4c49c34c6f5638d2a461eedc65dc4dc28a6"
    assert resource["html_url"] == NEW.decode()
    assert b"### 3.1 Descriptor tree" in data and b"| L10 |" in data
    (RECEIPTS / "26-pinned-target-verification.json").write_text(json.dumps(
        dict(META, pp_pin="424c688fa2205b934a7689a58f2aa766420f2326", blob=oid,
             bytes=len(data), html_url=resource["html_url"], section_3_1_and_L10_present=True), indent=2) + "\n")


if __name__ == "__main__":
    import sys
    {"prepare": prepare, "docs": docs, "focused": focused, "target": target}[sys.argv[1]]()
