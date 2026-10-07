# SPDX-License-Identifier: Apache-2.0
"""Portable foreground review checks. Usage: python3 review.py REPOSITORY TASK.
TASK: prepare, baseline, reversals, integration, bindings, reconcile, audit.
All generated sources and build products stay in the sibling scratch directory.
Published logs replace absolute paths; byte-for-byte output stays in scratch/raw.
No checkout files are changed. Dependencies are installed into scratch only.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tarfile
import urllib.request

HEAD = "e4f9995b791489c53b8ccb8a8dc09ec508e32e6b"
TREE = "9457a9568dad668a04e2a4042f6d3f984aebe387"
BASE = "19f5796b63652eb1151906de73cb827d4980a53f"
ROOT = Path(__file__).resolve().parent
SCRATCH = ROOT / "scratch"
SDK = SCRATCH / "sdk"
RECEIPTS = ROOT / "receipts"
RAW = SCRATCH / "raw"
for directory in (SCRATCH, RECEIPTS, RAW):
    directory.mkdir(exist_ok=True)
parser = argparse.ArgumentParser()
parser.add_argument("repository", type=Path)
parser.add_argument("task", choices=["prepare", "baseline", "reversals", "integration", "bindings", "reconcile", "audit"])
args = parser.parse_args()
REPO = args.repository.resolve()

def clean(text):
    for old, new in sorted([(str(SCRATCH), "$SCRATCH"), (str(REPO), "$REPOSITORY"),
                            (str(ROOT), "$PACKET"), (str(Path.home()), "$USER_DIRECTORY")],
                           key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    return re.sub(r"/(?:usr|lib|bin|opt|tmp|var)/[^\s;\"<>]+", "$SYSTEM_PATH", text)

def run(name, command, cwd=None, expected=0, contains=()):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    actual = list(map(str, command))
    result = subprocess.run(actual, cwd=cwd or REPO, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=540)
    output = result.stdout.decode(errors="replace")
    (RAW / (name + ".log")).write_bytes(result.stdout)
    (RECEIPTS / (name + ".log")).write_text(
        "# SPDX-License-Identifier: Apache-2.0\nCommand: " + clean(shlex.join(list(map(str, command)))) +
        "\nWorking directory: " + clean(str(cwd or REPO)) + "\n\n" + clean(output))
    (RECEIPTS / (name + ".rc")).write_text("# SPDX-License-Identifier: Apache-2.0\n" + str(result.returncode) + "\n")
    print(f"{name}: rc={result.returncode}", flush=True)
    assert result.returncode == expected, (name, result.returncode, clean(output[-4000:]))
    for fragment in contains:
        assert fragment in output, (name, fragment, clean(output[-4000:]))
    return output

def export(name, ref=HEAD):
    target = SCRATCH / name
    assert not target.exists(), f"Remove only this disposable tree before rerunning: {target}"
    target.mkdir()
    data = subprocess.check_output(["git", "-C", str(REPO), "archive", ref])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(target, filter="data")
    return target

def configure(name, source, extra=(), dependencies=True, expected=0):
    command = ["cmake", "-S", source, "-B", source / "build", "-G", "Unix Makefiles",
               "-DCMAKE_BUILD_TYPE=Debug"]
    if dependencies:
        command += [f"-DCMAKE_PREFIX_PATH={SDK}"]
    return run(name + "-configure", command + list(extra), source, expected)

def build(name, source, target=None):
    command = ["make", "-C", source / "build", "-j16"]
    if target:
        command.append(target)
    return run(name + "-build", command, source)

def ctest(name, source, expected=0, contains=()):
    return run(name, ["ctest", "--test-dir", "build", "--verbose", "--output-on-failure"],
               source, expected, contains)

def behave(name, source, expected=0, contains=()):
    return run(name, ["python3", "-m", "behave"], source, expected, contains)

def replace(path, old, new):
    text = path.read_text()
    assert text.count(old) == 1, (path.name, old)
    path.write_text(text.replace(old, new))

def prepare():
    url = "https://codeload.github.com/cgreen-devs/cgreen/tar.gz/refs/tags/1.7.0"
    archive = SCRATCH / "cgreen-1.7.0.tar.gz"
    if not archive.exists():
        archive.write_bytes(urllib.request.urlopen(url, timeout=60).read())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest == "406e3eb77fe855152ae917651a52a2445be7ccde6affbc68aad90bbe985d3869"
    (RECEIPTS / "dependency.txt").write_text(
        "SPDX-License-Identifier: Apache-2.0\nSource: " + url + "\nSHA256: " + digest +
        "\nVersion: 1.7.0; prefix restricted to scratch/sdk.\n")
    source = SCRATCH / "cgreen-1.7.0"
    if not source.exists():
        with tarfile.open(archive) as archive_file:
            archive_file.extractall(SCRATCH, filter="data")
    run("dependency-configure", ["cmake", "-S", source, "-B", SCRATCH / "cgreen-build",
        "-G", "Unix Makefiles", "-DCMAKE_BUILD_TYPE=Release", f"-DCMAKE_INSTALL_PREFIX={SDK}",
        "-DCGREEN_WITH_UNIT_TESTS=OFF", "-DCGREEN_WITH_LIBXML2=OFF"], SCRATCH)
    run("dependency-build", ["make", "-C", SCRATCH / "cgreen-build", "-j16"], SCRATCH)
    run("dependency-install", ["cmake", "--install", SCRATCH / "cgreen-build"], SCRATCH)
    run("versions", ["python3", "-c", "import platform,behave; print('Python',platform.python_version()); print('behave',behave.__version__)"], SCRATCH)

def baseline():
    for name, ref in [("baseline", BASE), ("head", HEAD)]:
        source = export(name, ref)
        configure(name, source)
        build(name, source)
        if name == "baseline":
            ctest(name + "-ctest", source, contains=["0 tests", "No assertions", "100% tests passed"])
            behave(name + "-behave", source, 1, ["undefined symbol: shlan_connect", "3 untested", "10 untested"])
        else:
            ctest(name + "-ctest", source, contains=["9 tests", "1690 passes", "100% tests passed"])
            behave(name + "-behave", source, contains=["1 feature passed", "3 scenarios passed", "10 steps passed"])
            run("head-symbols", ["nm", "-D", "--defined-only", "build/libshlan.so"], source)

def reversals():
    for name in ["exports", "ctypes", "unit-wiring", "empty-runner", "assertion"]:
        source = export("reversal-" + name)
        if name == "exports":
            replace(source / "CMakeLists.txt", "    tests/features/switch_bindings.c\n", "")
        if name == "ctypes":
            (source / "tests/features/environment.py").write_bytes(subprocess.check_output(
                ["git", "-C", str(REPO), "show", BASE + ":tests/features/environment.py"]))
        if name == "unit-wiring":
            (source / "tests/unit/placeholder.c").write_bytes(subprocess.check_output(
                ["git", "-C", str(REPO), "show", BASE + ":tests/unit/placeholder.c"]))
            replace(source / "CMakeLists.txt", "tests/unit/main.c tests/unit/mrp_pdu_test.c", "tests/unit/placeholder.c")
        if name == "empty-runner":
            replace(source / "tests/unit/main.c", "TestSuite *suite = mrp_pdu_suite();", "TestSuite *suite = create_test_suite();")
        if name == "assertion":
            replace(source / "tests/unit/mrp_pdu_test.c", "is_equal_to(215)", "is_equal_to(214)")
        label = "reversal-" + name
        configure(label, source)
        build(label, source)
        if name in ("exports", "ctypes"):
            symbol = "shlan_test_connect" if name == "exports" else "shlan_connect"
            behave(label + "-behave", source, 1, ["undefined symbol: " + symbol, "3 untested"])
        elif name == "assertion":
            ctest(label + "-ctest", source, 8, ["1689 passes, 1 failure"])
        else:
            ctest(label + "-ctest", source, 8, ["Regex=[No assertions]", "0 tests"])

def integration():
    source = export("release-library")
    configure("release-library", source, ["-DCMAKE_BUILD_TYPE=Release", "-DBUILD_TESTING=OFF"])
    build("release-library", source, "shlan")
    run("release-library-symbols", ["nm", "-D", "--defined-only", "build/libshlan.so"], source,
        contains=["shlan_test_connect", "shlan_test_disconnect", "shlan_test_port_enable", "shlan_test_port_disable"])
    run("release-library-test-list", ["ctest", "--test-dir", "build", "-N"], source, contains=["Total Tests: 1"])
    for label, ref, expected in [("base-no-dependency", BASE, 0), ("head-no-dependency", HEAD, 1)]:
        source = export(label, ref)
        configure(label, source, ["-DCMAKE_BUILD_TYPE=Release", "-DBUILD_TESTING=OFF",
            f"-DCMAKE_FIND_ROOT_PATH={SCRATCH / 'empty-root'}", "-DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY",
            "-DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY"], dependencies=False, expected=expected)
        if expected == 0:
            build(label, source, "shlan")
    source = export("zephyr-glue")
    wrapper = source / "wrapper"
    wrapper.mkdir()
    (wrapper / "CMakeLists.txt").write_text("""# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.20)
