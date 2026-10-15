#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The execution audit's controls: each guard refuses its control by name, and real work stays clean.

Run inside the image as root, with the network disabled (it plants programs in
`/usr/local/bin` and removes them):

    python3 ci/image/exec_audit.py --selftest
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile
import time
from typing import Callable
import zipfile

from exec_audit import PROCESS_ROOT, STREAM_WAIT, _record, audit_step
from exec_operands import EXEC_ONLY


#: Controls for the exec ABI: an x86-64 program that execs through the i386 or the x32 entry.
TRAMPOLINE = r'''static const char path[] = "%s";
int main(void) {
    long result;
#ifdef X32
    __asm__ volatile ("syscall" : "=a"(result) : "a"(0x40000000L + 520), "D"(path), "S"(0), "d"(0)
                      : "rcx", "r11", "memory");
#else
    __asm__ volatile ("int $0x80" : "=a"(result) : "a"(11), "b"(path), "c"(0), "d"(0) : "memory");
#endif
    return result == 0 ? 0 : 99;
}
'''
#: Controls for the exec target: a program run from a memfd, from a deleted file, and through the
#: process filesystem's descriptor links.
NON_PATH = r'''import os, shutil, sys
how, root, self_fds = sys.argv[1:4]
with open("/bin/true", "rb") as source:
    image = source.read()
if how == "memfd":
    descriptor = os.memfd_create("zz_hidden")
    os.write(descriptor, image)
    os.execve(descriptor, ["zz_hidden"], {})
if how == "deleted":
    path = os.path.join(root, "zz_deleted")
    shutil.copy("/bin/true", path)
    descriptor = os.open(path, os.O_RDONLY)
    os.unlink(path)
    os.execve(descriptor, ["zz_deleted"], {})
descriptor = os.memfd_create("zz_linked")
os.write(descriptor, image)
os.execv(f"{self_fds}/{descriptor}", ["zz_linked"])
'''
#: The real offline install of a local wheel, run in-process through pip's own entry point.
WHEEL = ("import runpy, sys; sys.argv = ['pip', 'install', '--no-index', '--no-deps', "
         "'--disable-pip-version-check', '--target', {target!r}, {wheel!r}]; "
         "runpy.run_module('pip', run_name='__main__')")
SYSTEM = Path("/usr/local/bin")

Step = Callable[[str, str, "str | None"], dict]


def abi_and_target(step: Step, base: Path) -> None:
    """Calls the audit cannot read are refused before they run: a foreign ABI, a target that is not a path."""
    (base / "static.c").write_text("int main(void) { return 0; }\n")
    report = step("a static binary the step builds is observed and has provenance",
                  f"gcc -static -o {base}/static {base}/static.c && {base}/static", None)
    assert any(row["provenance"].startswith("built by") for row in report["population"]), report["population"]
    shutil.copy(base / "static", SYSTEM / "zz_static_probe")
    step("a static binary planted in a system directory", f"{SYSTEM}/zz_static_probe",
         "system program not in the allowlist: zz_static_probe")
    (SYSTEM / "zz_static_probe").unlink()
    marker = base / "marker"
    (base / "marker-stub").write_text(f"#!/bin/sh\ntouch {marker}\n")
    (base / "marker-stub").chmod(0o755)
    for abi, define, expect in (("i386", "", "i386 system call refused: 11"),
                                ("x32", "-DX32 ", "x32 system call refused: 520")):
        (base / f"{abi}.c").write_text(TRAMPOLINE % (base / "marker-stub"))
        step(f"a static program that execs through the {abi} entry is refused before the exec runs",
             f"gcc -static {define}-o {base}/{abi} {base}/{abi}.c && {base}/{abi}", expect)
        assert not marker.exists(), f"the {abi} exec ran"
    (base / "non_path.py").write_text(NON_PATH)
    for how, expect in (("memfd", "exec of a descriptor that is not a file on a path: /memfd:zz_hidden"),
                        ("deleted", "exec of a descriptor that is not a file on a path"),
                        ("linked", f"exec through {PROCESS_ROOT}: not a file on a path")):
        step(f"an unlisted copy run from a {how} descriptor is refused before it runs",
             f"python3 {base}/non_path.py {how} {base} {_record('self', 'fd')}", expect)


