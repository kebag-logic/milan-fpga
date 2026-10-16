#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The execution audit's controls: each guard refuses its control by name, and real work stays clean.

Run inside the image as root, with the network disabled (it plants programs in
`/usr/local/bin` and removes them):

    python3 ci/image/exec_audit.py --selftest

The controls' own reviewed entries (`CONTROLS`) are added to the reviewed lists
for these steps only; the production lists in `exec-audit.json` hold none of them.
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

from exec_audit import PROCESS_ROOT, STREAM_WAIT, Origin, _record, audit_step
from exec_operands import EXEC_ONLY

NOTHING = "it installs and fetches nothing."
#: The controls' own reviewed entries, by list: each is accepted only in these controls.
CONTROLS = {
    "inline_programs": {
        hashlib.sha256(text.encode()).hexdigest(): {
            "form": form, "interpreter": family, "source": "ci/image/exec_audit_selftest.py", "text": text,
            "reason": f"The audit's own pinned {family} control: it prints a constant; {NOTHING}"}
        for text, family, form in (("print(1)", "python", "inline"), ("print q(pinned-perl)\n", "perl", "inline"),
                                   ('console.log("pinned-node")', "node", "inline"),
                                   ("puts pinned-tcl\n", "tclsh", "stream"), ("puts /tmp/<job>\n", "tclsh", "stream"))},
    "generated_programs": {
        hashlib.sha256(b"import sys\nprint('/tmp/<job>')\n").hexdigest(): {
            "generator": "ci/image/exec_audit_selftest.py", "interpreter": "python", "kind": "script",
            "name": "zz_generated.py", "reason": f"The audit's own generated control: it prints a job-temporary path; "
                                                 f"{NOTHING}"}},
    "checkout_writes": {
        "zz_reviewed_write.txt": {"by": "ci/image/exec_audit_selftest.py",
                                  "reason": "The audit's own control: a step rewrites a reviewed checkout file."}},
}


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
    step("a static binary planted in an image directory before the job", f"{SYSTEM}/zz_static_probe",
         "image program not in the allowlist: zz_static_probe")
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
    step("an unlisted shebang script in an image directory before the job", "zz_shebang_probe",
         "image script not in the allowlist: zz_shebang_probe")
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
    """A program is the image's own file by its identity, or needs a traced build output's bytes; a copy,
    changed or not, of anything else is refused, whatever its name or directory."""
    try:
        step("a copied image program with a byte appended, installed in an image directory under a listed name",
             f"cp /usr/bin/printenv {SYSTEM}/cp && printf '\\0' >> {SYSTEM}/cp && {SYSTEM}/cp HOME",
             "program without provenance: cp")
    finally:
        (SYSTEM / "cp").unlink(missing_ok=True)
    (base / "tool.py").write_text("print('ok')\n")
    step("a copied image program with a byte appended, named python3, given a checkout script",
         f"cp /usr/bin/true {base}/bin/python3 && printf '\\0' >> {base}/bin/python3 && "
         f"{base}/bin/python3 {base}/tool.py", "program without provenance: python3")
    step("a copy of bash named dash, given an inline program",
         f"cp /usr/bin/bash {base}/bin/dash && {base}/bin/dash -c 'echo renamed; shopt -s extglob'",
         "program without provenance: dash")
    step("an unlisted program the job copies from the image",
         f"cp /bin/true {base}/bin/zz_copied_program && {base}/bin/zz_copied_program",
         "program without provenance: zz_copied_program")
    step("a copied image program with a byte appended has no provenance",
         f"cp /usr/bin/printenv {base}/bin/zz_appended && printf '\\0' >> {base}/bin/zz_appended && "
         f"{base}/bin/zz_appended --version", "program without provenance: zz_appended")
    step("a renamed copy of the image's pip3 script is judged as the pip it reproduces",
         f'cp "$(command -v pip3)" {base}/bin/zz_copied_tool && python3 {base}/bin/zz_copied_tool --version',
         "installer executed: pip")
    step("a reviewed generated program is accepted with its job-temporary paths masked",
         f"printf \"import sys\\nprint('{base}/data')\\n\" > {base}/bin/zz_generated.py && "
         f"python3 {base}/bin/zz_generated.py", None)
    step("a generated program with one more statement is not the reviewed one",
         f"printf \"import sys\\nprint('{base}/data')\\nsys.exit(0)\\n\" > {base}/bin/zz_extended.py && "
         f"python3 {base}/bin/zz_extended.py", "script without provenance: zz_extended.py")
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
    (base / "zz_reviewed_write.txt").write_text("before\n")
    report = step("a checkout file in the reviewed write list is recorded, not refused",
                  f"printf 'after\\n' > {base}/zz_reviewed_write.txt", None)
    assert report.get("checkout_writes") == ["zz_reviewed_write.txt"], report
    step("a step that fails under the disabled network", "exit 7", "step exited 7")