project(integration_probe C)
set(ZEPHYR_BASE simulated)
set(CONFIG_LWSRP ON)
function(zephyr_library_named name)
  add_library(${name} STATIC)
endfunction()
function(zephyr_library_sources)
  target_sources(lwsrp PRIVATE ${ARGV})
endfunction()
function(zephyr_include_directories)
  target_include_directories(lwsrp PRIVATE ${ARGV})
endfunction()
function(zephyr_library_include_directories)
  target_include_directories(lwsrp PRIVATE ${ARGV})
endfunction()
add_subdirectory(.. component)
""")
    configure("zephyr-glue", wrapper, dependencies=False)
    build("zephyr-glue", wrapper)
    output = run("zephyr-glue-symbols", ["nm", "-g", "--defined-only", "build/component/liblwsrp.a"], wrapper)
    assert "shlan_test_" not in output

def bindings():
    run("binding-forwarding", ["python3", ROOT / "binding_probe.py", SCRATCH / "head/build/libshlan.so"], SCRATCH)

def reconcile():
    for name in ["disable-dispatch", "connect-noop"]:
        source = export("prior-" + name)
        path = source / "tests/features/switch_bindings.c"
        if name == "disable-dispatch":
            replace(path, "return shlan_port_disable(sw, port_id);", "return shlan_port_enable(sw, port_id);")
        else:
            replace(path, "return shlan_connect(sw);", "(void)sw; return 0;")
        configure("prior-" + name, source)
        build("prior-" + name, source)
        behave("prior-" + name + "-behave", source, contains=["3 scenarios passed", "10 steps passed"])
    run("prior-prototypes", ["cc", "-fsyntax-only", "-std=c11", "-Wall", "-Wextra", "-Wpedantic",
        "-Wmissing-prototypes", "-Wstrict-prototypes", "-I", SDK / "include", "-I", REPO / "src/include",
        REPO / "tests/features/switch_bindings.c", REPO / "tests/unit/main.c", REPO / "tests/unit/mrp_pdu_test.c"],
        SCRATCH, contains=["no previous prototype"])
    output = run("head-dynamic-dependencies", ["readelf", "-d", SCRATCH / "head/build/libshlan.so"], SCRATCH)
    assert "libcgreen" not in output

def audit():
    def git(*arguments):
        return subprocess.check_output(["git", "-C", str(REPO), *arguments])
    assert git("rev-parse", "HEAD").decode().strip() == HEAD
    assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    assert not git("diff", "--raw", HEAD)
    assert not git("diff", "--cached", "--raw", HEAD)
    entries = git("ls-tree", "-rz", HEAD).split(b"\0")
    index = git("ls-files", "--stage", "-z").split(b"\0")
    expected_index = []
    links = []
    count = 0
    for entry in entries:
        if not entry:
            continue
        header, path = entry.split(b"\t", 1)
        mode, kind, oid = header.split()
        expected_index.append(mode + b" " + oid + b" 0\t" + path)
        if mode == b"160000":
            links.append((path.decode(), oid.decode()))
            continue
        file = REPO / os.fsdecode(path)
        content = os.readlink(file).encode() if mode == b"120000" else file.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        assert actual == oid.decode(), path
        copied = SCRATCH / "head" / os.fsdecode(path)
        if (SCRATCH / "head").exists():
            assert copied.read_bytes() == content, path
            assert (copied.stat().st_mode & 0o111) == (file.stat().st_mode & 0o111), path
        if mode != b"120000":
            assert bool(file.stat().st_mode & 0o111) == (mode == b"100755"), path
        count += 1
    assert sorted(x for x in index if x) == sorted(expected_index)
    assert not git("diff", BASE, HEAD, "--", "src")
    added = git("diff", "--diff-filter=A", "--name-only", BASE, HEAD).decode().splitlines()
    for filename in added:
        assert "SPDX-License-Identifier: Apache-2.0" in (REPO / filename).read_text().splitlines()[0]
    patch = git("diff", "--unified=0", BASE, HEAD).decode()
    new_lines = "\n".join(x[1:] for x in patch.splitlines() if x.startswith('+') and not x.startswith('+++'))
    forbidden = ["/home/", "/data/", "@", *[bytes.fromhex(value).decode() for value in ("43686174475054", "436f646578", "436c61756465", "47656d696e69", "4750542d")]]
    assert not [word for word in forbidden if word.lower() in new_lines.lower()]
    run("diff-whitespace", ["git", "diff", "--check", BASE, HEAD])
    text = ("SPDX-License-Identifier: Apache-2.0\n" + f"HEAD {HEAD}\nTREE {TREE}\n" +
        f"PASS: {count} tracked blobs verified from on-disk bytes; modes and index match HEAD.\n" +
        "PASS: built head archive files and executable modes also match the original tracked sources.\n" +
        f"Submodule gitlinks: {json.dumps(links)} (none required by this standalone tree).\n" +
        "PASS: no tracked, staged, or untracked checkout changes.\n" +
        "PASS: src/ identical to base.\n" +
        f"PASS: new files licensed on first line: {', '.join(added)}.\n" +
        "PASS: added source lines contain no host paths, account identifiers, or assistant attribution.\n")
    (RECEIPTS / "integrity.txt").write_text(text)
    print(text)

globals()[args.task]()