def installers_and_programs(step: Step, base: Path) -> None:
    """Installers by name, module, inline or streamed program; interpreter programs by digest only."""
    for interpreter in EXEC_ONLY:
        path = shutil.which(interpreter)
        symbols = subprocess.run(["readelf", "--dyn-syms", "--wide", str(Path(path).resolve())],
                                 capture_output=True, text=True, check=True).stdout
        assert not re.search(r"\bdl(?:m)?open\b", symbols), f"{interpreter} imports a dynamic loader entry"
        print(f"PASS: the exec-only interpreter {interpreter} imports no dynamic loader entry")
    step("a scripted installer run by name", "pip3 --version", "installer executed: pip3")
    step("a scripted package manager run by name", "npm --version", "installer executed: npm")
    wheel = base / "zz_probe_pkg-0.1-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("zz_probe_pkg/__init__.py", "")
        archive.writestr("zz_probe_pkg-0.1.dist-info/METADATA",
                         "Metadata-Version: 2.1\nName: zz-probe-pkg\nVersion: 0.1\n")
        archive.writestr("zz_probe_pkg-0.1.dist-info/WHEEL",
                         "Wheel-Version: 1.0\nGenerator: fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
        archive.writestr("zz_probe_pkg-0.1.dist-info/RECORD", "")
    step("a real offline install of a local wheel",
         f"python3 -m pip install --no-index --no-deps --disable-pip-version-check --target "
         f"{base}/installed {wheel} && test -f {base}/installed/zz_probe_pkg/__init__.py",
         "installer module executed: pip")
    inline = WHEEL.format(target=f"{base}/inline", wheel=str(wheel))
    step("a real offline install of a local wheel by an inline program",
         f"python3 -c {shlex.quote(inline)} && test -f {base}/inline/zz_probe_pkg/__init__.py",
         "unpinned inline program: python3.12")
    streamed = WHEEL.format(target=f"{base}/streamed", wheel=str(wheel))
    step("a real offline install of a local wheel by a streamed program",
         f"printf '%s\\n' {shlex.quote(streamed)} | python3 - && test -f {base}/streamed/zz_probe_pkg/__init__.py",
         "unpinned streamed program: python3.12")
    (base / "spawner.py").write_text(
        "import subprocess, sys\nsubprocess.run([sys.executable, '-'], input='print(3)\\n', text=True, check=True)\n")
    started = time.monotonic()
    report = step("a streamed program its spawning parent writes after the exec is read whole",
                  f"python3 {base}/spawner.py", "unpinned streamed program: python3.12")
    assert time.monotonic() - started < STREAM_WAIT / 2, "the streamed program waited out its deadline"
    assert hashlib.sha256(b"print(3)\n").hexdigest() in {f["sha256"] for f in report["findings"]}, report["findings"]
    step("an unpinned bash inline program", "bash -c 'true'", "unpinned inline program: bash")
    (base / "tool.py").write_text("print('ok')\n")
    step("a pinned inline program and a checkout script", f"python3 -c 'print(1)' && python3 {base}/tool.py", None)
    step("an interpreter given a missing script runs nothing from it",
         f"python3 {base}/missing.py 2>/dev/null || true", None)
    (SYSTEM / "zz_shebang_probe").write_text("#!/bin/sh\nexit 0\n")
    (SYSTEM / "zz_shebang_probe").chmod(0o755)
    step("an unlisted shebang script in a system directory", "zz_shebang_probe",
         "system script not in the allowlist: zz_shebang_probe")
    (SYSTEM / "zz_shebang_probe").unlink()
    (base / "bin").mkdir()
    (base / "bin/apt-get").write_text("#!/bin/sh\nexit 0\n")
    (base / "bin/apt-get").chmod(0o755)
    step("a shebang apt-get outside the system directories", f"{base}/bin/apt-get update",
         "installer executed: apt-get")
    (base / "fetched.sh").write_text("exit 0\n")
    step("a fetched program piped to a shell", f"curl -fsS file://{base}/fetched.sh | sh",
         "fetched program executed by dash")
    (base / "bin/gem").write_text("#!/bin/sh\nexit 0\n")
    (base / "bin/gem").chmod(0o755)
    step("an installing subcommand", f"{base}/bin/gem install zz-probe", "installer subcommand executed: gem install")
    (base / "bin/cargo").write_text("#!/bin/sh\nexit 0\n")
    (base / "bin/cargo").chmod(0o755)
    step("an installing subcommand after leading options", f"{base}/bin/cargo +stable -v install zz-probe",
         "installer subcommand executed: cargo install")


def provenance(step: Step, base: Path) -> None:
    """A program needs a traced build output's bytes; a copy, changed or not, of anything else is refused."""
    step("an unlisted program the job copies from the image",
         f"cp /bin/true {base}/bin/zz_copied_program && {base}/bin/zz_copied_program",
         "program without provenance: zz_copied_program")
    step("a copied image program with a byte appended has no provenance",
         f"cp /usr/bin/printenv {base}/bin/zz_appended && printf '\\0' >> {base}/bin/zz_appended && "
         f"{base}/bin/zz_appended --version", "program without provenance: zz_appended")
    step("a renamed copy of the image's pip3 script is judged as the pip it reproduces",
         f'cp "$(command -v pip3)" {base}/bin/zz_copied_tool && python3 {base}/bin/zz_copied_tool --version',
         "installer executed: pip")
    step("a job-written Python script that is not pinned has no provenance",
         f"printf 'print(2)\\n' > {base}/bin/zz_written.py && python3 {base}/bin/zz_written.py",
         "script without provenance: zz_written.py")
    report = step("a stub the job writes with the bytes of the image's initctl is judged as initctl",
                  f"printf '#!/bin/sh\\nexit 0\\n' > {base}/bin/zz_stub && sh {base}/bin/zz_stub", None)
    assert any(row["invocation"] == "initctl" for row in report["population"]), report["population"]
    step("a job-written dash script and a dash inline program are judged by their execs",
         f"printf '#!/bin/sh\\ntrue\\n' > {base}/bin/zz_dash && chmod +x {base}/bin/zz_dash && "
         f"{base}/bin/zz_dash && sh -c 'true'", None)
    (base / "built.c").write_text("int main(void) { return 0; }\n")
    step("a program the job built under a temporary name, then renamed",
         f"cc -o {base}/renamed.part {base}/built.c && mv {base}/renamed.part {base}/renamed && {base}/renamed",
         None)
    step("a program the step built, and an installed copy of it",
         f"cc -o {base}/built {base}/built.c && {base}/built && install -m 755 {base}/built {base}/copy && "
         f"{base}/copy", None)
    step("a program built without -o, as a.out", f"cd {base} && cc built.c && ./a.out", None)
    step("a failed build's declared output is not a build output",
         f"cp /bin/true {base}/bin/zz_failed && ! cc -o {base}/bin/zz_failed {base}/missing.c 2>/dev/null && "
         f"{base}/bin/zz_failed", "program without provenance: zz_failed")
    (base / "leak.c").write_text("#include <stdlib.h>\nint main(void) { return malloc(1) == 0; }\n")
    step("a LeakSanitizer build runs its leak check under the audit",
         f"cc -fsanitize=address -o {base}/leak {base}/leak.c && ! {base}/leak 2>{base}/leak.log && "
         f"grep -q 'detected memory leaks' {base}/leak.log", None)


def checkout(step: Step, base: Path) -> None:
    """What the walker read is what ran: a checkout file changed during the job is caught."""
    (base / "checkout.sh").write_text("exit 0\n")
    step("a link the step makes to a checkout script is judged as that script",
         f"mkdir -p {base}/shadow && ln -s {base}/checkout.sh {base}/shadow/run.sh && bash {base}/shadow/run.sh",
         None)
    step("a link named as an installer is caught by that name",
         f"ln -s {base}/checkout.sh {base}/shadow/apt-get && bash {base}/shadow/apt-get",
         "installer executed: apt-get")
    (base / "rewritten.sh").write_text("exit 0\n")
    step("a checkout script an earlier program rewrites is caught at its exec",
         f"printf 'true\\n' > {base}/rewritten.sh && bash {base}/rewritten.sh",
         "checkout file changed before it ran: rewritten.sh")
    (base / "sourced.sh").write_text("exit 0\n")
    step("a checkout file an earlier program rewrites is caught though no exec reads it",
         f"printf 'true\\n' > {base}/sourced.sh && . {base}/sourced.sh",
         "checkout file changed during the job: sourced.sh")
    step("a step that fails under the disabled network", "exit 7", "step exited 7")


def selftest(names: dict[str, object]) -> int:
    """Each control is judged as the audit must judge it, by name."""
    environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/root"),
                   "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    with tempfile.TemporaryDirectory(prefix="exec-audit-") as directory:
        base = Path(directory)

        def step(label: str, command: str, expect: str | None) -> dict:
            """Audit one control step, its text the step's own, and require its expected judgment."""
            report = audit_step({"job": "selftest", "label": label, "argv": ["bash", "-e", "-c", command],
                                 "text": command}, names, base, environment)
            reasons = [f["reason"] for f in report["findings"]]
            if expect is None:
                assert not reasons, (label, reasons, report["population"])
            else:
                assert any(expect in reason for reason in reasons), (label, expect, reasons)
            print(f"PASS: {label}: " + (f"caught ({expect})" if expect else "clean"))
            return report

        for group in (abi_and_target, installers_and_programs, provenance, checkout):
            group(step, base)
    return 0