def text_digest(text: str) -> str:
    """The digest an unpinned program's finding names."""
    return hashlib.sha256(text.encode()).hexdigest()


def interpreter_programs(step: Step, base: Path) -> None:
    """Every image interpreter, under every installed spelling, reaches a text digest or a named refusal."""
    for command, expect, text in (
            ("perl -e 'print qq(PERL-E\\n)'", "unpinned inline program: perl", "print qq(PERL-E\\n)\n"),
            ("perl -le 'print q(PERL-LE)'", "unpinned inline program: perl", "print q(PERL-LE)\n"),
            ("perl -wE 'say q(PERL-WE)'", "unpinned inline program: perl", "say q(PERL-WE)\n"),
            ("perl -l012e 'print q(PERL-L012E);' -e 'print q(2)'", "unpinned inline program: perl",
             "print q(PERL-L012E);\nprint q(2)\n"),
            ("node -e 'console.log(\"NODE-E\")'", "unpinned inline program: node", 'console.log("NODE-E")'),
            ("node --eval='console.log(\"NODE-EVAL\")'", "unpinned inline program: node", 'console.log("NODE-EVAL")'),
            ("node -p -e '\"NODE-P\"'", "unpinned inline program: node", '"NODE-P"'),
            ("printf 'puts TCL-STREAM\\n' | tclsh", "unpinned streamed program: tclsh8.6", "puts TCL-STREAM\n"),
            ("printf 'puts TCL-VERSIONED\\n' | tclsh8.6", "unpinned streamed program: tclsh8.6",
             "puts TCL-VERSIONED\n"),
            ("printf 'print(4)\\n' | python3", "unpinned streamed program: python3.12", "print(4)\n")):
        report = step(f"an unlisted program text is refused: {command}", f"{command} >/dev/null", expect)
        assert [f.get("sha256") for f in report["findings"]] == [text_digest(text)], (command, report["findings"])
    step("pinned Perl, Node and Tcl texts are accepted",
         "perl -le 'print q(pinned-perl)' && node -e 'console.log(\"pinned-node\")' && "
         "printf 'puts pinned-tcl\\n' | tclsh8.6", None)
    step("a pinned streamed text is accepted with its job-temporary path masked",
         f"printf 'puts {base}/report\\n' | tclsh", None)
    report = step("a job-temporary path with a .. component is not masked past it",
                  f"printf 'puts {base}/../report\\n' | tclsh", "unpinned streamed program: tclsh8.6")
    assert [f.get("sha256") for f in report["findings"]] == [text_digest("puts /tmp/<job>/../report\n")], report
    (base / "tool.pl").write_text("print qq(ok\\n);\n")
    (base / "tool.tcl").write_text("puts ok\n")
    (base / "tool.js").write_text("console.log('ok');\n")
    step("checkout scripts run by Perl, Node and Tcl, after switches", f"perl -w -I {base} {base}/tool.pl && "
         f"node {base}/tool.js && tclsh -encoding utf-8 {base}/tool.tcl && tclsh8.6 {base}/tool.tcl", None)
    step("an installed spelling the allowlist does not name", "perl5.38.2 -e 1",
         "interpreter not in the allowlist: perl5.38.2")
    for command, expect in (("perl -MPOSIX -e 1", "perl switch -M is not modelled"),
                            ("perl -x -e 1", "perl switch -x is not modelled"),
                            ("node -r fs -e 1", "node option -r is not modelled"),
                            ("node -i -e 1", "node option -i is not modelled"),
                            ("bash -i -c true", "shell option -i reads code from start files"),
                            ("bash --login -c true", "shell option --login reads code from start files"),
                            ("python3 -i -c 1", "python option -i is not modelled")):
        step(f"a command line the readers do not model is refused: {command}",
             f"{command} </dev/null >/dev/null 2>&1 || true", f"interpreter command line refused: {expect}")
    (base / "socket_stream.py").write_text(
        "import socket, subprocess\nreader, writer = socket.socketpair()\nwriter.sendall(b'print(5)\\n')\n"
        "writer.close()\nsubprocess.run(['python3', '-'], stdin=reader, check=True)\n")
    step("a streamed program the audit cannot read is refused", f"python3 {base}/socket_stream.py",
         "streamed program not readable at its exec: python3.12")


def masks(step: Step, base: Path) -> None:
    """A program text names a job-written checkout file like a job-temporary one; a file the checkout held stays."""
    with tempfile.TemporaryDirectory(prefix="zz-checkout-", dir="/var/tmp") as directory:
        root = Path(directory)
        (root / "sub").mkdir()
        (root / "sub/held.tcl").write_text("puts held\n")
        origin = Origin(root, CONTROLS, watch=False)
        for text, expect in ((f"source {{{root}/sub/held.tcl}}", f"source {{{root}/sub/held.tcl}}"),
                             (f"source {{{root}/sub/.mut-x1y2z3.tcl}}", f"source {{{root}/sub/<job>}}"),
                             (f"source {{{root}/new/deep.tcl}}", f"source {{{root}/<job>}}"),
                             (f"source {{{root}/sub/../held.tcl}}", f"source {{{root}/sub/../held.tcl}}"),
                             ("source {/tmp/zz/a.tcl}", "source {/tmp/<job>}"),
                             ("source {/var/tmp/zz/a.tcl}", "source {/var/tmp/zz/a.tcl}")):
            assert origin.masked(text.encode()) == text_digest(expect), (text, expect)
    print("PASS: a job-written checkout path in a program text is masked; a held file, `..` and /var/tmp stay")


def loader_errors(step: Step, base: Path) -> None:
    """A load that fails returns its own error and names its own reason; bash's in-process fallback is judged."""
    (base / "noshebang.sh").write_text("echo checkout-fallback\n")
    (base / "noshebang.sh").chmod(0o755)
    step("a checkout text file without #! that bash runs itself is a checkout script", f"{base}/noshebang.sh", None)
    report = step("a job-written text file without #! that bash runs itself is judged as a bash script",
                  f"printf 'echo fallback\\n' > {base}/bin/zz_noshebang && chmod +x {base}/bin/zz_noshebang && "
                  f"{base}/bin/zz_noshebang", "script without provenance: zz_noshebang")
    assert any(row["invocation"] == "zz_noshebang" and row["kind"] == "script" for row in report["population"])
    report = step("dash runs a text file without #! by an exec of /bin/sh, which the audit judges",
                  f"printf 'true\\n' > {base}/bin/zz_dash_fallback && chmod +x {base}/bin/zz_dash_fallback && "
                  f"sh -c '{base}/bin/zz_dash_fallback; true'", None)
    assert any(row["invocation"] == "zz_dash_fallback" for row in report["population"]), report["population"]
    step("a binary file bash refuses to run is not judged as a script",
         f"printf 'zz\\0\\n' > {base}/bin/zz_binary && chmod +x {base}/bin/zz_binary && "
         f"! {base}/bin/zz_binary 2>/dev/null", None)
    step("a missing #! interpreter fails as the exec fails, and nothing runs",
         f"printf '#!/nonexistent/zz_interpreter\\n' > {base}/bin/zz_missing && chmod +x {base}/bin/zz_missing && "
         f"! {base}/bin/zz_missing 2>/dev/null", None)
    step("a #! interpreter through the process filesystem is refused with its own reason",
         f"printf '#!{PROCESS_ROOT}/self/exe\\n' > {base}/bin/zz_refused && chmod +x {base}/bin/zz_refused && "
         f"! {base}/bin/zz_refused 2>/dev/null", f"exec refused: exec through {PROCESS_ROOT}: not a file on a path")


def selftest(names: dict[str, object]) -> int:
    """Each control is judged as the audit must judge it, by name."""
    names = {**names, **{key: {**names.get(key, {}), **entries} for key, entries in CONTROLS.items()}}
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

        for group in (abi_and_target, installers_and_programs, interpreter_programs, provenance, masks,
                      loader_errors, checkout):
            group(step, base)
    return 0
