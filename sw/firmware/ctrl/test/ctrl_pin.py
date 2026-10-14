# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_pin.py - the TSN stack's pin, held at every gate that builds the stack (#697).

The pin check itself is ctrl_build.stack_pin: the submodule at its gitlink,
and its checkout the gitlink's whole tree (the same paths, types and modes,
every file hashing to the tree's blob). Every Python gate that builds the stack
calls it first. This module holds the rest, for the boundary gate
(ctrl_boundary.py).

THE HOOK (ctrl_build.audited). The pin proof's modules are ctrl_build.py and
this one; what decides the pin is ctrl_build.DECISION (stack_gitlink,
stack_pin and the command line's main). Before the proof's first Git call,
where ctrl_build.py defines its helper (ctrl_build.git), the proof installs a
PEP 578 audit hook, which stays for the life of the process. An audit hook
cannot be removed, and this one binds, as it is installed, all it judges by
(the helper's code, ctrl_build.py's namespace, the Git program, and every
function, builtin and constant it uses), so no later rebinding of a name
changes how it judges an event; what it judges is the events the interpreter
raises. While the proof runs (a function of DECISION, in any thread,
or the top level of one of the proof's modules), the hook refuses every
process start the interpreter audits but the helper's: the subprocess module
starting, for the helper's own code, the Git program PATH named when the proof
was loaded (ctrl_build.GIT), with exactly the proof's own environment
(ctrl_build.GIT_ENVIRONMENT; under a capture, also the builders' names its
audit hook adds, ctrl_build.CAPTURED, which Git does not read), each key and
value a plain str, so that what Git is given is what the hook judged: GIT_NO_REPLACE_OBJECTS=1, a
GIT_GRAFT_FILE that cannot exist, no system or global configuration,
GIT_NO_LAZY_FETCH=1, and nothing the proof inherits. It
refuses every thread start there too, since a thread could change a start's
arguments after the hook has read them. It
refuses exec, compile and an import of importlib, and the reaches into its own
state (the collector's lists of objects, a trace or profile function), while
a function of DECISION runs and wherever the proof's own code asks for them,
the helper's included; this module puts its code under the hook by raising
ctrl_build.PROOF_EVENT. It refuses at any time a replacement of what a
function of the proof runs (its code or its defaults). Each refusal is a
ctrl_build.AuditRefusal naming the line of the proof that asked, written first
to the standard error, so a refusal that is caught and ignored is still read.
A function of the proof's
modules that starts a process while the proof is not running is not judged:
ctrl_build.py's build functions and run, and this module's tool runs (make,
and the gates the controls run), all through fw_gtest.run.

THE THREAT MODEL (#697, the round-12 ruling). What the pin proof defends
against is the state it reads: the checkout's files and modes, Git's object
store, refs, configuration and attributes, and the environment the proof
inherits. Git is given none of that environment, so no variable of it can
redirect Git's repository, index, object store, configuration, attributes or
replacement refs; ctrl_pin_env.py sets each such variable in a control. The
proof's own modules are reviewed source, outside the model: a rebinding of
sys.audit, or an object crafted inside them, is a change review sees. The
hook is defence in depth against such code. It sees a launch through the
interpreter's audited interfaces only: not ctypes or an extension module, and
on the runner's CPython 3.12.3 not _posixsubprocess.fork_exec, which
subprocess calls just after raising its own event from Python (CPython 3.14
audits fork_exec itself). What Git itself starts is outside the hook, and so
is code that runs before the hook is installed (ctrl_build.py's top, above
the helper). Every object the proof reads, the pinned commit and each tree
under it, is read raw and hashed here against its id (ctrl_build.stored), so
a forged or corrupt object is refused by its place; no blob is read. One
parser reads both repositories' keys (ctrl_build.parsed_key). The stack's
own configuration may hold only the keys Git writes itself for a clone and a
submodule (its allowlist, ctrl_build.STACK_CONFIG); any other is refused by
name before an object is read. The superproject's may hold no key of a
promisor remote, its transport or an fsmonitor, judged by section and
variable whatever the subsection (ctrl_build.SUPERPROJECT_REFUSED), so it
declares no promisor remote in any key spelling Git reads; its other keys are
not judged. core.fsmonitor=false and GIT_NO_LAZY_FETCH=1 are defence in depth;
ctrl_pin_store.py holds the controls of the store and the configuration.

THE CENSUS (census). A fast lint of the two modules' syntax trees, not their
text, beside the hook's own check of them (exercised: the pin proof run from
the texts it is given, under the hook, each refusal reported at its line).
The guarantee is the hook's: the lint reads the modules as written, so it does
not see a rebinding by assignment or code built at run time. It refuses:
- outside the helper, any reference to a process-launch facility, by import,
  alias or attribute: the subprocess, pty and asyncio.subprocess modules and
  their members; os.system, os.popen, os.exec*, os.spawn*, os.posix_spawn*,
  os.fork, os.forkpty and os.startfile; asyncio's create_subprocess_exec and
  create_subprocess_shell. An attribute so named is refused on any object, so
  os reached through another module is refused too;
- anywhere, the helper included, eval, exec, compile, __import__, importlib
  and builtins, by name, by import or as an attribute of any object (but
  re.compile); outside the hook, the reflection that reaches an object without
  naming it (getattr, setattr, delattr, vars, globals, locals, an attribute
  beginning with an underscore but __name__, a frame's attributes,
  sys.modules); a wildcard import;
- in what decides the pin and every function, class and constant of
  ctrl_build.py it names, followed through each, any name outside the proof's
  vocabulary (VOCABULARY, BUILTINS, ATTRIBUTES): a few names of os, hashlib,
  stat, pathlib and argparse, and builtins and attributes of its own values;
- ctrl_build.py without the helper or with its name bound again, and a helper
  environment that would read a replacement or a graft.

THE MAKEFILES. A Makefile among the firmware's builders is read with make's
own database (make -p) and dry run (make -n -B --trace), never restated here,
with the stack it builds named through STACK_DIR. A target whose own recipe
names that stack (its include path, its sources) must have a target that runs
the pin check (ctrl_build.py --stack-pin) as a prerequisite, so no target
reaches the stack unpinned, whichever target is run alone; a recipe that names
the checkout's stack rather than STACK_DIR's is refused too, since no stack
could be checked in its place.

THE CONTROLS (pin_controls, under ctrl_boundary.py --selftest). The pin check
passes a clone of the stack at its gitlink and refuses, by name, the clone with
a source, a test, a script, a CMake file or a file no gate builds edited, with
an edit the index hides, with a file the tree does not hold, with a symbolic
link standing in for a file, with a file made executable, and at another
revision. It refuses, by the edited source's name, an edit that a replacement
of the pinned tree's src/ or of the pinned commit would make git read as
pinned, and one beside a graft file; and, by the filter's key, one a clean
filter given through the clone's attributes turns back into the pinned bytes. The pin proof as the
checkout holds it runs to its verdict under the hook; and the proof run under
the hook with one bypass planted (census_arms, HOOK_PLANTS) ends, before any
build, in the hook's refusal at the plant's line: a git command run outside
the helper (by the harness's runner, under a computed name, as a dashed
program, and by the Git program's path with the helper's environment), one
whose refusal is caught and ignored, an aliased import of subprocess,
os.system and exec of a string; the helper's name rebound by attribute
assignment in either module, and os.walk rebound to start Git;
inspect.builtins.exec, eval and compile, dynamic code a library runs where
the pin is decided, an import of importlib.metadata and
pkgutil.importlib.import_module; exec, eval and compile inside the helper;
this module's code kept from the hook by rebinding sys.audit, then exec; a
thread started, the decision's code replaced, the collector's list of objects
and a trace function. Code of this module filed under another name, then
exec, is refused at that name's line; the Git program rebound, for the
program the helper would start; and the helper's environment without either
of its two settings, and with the builtins a hook could look up rebound, by
the setting's name. The helper's environment the caller's again, with a
variable added (GIT_DIR), and with a key or a value that is not a plain str,
are refused at the helper's line, the variable by its name. The
inherited-environment controls follow (ctrl_pin_env.py), then those of the
object store and the repositories' own configuration (ctrl_pin_store.py),
R585-12's forged src/ tree, R584-12's, R585-14's and R584-14's promisors among
them. The MAAP differential (both its modes) and the AECP
lane's arms, campaign and wire comparison refuse an edited clone before
building it. Then every target of
every Makefile builder whose dry run reaches the stack is run for real, in a
scratch copy of its directory (the rest of the checkout linked, so its paths
reach what they reach in the checkout), with the system's compilers and a
simulator that builds nothing, against a clone whose wire.h is poisoned: each
must refuse on the pin check and never compile the poisoned header. A planted
copy of the mailbox bench's Makefile whose run-if2 lacks the pin prerequisite
must be refused by name.
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from ctrl_build import (DECISION, HERE, HOOK_REFUSED, PP, PROOF_EVENT, ROOT, STACK, UNLISTED, Refusal, audited, git,
                        git_env, stack_gitlink, stack_pin)
from ctrl_capture import COMPILER
from ctrl_pin_bench import bench_arms
from ctrl_pin_env import create, inherited_arms
from ctrl_pin_store import store_arms
from ctrl_pin_lifecycle import controls as lifecycle_controls
import fw_gtest

#: This module's code is the pin proof's: under the audit hook from here on, as ctrl_build.py's is (THE HOOK).
sys.audit(PROOF_EVENT)

#: The pin proof's modules, in which only the helper (ctrl_build.git) names a process-launch facility.
PROOF = (HERE / "ctrl_build.py", HERE / "ctrl_pin.py")
#: The helper: the one function, of ctrl_build.py, that may name a process-launch facility.
HELPER = git.__name__
#: The audit hook's installer, of ctrl_build.py: the one function of the proof that may use reflection.
HOOK = audited.__name__
#: What decides the pin, in ctrl_build.py: these functions, and all they name, use only the proof's vocabulary.
ROOTS = DECISION
#: The names that start a process: a module's (subprocess, pty, asyncio.subprocess), and a function's of os,
#: asyncio or any object.
LAUNCH_NAMES = frozenset({"subprocess", "pty", "system", "popen", "startfile", "fork", "forkpty", "posix_spawn",
                          "posix_spawnp", "create_subprocess_exec", "create_subprocess_shell",
                          *(verb + tail for verb in ("exec", "spawn")
                            for tail in ("l", "le", "lp", "lpe", "v", "ve", "vp", "vpe"))})
#: Dynamic code, and the reflection that reaches an object without naming it: refused wherever named.
DYNAMIC = frozenset({"eval", "exec", "compile", "__import__", "importlib", "builtins", "__builtins__", "getattr",
                     "setattr", "delattr", "vars", "globals", "locals"})
#: An attribute that reaches an object without naming it: the interpreter's own (a leading underscore, but the
#: __name__ HELPER reads), a frame's or a generator's (f_globals, gi_frame), the table of loaded modules.
REFLECTIVE = re.compile(r"_(?!_name__$)|(?:f|gi|cr|ag|tb)_|modules$")
#: The pin proof's vocabulary: each module it may name, with the names of it it may use.
VOCABULARY = {"os": frozenset({"walk", "readlink"}), "hashlib": frozenset({"new", "algorithms_available"}),
              "stat": frozenset({"S_ISLNK", "S_ISDIR", "S_ISREG", "S_IXUSR"}), "pathlib": frozenset({"Path"}),
              "argparse": frozenset({"ArgumentParser"})}
#: The builtins the pin proof may name (and its module's own file name).
BUILTINS = frozenset({"Exception", "bytes", "dict", "filter", "int", "len", "list", "print", "sorted", "str",
                      "tuple", "__file__"})
#: The attributes of its own values the pin proof may use: of paths, text, bytes, lists, maps, the helper's answer,
#: a hash, a file's status and the command line's parser and arguments.
ATTRIBUTES = frozenset({"add_argument", "append", "as_posix", "decode", "encode", "get", "hex", "hexdigest",
                        "is_symlink", "join", "keys", "lstat", "parent", "parents", "parse_args", "partition", "pop",
                        "raw", "read_bytes", "relative_to", "resolve", "returncode", "rpartition", "split", "st_mode",
                        "stack_pin", "stderr", "stdout", "strip"})

#: A target make's database does not hold: asked for so make prints the database and runs nothing.
NO_GOAL = "ctrl-pin-no-such-goal"
#: make --trace's line before each target's commands, the target in group 1.
TRACE = re.compile(r"^\S+:\d+: (?:update )?target '(.+?)'")
#: What a recipe line that runs the pin check holds.
PIN_RUN = "--stack-pin"
#: The checkout's stack, however a recipe names it (relative or absolute).
CHECKOUT_STACK = STACK.relative_to(ROOT).as_posix()
#: The line the poisoned clone's wire.h ends with; a build that reads it fails naming it.
POISON = "#error PIN-POISON: the poisoned tsn-c-stack was compiled"
#: A simulator that builds nothing: it writes, where Verilator would build it, an executable that passes.
NO_SIMULATOR = '''import sys
from pathlib import Path
args = sys.argv[1:]
if "--Mdir" in args and "-o" in args:
    exe = Path(args[args.index("--Mdir") + 1]) / args[args.index("-o") + 1]
    exe.parent.mkdir(parents=True, exist_ok=True)
    exe.write_text("#!/bin/sh\\nexit 0\\n", encoding="utf-8")
    exe.chmod(0o755)
'''
#: The planted Makefile control: the mailbox bench's run-if2 without the pin check as its prerequisite.
UNPINNED = (ROOT / "tb/verilator/mbx/Makefile", "run-if2: if2-gen | stack-pin\n", "run-if2: if2-gen\n", "run-if2")
#: The counter entry points share the prerequisite, including the RTL-only counter target.
COUNTER_TARGETS = ("counters", "counters-f5", "counters-mutants")
#: How long one bench target may run against the poisoned clone before it is a failure.
BENCH_TIMEOUT_S = 900
#: The pin proof run from a census's texts in a fresh interpreter (exercised): each module compiled from its text
#: under its own path in the checkout, so its lines are its file's; ctrl_build.py first, which installs the audit
#: hook, then ctrl_pin.py; then the command line's pin check. Its arguments: the checkout, the texts (a JSON
#: file, by path from the checkout) and the stack checkout to check.
PROOF_RUN = '''import json
import sys
import types
from pathlib import Path
root, texts = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
for name in ("ctrl_build", "ctrl_pin"):
    for rel, text in texts.items():
        if Path(rel).name == name + ".py":
            module = types.ModuleType(name)
            module.__file__ = str(root / rel)
            sys.modules[name] = module
            exec(compile(text, module.__file__, "exec"), module.__dict__)
sys.exit(sys.modules["ctrl_build"].main(["--stack-pin", sys.argv[3]]))
'''
#: How long that run may take before it is a failure.
PROOF_RUN_TIMEOUT_S = 300
#: Where the pin proof's controls plant in ctrl_build.py: the pin check's reads (of HEAD, of the pinned tree, of
#: the gitlink), the decision's first function, the helper's own import, and the helper environment's settings.
HEAD_READ = 'head = git(stack, "rev-parse", "HEAD")'
TREE_READ = "want = pinned_tree(stack, pin, algorithm)"
ENTRY_READ = 'entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()'
GITLINK_DEF = "\n\ndef stack_gitlink("
HELPER_IMPORT = "    import subprocess\n"
#: Where ctrl_pin.py puts its code under the hook.
REGISTERED = "sys.audit(PROOF_EVENT)\n"
#: Git through the harness's runner, with the helper's environment, bound as the helper (R584-9's E2b and E6).
PLAIN = '''def plain(directory: Path, *args: str, stdin: str | None = None) -> object:
    """git through the harness's runner."""
    res = fw_gtest.run(["git", "-C", str(directory), *args], env=git_env())
    return ctrl_build.GitRun(res.returncode, res.stdout, res.stderr)


ctrl_build.git = plain
'''
#: A key of the helper's environment that the hook would read as GIT_NO_REPLACE_OBJECTS, but Git is given as another.
KEYED = '''import ctrl_build  # noqa: E402


class Key(str):
    """Equal to any key, under GIT_NO_REPLACE_OBJECTS's hash."""

    def __eq__(self, other: object) -> bool:
        return True

    def __hash__(self) -> int:
        return hash("GIT_NO_REPLACE_OBJECTS")


OWN = {k: v for k, v in ctrl_build.GIT_ENVIRONMENT.items() if k != "GIT_NO_REPLACE_OBJECTS"}
ctrl_build.git_env = lambda: {Key("GIT_NO_REPLACE"): "1", **OWN}
'''
#: A value of the helper's environment that the hook would read as 1, but Git is given as 0.
VALUED = '''import ctrl_build  # noqa: E402


class Value(str):
    """The text 1, encoded as 0."""

    def encode(self, *args: object) -> bytes:
        return b"0"


ctrl_build.git_env = lambda: {**ctrl_build.GIT_ENVIRONMENT, "GIT_NO_REPLACE_OBJECTS": Value("1")}
'''
#: The pin proof's standing controls under its audit hook: what each plants; in which pin-proof module; the anchor
#: it replaces there (None: it is added at the module's end); the planted text; the words the hook's refusal must
#: hold; and whether that refusal must name a line of the plant (else it is the helper's own). Each starts a
#: process outside the helper, runs dynamic code, or has the helper start another program or Git unhardened.
HOOK_PLANTS = (
    ("a Git command run by the harness's runner (ctrl_build.run)", "ctrl_build.py", HEAD_READ,
     'head = run(["git", "-C", str(stack), "rev-parse", "HEAD"])', "(subprocess.Popen)", True),
    ("a program named by a computed name (git.__name__)", "ctrl_build.py", TREE_READ,
     'tree = run([git.__name__, "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin])',
     "(subprocess.Popen)", True),
    ("a dashed program (git-ls-tree)", "ctrl_build.py", TREE_READ,
     'tree = run(["git-ls-tree", "-r", "-t", "-z", "--full-tree", pin], cwd=stack)', "(subprocess.Popen)", True),
    ("the Git program by its path, with the helper's environment, by the harness's runner", "ctrl_build.py",
     TREE_READ, 'tree = run([GIT, "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin], env=git_env())',
     "(subprocess.Popen)", True),
    ("a refusal caught and ignored", "ctrl_build.py", TREE_READ,
     'try:\n        run(["git", "-C", str(stack), "status"])\n    except BaseException:\n        pass\n    '
     + TREE_READ,
     "(subprocess.Popen)", True),
    ("an aliased import (from subprocess import run as r)", "ctrl_build.py", TREE_READ,
     'from subprocess import run as r\n    tree = r(["git", "-C", str(stack), "ls-tree", "-r", "-t", "-z", '
     '"--full-tree", pin])', "(subprocess.Popen)", True),
    ("os.system, in a line added to ctrl_pin.py", "ctrl_pin.py", None, 'LISTED = os.system("git ls-files")\n',
     "(os.system)", True),
    ("exec of a string", "ctrl_build.py", ENTRY_READ,
     'exec("entry = run([\'git\', \'ls-files\', \'--stage\', \'--\', rel], cwd=root).stdout.split()")',
     "asks for compile", True),
    ("the helper's name rebound by attribute assignment in ctrl_build.py", "ctrl_build.py", GITLINK_DEF,
     "\n\nimport ctrl_build  # noqa: E402\n\n\n" + PLAIN + GITLINK_DEF, "(subprocess.Popen)", True),
    ("the helper's name rebound by attribute assignment in ctrl_pin.py", "ctrl_pin.py", None,
     "import ctrl_build  # noqa: E402\n\n\n" + PLAIN, "(subprocess.Popen)", True),
    ("os.walk, a name of the proof's vocabulary, rebound to start Git", "ctrl_build.py", GITLINK_DEF,
     '\n\nWALK = os.walk\n\n\ndef walk(top: str) -> object:\n    """os.walk, after a git command."""\n'
     '    run(["git", "-C", str(top), "status", "--porcelain"])\n    return WALK(top)\n\n\nos.walk = walk\n'
     + GITLINK_DEF, "(subprocess.Popen)", True),
    ("inspect.builtins.exec, in lines added to ctrl_pin.py", "ctrl_pin.py", None,
     'import inspect  # noqa: E402\ninspect.builtins.exec("import subprocess; subprocess.run([\'git\', \'ls-files\'])")'
     '\n', "asks for compile", True),
    ("inspect.builtins.eval", "ctrl_build.py", ENTRY_READ,
     'import inspect\n    entry = inspect.builtins.eval("run([\'git\', \'ls-files\', \'--stage\', \'--\', rel], '
     'cwd=root)").stdout.split()', "asks for compile", True),
    ("inspect.builtins.compile", "ctrl_build.py", TREE_READ,
     'import inspect\n    tree = eval(inspect.builtins.compile("run([\'git\', \'ls-tree\', \'-r\', \'-z\', pin], '
     'cwd=stack)", "<plant>", "eval"))', "asks for compile", True),
    ("dynamic code a library runs where the pin is decided (collections.namedtuple)", "ctrl_build.py", ENTRY_READ,
     'import collections\n    collections.namedtuple("Entry", "mode oid stage path")\n    ' + ENTRY_READ,
     "asks for compile", True),
    ("ctrl_pin.py's code filed under another name (code.replace), then exec of a string", "ctrl_pin.py", None,
     'def plant() -> None:\n    """exec of a string."""\n    exec("import os")\n\n\n'
     'PLANT = type(plant)(plant.__code__.replace(co_filename="<elsewhere>"), globals())\nPLANT()\n',
     "<elsewhere>:", False),
    ("an import of importlib.metadata, in a line added to ctrl_pin.py", "ctrl_pin.py", None,
     "import importlib.metadata  # noqa: E402\n", "asks for an import of importlib.metadata", True),
    ("pkgutil.importlib.import_module", "ctrl_build.py", TREE_READ,
     'import pkgutil\n    tree = pkgutil.importlib.import_module("subprocess").run(["git", "-C", str(stack), '
     '"ls-tree", "-r", "-t", "-z", "--full-tree", pin], capture_output=True, encoding="utf-8")', "pin proof", True),
    ("exec of a string inside the helper", "ctrl_build.py", HELPER_IMPORT,
     '    exec("import os; os.system(\'git ls-files\')")\n' + HELPER_IMPORT, "asks for compile", True),
    ("eval inside the helper", "ctrl_build.py", HELPER_IMPORT,
     '    eval("__import__(\'os\').system(\'git ls-files\')")\n' + HELPER_IMPORT, "asks for compile", True),
    ("compile inside the helper", "ctrl_build.py", HELPER_IMPORT,
     '    compile("import os", "<plant>", "exec")\n' + HELPER_IMPORT, "asks for compile", True),
    ("ctrl_pin.py's code not put under the hook (sys.audit rebound first), then exec of a string", "ctrl_pin.py",
     REGISTERED, "sys.audit = lambda *args: None\n" + REGISTERED + 'import inspect  # noqa: E402\n'
     'inspect.builtins.exec("import os")\n', "asks for compile", True),
    ("a thread started, in lines added to ctrl_pin.py", "ctrl_pin.py", None,
     "import threading  # noqa: E402\nthreading.Thread(target=print).start()\n", "(_thread.start_", True),
    ("the decision's code replaced (stack_pin.__code__), in a line added to ctrl_pin.py", "ctrl_pin.py", None,
     "stack_pin.__code__ = mirror.__code__\n", "replaces __code__ of stack_pin", True),
    ("the collector's list of objects, in lines added to ctrl_pin.py", "ctrl_pin.py", None,
     "import gc  # noqa: E402\nOBJECTS = gc.get_objects()\n", "asks for gc.get_objects", True),
    ("a trace function, in a line added to ctrl_pin.py", "ctrl_pin.py", None, "sys.settrace(None)\n",
     "asks for sys.settrace", True),
    ("the Git program rebound by attribute assignment in ctrl_pin.py", "ctrl_pin.py", None,
     'import ctrl_build  # noqa: E402\nctrl_build.GIT = shutil.which("true")\n', "not the Git program", False),
    ("the helper's environment without GIT_NO_REPLACE_OBJECTS", "ctrl_build.py", '"GIT_NO_REPLACE_OBJECTS": "1", ',
     "", "without GIT_NO_REPLACE_OBJECTS=1", False),
    ("the helper's environment without GIT_GRAFT_FILE", "ctrl_build.py", ', "GIT_GRAFT_FILE": NO_GRAFTS', "",
     "with GIT_GRAFT_FILE None", False),
    ("the helper's environment, and the builtins a hook could look up, rebound in ctrl_pin.py", "ctrl_pin.py", None,
     'import ctrl_build  # noqa: E402\nctrl_build.git_env = lambda: dict(os.environ)\n'
     'ctrl_build.type = ctrl_build.dict = ctrl_build.isinstance = ctrl_build.any = lambda *args: True\n',
     "without GIT_NO_REPLACE_OBJECTS=1", False),
    ("the caller's environment passed to Git again, git_env rebound in ctrl_pin.py", "ctrl_pin.py", None,
     'import ctrl_build  # noqa: E402\nctrl_build.git_env = lambda: {**os.environ, **ctrl_build.GIT_ENVIRONMENT}\n',
     "in its environment, which the pin proof's own does not set", False),
    ("a variable added to the proof's own environment (GIT_DIR) in ctrl_pin.py", "ctrl_pin.py", None,
     'import ctrl_build  # noqa: E402\nctrl_build.GIT_ENVIRONMENT["GIT_DIR"] = "elsewhere"\n',
     "with GIT_DIR in its environment", False),
    ("a key of the helper's environment that is another's to the hook (a str subclass)", "ctrl_pin.py", None, KEYED,
     "not all plain str", False),
    ("a value of the helper's environment that Git is given as another (a str subclass)", "ctrl_pin.py", None,
     VALUED, "not all plain str", False),
)


def run(argv: list[str], cwd: Path | None = None, env: dict[str, str] | None = None,
        timeout: int | None = None) -> tuple[int, str]:
    """One tool, through the harness's runner (fw_gtest.run): its output then its errors, its messages in
    English."""
    res = fw_gtest.run(argv, cwd=cwd, timeout=timeout, env={**os.environ, "LC_ALL": "C", **(env or {})})
    return res.returncode, res.stdout + res.stderr


def imported(stmt: ast.Import | ast.ImportFrom) -> list[tuple[ast.alias, str, str]]:
    """Each name an import binds, and what it names: a module (import os: os) or a module's member (from
    pathlib import Path: pathlib.Path)."""
    if isinstance(stmt, ast.Import):
        return [(a, a.asname or a.name.split(".")[0], a.name if a.asname else a.name.split(".")[0])
                for a in stmt.names]
    return [(a, a.asname or a.name, f"{'.' * stmt.level}{stmt.module or ''}.{a.name}") for a in stmt.names]


def scope(top: ast.Module) -> dict[str, list[tuple[str, ast.AST, str]]]:
    """Each name a module binds outside its functions and classes, with every binding of it: a function or class
    ("def", its node), a value ("value", the expression), an import ("import", the alias, what it names), or a
    kind the census does not follow ("other")."""
    bound: dict[str, list[tuple[str, ast.AST, str]]] = {}
    statements = list(top.body)
    while statements:
        stmt = statements.pop(0)
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.setdefault(stmt.name, []).append(("def", stmt, ""))
        elif isinstance(stmt, (ast.Import, ast.ImportFrom)):
            for alias, name, target in imported(stmt):
                bound.setdefault(name, []).append(("import", alias, target))
        elif isinstance(stmt, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            heads = [stmt.target] if isinstance(stmt, ast.For) else \
                [i.optional_vars for i in stmt.items if i.optional_vars] if isinstance(stmt, ast.With) else []
            for node in (n for head in heads for n in ast.walk(head) if isinstance(n, ast.Name)):
                bound.setdefault(node.id, []).append(("other", node, ""))
            statements += stmt.body + (stmt.orelse if not isinstance(stmt, ast.With) else [])
            if isinstance(stmt, ast.Try):
                statements += stmt.finalbody + [s for handler in stmt.handlers for s in handler.body]
        else:
            value = stmt.value if isinstance(stmt, (ast.Assign, ast.AnnAssign)) and stmt.value else None
            for node in ast.walk(stmt):
                if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load):
                    bound.setdefault(node.id, []).append(("value", value, "") if value else ("other", node, ""))
    return bound


def spoken(target: str) -> bool:
    """Whether a module (os) or a module's member (pathlib.Path) is in the pin proof's vocabulary."""
    module, _, member = target.rpartition(".")
    return target in VOCABULARY or member in VOCABULARY.get(module, ())


def launches(rel: str, tree: ast.Module, helper: set[int], hook: set[int]) -> list[str]:
    """Each reference of a pin-proof module to dynamic code, the helper's included, by import, alias, name or
    attribute of any object (but re.compile); outside the helper (`helper`: its nodes), each to a process-launch
    facility; outside the audit hook's installer (`hook`: its nodes), each to reflection; each wildcard import."""
    found, facility = [], {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias, name, _ in imported(node):
                dotted = alias.name if isinstance(node, ast.Import) else f"{node.module or ''}.{alias.name}"
                parts = set(dotted.split("."))
                if alias.name == "*":
                    found.append(f"{rel}:{node.lineno} imports every name of {node.module}, which the census "
                                 f"cannot follow")
                elif parts & DYNAMIC or (parts & LAUNCH_NAMES and id(node) not in helper):
                    facility[name] = dotted
                    found.append(f"{rel}:{node.lineno} imports {dotted}" + (f" as {name}" if alias.asname else "") +
                                 f", {'a process-launch facility' if parts & LAUNCH_NAMES else 'dynamic code'}")
        elif isinstance(node, ast.Name) and node.id in DYNAMIC:
            found.append(f"{rel}:{node.lineno} names {node.id}, dynamic code or reflection")
        elif isinstance(node, ast.Name) and node.id in facility and isinstance(node.ctx, ast.Load):
            found.append(f"{rel}:{node.lineno} names {node.id}, which is {facility[node.id]}")
        elif isinstance(node, ast.Attribute) and node.attr in DYNAMIC and ast.unparse(node) != "re.compile":
            found.append(f"{rel}:{node.lineno} names {ast.unparse(node)}, dynamic code or reflection")
        elif isinstance(node, ast.Attribute) and node.attr in LAUNCH_NAMES and id(node) not in helper:
            found.append(f"{rel}:{node.lineno} names {ast.unparse(node)}, a process-launch facility")
        elif isinstance(node, ast.Attribute) and REFLECTIVE.match(node.attr) and id(node) not in hook:
            found.append(f"{rel}:{node.lineno} names {ast.unparse(node)}, reflection that reaches an object "
                         f"without naming it")
    return found


def reach(rel: str, tree: ast.Module) -> list[str]:
    """Each name the pin decision (ROOTS, and every function, class and constant of ctrl_build.py they name,
    followed through each) uses outside the proof's vocabulary, at the line that names it."""
    bound = scope(tree)
    judged: dict[int, str | None] = {}

    def judge(name: str) -> str | None:
        """Why the pin decision may not name `name`, one of the module's own; None where it may."""
        for kind, node, target in bound[name]:
            if kind == "def" and name == HELPER:
                continue
            if id(node) not in judged:
                judged[id(node)] = None  # a function that names itself is judged once, by its own uses
                why = [f"{rel}:{node.lineno} binds {name} as the census cannot follow"] if kind == "other" else \
                    [] if kind != "import" or spoken(target) else \
                    [f"{rel}:{node.lineno} imports {target}, outside the pin proof's vocabulary"]
                judged[id(node)] = (why or uses(name if kind == "def" else f"the value of {name}", node, kind)
                                    or [None])[0]
            if judged[id(node)]:
                return judged[id(node)]
        return None

    def uses(owner: str, node: ast.AST, kind: str = "def") -> list[str]:
        """Each name `owner` (a function, class or value of the module) uses outside the vocabulary."""
        if kind == "import":
            return []
        nodes = list(ast.walk(node))
        local = {n.id for n in nodes if isinstance(n, ast.Name) and not isinstance(n.ctx, ast.Load)}
        local |= {n.arg for n in nodes if isinstance(n, ast.arg)}
        local |= {n.name for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                                                          ast.ExceptHandler)) and n is not node and n.name}
        found = []
        for n in nodes:
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                found += [f"{rel}:{n.lineno} {owner} imports {target}, outside the pin proof's vocabulary"
                          for _, _, target in imported(n) if not spoken(target)]
            elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id in bound:
                if why := judge(n.id):
                    found.append(f"{rel}:{n.lineno} {owner} names {n.id}, which the pin decision may not reach "
                                 f"({why})")
            elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id not in local | BUILTINS:
                found.append(f"{rel}:{n.lineno} {owner} names {n.id}, neither ctrl_build.py's nor in the pin "
                             f"proof's vocabulary")
            elif isinstance(n, ast.Attribute):
                modules = [t for k, _, t in bound.get(n.value.id, []) if k == "import"] \
                    if isinstance(n.value, ast.Name) else []
                if modules and n.attr not in VOCABULARY.get(modules[0], frozenset()):
                    found.append(f"{rel}:{n.lineno} {owner} names {ast.unparse(n)}, outside the pin proof's "
                                 f"vocabulary")
                elif not modules and n.attr not in ATTRIBUTES:
                    found.append(f"{rel}:{n.lineno} {owner} names .{n.attr}, outside the pin proof's vocabulary")
        return found

    found = []
    for root in ROOTS:
        if not any(kind == "def" for kind, _, _ in bound.get(root, [])):
            found.append(f"{rel} holds no {root}, which decides the pin")
        for kind, node, _ in bound.get(root, []):
            found += uses(root, node) if kind == "def" else [f"{rel}:{node.lineno} binds {root} again"]
    return found


def proof_run(texts: dict[str, str], stack: Path = STACK, inherited: dict[str, str] | None = None) -> tuple[int, str]:
    """The pin proof run from `texts` (each module's path and text) under its audit hook, in a fresh interpreter
    and before any build (PROOF_RUN), on `stack`, with `inherited` added to the environment it inherits: its exit
    status, and its output then its errors. That environment holds neither of the helper's two settings, so only
    the helper's own environment can give them."""
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_NO_REPLACE_OBJECTS", "GIT_GRAFT_FILE")}
    with tempfile.TemporaryDirectory(prefix="ctrl-pin-") as scratch:
        given = Path(scratch) / "texts.json"
        given.write_text(json.dumps(texts), encoding="utf-8")
        res = fw_gtest.run([sys.executable, "-I", "-B", "-c", PROOF_RUN, str(ROOT), str(given), str(stack)],
                           timeout=PROOF_RUN_TIMEOUT_S, env={**env, "LC_ALL": "C", **(inherited or {})})
    return res.returncode, res.stdout + res.stderr


def exercised(texts: dict[str, str]) -> list[str]:
    """The pin proof run from `texts` under its audit hook (proof_run): each refusal of the hook, at the line of the
    proof that asked; or, if the run did not reach the pin check's verdict, how it ended."""
    rc, out = proof_run(texts)
    refused = [ln.removeprefix(HOOK_REFUSED) for ln in out.splitlines() if ln.startswith(HOOK_REFUSED)]
    if refused or (rc == 0 and "tsn-c-stack at " in out):
        return list(dict.fromkeys(refused))
    return [f"the pin proof did not reach its verdict under its audit hook: exit {rc}: "
            f"{out.strip().splitlines()[-1] if out.strip() else 'no output'}"]


def census(texts: dict[str, str], env: dict[str, str]) -> list[str]:
    """Each way the pin proof's modules (`texts`: each one's path and text) could start a process other than
    through the helper, or run dynamic code (THE CENSUS), and each setting of the helper's environment (`env`) that
    would let git read a replacement object or a graft; then each refusal of the audit hook when the proof runs from
    the texts (exercised)."""
    findings = []
    builds = [rel for rel in texts if Path(rel).name == "ctrl_build.py"]
    if len(builds) != 1:
        findings.append(f"the census was given {len(builds)} ctrl_build.py, which holds the helper, where it needs one")
    for rel, text in texts.items():
        tree = ast.parse(text, rel)
        helper_nodes: set[int] = set()
        hook_nodes: set[int] = set()
        if rel in builds:
            bound = scope(tree)
            helper = bound.get(HELPER, [])
            defs = [node for kind, node, _ in helper if kind == "def"]
            if not defs:
                findings.append(f"{rel} holds no helper ({HELPER})")
            findings += [f"{rel}:{node.lineno} binds the helper's name {HELPER} again" for _, node, _ in helper
                         if node is not defs[0]]
            helper_nodes = {id(n) for helper_def in defs[:1] for n in ast.walk(helper_def)}
            hooks = [node for kind, node, _ in bound.get(HOOK, []) if kind == "def"]
            hook_nodes = {id(n) for hook_def in hooks[:1] for n in ast.walk(hook_def)}
            findings += reach(rel, tree)
        findings += launches(rel, tree, helper_nodes, hook_nodes)
    if len(builds) == 1:
        findings += exercised(texts)
    if env.get("GIT_NO_REPLACE_OBJECTS") != "1":
        findings.append("the pin proof's Git environment does not set GIT_NO_REPLACE_OBJECTS=1, so Git would read "
                        "a replacement object")
    graft = env.get("GIT_GRAFT_FILE")
    if not graft or Path(graft).exists(follow_symlinks=False):
        findings.append(f"the pin proof's Git environment gives GIT_GRAFT_FILE {graft or 'no value'}, so Git would "
                        f"read a graft file")
    return list(dict.fromkeys(findings))


def proof_census() -> list[str]:
    """The census of the pin proof as the checkout holds it, with the helper's own environment."""
    return census({p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}, git_env())


def make(makefile: Path, *args: str, timeout: int | None = None, env: dict[str, str] | None = None) -> tuple[int, str]:
    """make on one Makefile, in its directory."""
    return run(["make", "--no-print-directory", "-C", str(makefile.parent), "-f", makefile.name, *args],
               env=env, timeout=timeout)


def targets(makefile: Path, overrides: list[str], env: dict[str, str] | None = None) -> dict[str, frozenset[str]]:
    """Every target the Makefile defines, special and pattern ones aside, with all its prerequisites (normal
    and order-only), from make's own database."""
    _, out = make(makefile, "-p", "-n", "-q", "-R", *overrides, NO_GOAL, env=env)
    files = out.partition("\n# Files\n")[2].partition("\n# files hash-table stats")[0]
    if not files:
        raise Refusal(f"make printed no database for {makefile.relative_to(ROOT)}")
    found = {}
    for entry in files.split("\n\n"):
        lines = [ln for ln in entry.splitlines() if ln]
        rule = next((ln for ln in lines if not ln.startswith(("#", "\t"))), None)
        if rule is None or any(ln.startswith("# Not a target") for ln in lines):
            continue
        name, sep, rest = rule.partition(":")
        if sep and not name.startswith(".") and "%" not in name:
            found[name.strip()] = frozenset(rest.lstrip(":").replace("|", " ").split())
    return found


def recipes(makefile: Path, target: str, overrides: list[str],
            env: dict[str, str] | None = None) -> dict[str, list[str]]:
    """Each target make's dry run of `target` would build (it and its prerequisites, every one remade), with the
    command lines of its own recipe."""
    _, out = make(makefile, "-n", "-B", "--trace", *overrides, target, env=env)
    own: dict[str, list[str]] = {}
    current = None
    for line in out.splitlines():
        if m := TRACE.match(line):
            current = m[1]
            own.setdefault(current, [])
        elif current is not None:
            own[current].append(line)
    return own


def stack_targets(makefile: Path, stack: Path) -> tuple[list[str], list[str], list[str]]:
    """The Makefile's targets whose build reaches `stack` (STACK_DIR), those that run the pin check, and the
    findings: each target whose own recipe names the stack without one that runs the pin check among its
    prerequisites, and each that names the checkout's stack instead."""
    overrides = [f"STACK_DIR={stack}"]
    defined = targets(makefile, overrides)
    built = {name: recipes(makefile, name, overrides) for name in defined}
    pins = {t for own in built.values() for t, lines in own.items() if any(PIN_RUN in ln for ln in lines)}
    where = makefile.relative_to(ROOT).as_posix() if makefile.is_relative_to(ROOT) else makefile.name
    reaching, findings = [], {}
    for name, own in built.items():
        if any(str(stack) in ln for lines in own.values() for ln in lines):
            reaching.append(name)
        for target, lines in own.items():
            if target in pins:
                continue
            if any(CHECKOUT_STACK in ln for ln in lines):
                findings[f"{where}: {target} builds the checkout's tsn-c-stack, not the STACK_DIR it is given"] = None
            elif any(str(stack) in ln for ln in lines) and not defined.get(target, frozenset()) & pins:
                findings[f"{where}: {target} builds against tsn-c-stack without the pin check "
                         f"({', '.join(sorted(pins)) or 'none'}) as a prerequisite"] = None
    return reaching, sorted(pins), list(findings)


def named_compilers(makefile: Path, env: dict[str, str]) -> list[dict]:
    """Each compiler a Makefile's recipes run by a path no capture wrapper stands on (`env`'s CTRL_CAPTURE_BIN),
    read from make's own dry run of every target under the capture's environment: a bypass record of each, as
    the capture's audit hook writes one for a Python builder."""
    wrappers = Path(env["CTRL_CAPTURE_BIN"]).resolve()
    where = makefile.relative_to(ROOT).as_posix() if makefile.is_relative_to(ROOT) else makefile.name
    found = {}
    for target in targets(makefile, [], env):
        for own, lines in recipes(makefile, target, [], env).items():
            for line in lines:
                for word in re.split(r"[\s;&|()`]+", line):
                    word = word.strip("'\"")
                    if "/" in word and COMPILER.match(word.rpartition("/")[2]) and \
                            (makefile.parent / word).resolve().parent != wrappers:
                        found[(word, line)] = {"bypass": word, "args": [line], "cwd": str(makefile.parent),
                                               "from": [f"{where} (target {own})"]}
    return list(found.values())


def makefile_findings(makefiles: list[Path], work: Path) -> list[str]:
    """Every Makefile builder's targets that build the stack take the pin check first: judged with STACK_DIR a
    link to the submodule, so a recipe naming the submodule itself is told apart."""
    link = work / "tsn-c-stack-link"
    work.mkdir(parents=True, exist_ok=True)
    if not link.is_symlink():
        link.symlink_to(STACK, target_is_directory=True)
    findings = [f for makefile in makefiles for f in stack_targets(makefile, link)[2]]
    for makefile in makefiles:
        if makefile.parent.name == "milan_dp":
            defined = targets(makefile, [])
            findings += [f"{target} lacks its required stack-pin prerequisite"
                         for target in COUNTER_TARGETS if "stack-pin" not in defined.get(target, frozenset())]
    return findings


def mirror(directory: Path, into: Path) -> Path:
    """A scratch checkout for one directory of it: the directory's files copied (tracked, or new and not
    ignored), every other entry of the checkout linked, so its relative paths reach what they reach in the
    checkout and what it writes stays in the copy."""
    if into.exists():
        shutil.rmtree(into)
    here, there = ROOT, into
    for part in directory.relative_to(ROOT).parts:
        there.mkdir(parents=True, exist_ok=True)
        for entry in here.iterdir():
            if entry.name != part:
                (there / entry.name).symlink_to(entry)
        here, there = here / part, there / part
    listed = git(directory, "ls-files", "-z", "--cached", "--others", "--exclude-standard", ".")
    if listed.returncode:
        raise Refusal(f"cannot list {directory.relative_to(ROOT)}: {listed.stderr.strip()}")
    for name in filter(None, listed.stdout.split("\0")):
        if (directory / name).is_file():
            (there / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(directory / name, there / name)
    return there


def vanished(_function: object, _path: str, error: tuple) -> None:
    """Only a file vanishing during scratch removal is harmless; every other error propagates."""
    if not isinstance(error[1], FileNotFoundError):
        raise error[1]


@dataclass(frozen=True)
class Clone:
    """The scratch clone of the stack each pin control spoils (`path`, under `work`), at the gitlink `pin`."""

    work: Path
    pin: str

    @property
    def path(self) -> Path:
        """The clone's checkout."""
        return self.work / "pin-clone"

    def fresh(self) -> None:
        """A new clone of the stack at its gitlink, for the next control."""
        if self.path.exists():
            shutil.rmtree(self.path, onerror=vanished)
        create(self.path, STACK)
        self.answer("-c", "advice.detachedHead=false", "checkout", "--quiet", self.pin)

    def answer(self, *args: str, stdin: str | None = None) -> str:
        """What a command of the clone's repository prints; a failure refuses the control's setup."""
        res = git(self.path, *args, stdin=stdin)
        if res.returncode:
            raise Refusal(f"a pin control's setup failed ({' '.join(args[:2])}): {res.stderr.strip()}")
        return res.stdout

    def append(self, rel: str) -> None:
        """One line added to a file of the clone."""
        (self.path / rel).write_text((self.path / rel).read_text(encoding="utf-8") + "\n", encoding="utf-8")

    def hidden(self) -> None:
        """A source edited and hidden from the index's comparison by its assume-unchanged flag."""
        self.append("src/adp.c")
        self.answer("update-index", "--assume-unchanged", "src/adp.c")

    def linked(self) -> None:
        """A source replaced by a symbolic link to a copy of its own bytes outside the clone."""
        copy = self.work / "adp.c"
        shutil.copyfile(self.path / "src/adp.c", copy)
        (self.path / "src/adp.c").unlink()
        (self.path / "src/adp.c").symlink_to(copy)

    def executable(self) -> None:
        """A script made executable, its bytes unchanged."""
        script = self.path / "scripts/check_boundary.py"
        script.chmod(script.stat().st_mode | stat.S_IXUSR)

    def remade(self, tree: str, name: str, oid: str) -> str:
        """A tree written into the clone's objects: `tree` with its entry `name` holding `oid` instead."""
        entries = []
        for entry in filter(None, self.answer("ls-tree", "-z", tree).split("\0")):
            meta, entry_name = entry.split("\t", 1)
            mode, kind, _ = meta.split()
            entries.append(f"{mode} {kind} {oid}\t{name}" if entry_name == name else entry)
        return self.answer("mktree", "-z", stdin="\0".join(entries) + "\0").strip()

    def substitutes(self) -> tuple[str, str, str]:
        """src/adp.c edited on disk, and the trees that would make the pinned commit hold the edit written into the
        clone's objects: the pinned src/ tree, its substitute, and the substitute of the pinned commit's tree."""
        self.append("src/adp.c")
        blob = self.answer("hash-object", "-w", "--no-filters", "src/adp.c").strip()
        src = self.answer("rev-parse", f"{self.pin}:src").strip()
        new_src = self.remade(src, "adp.c", blob)
        return src, new_src, self.remade(self.answer("rev-parse", f"{self.pin}^{{tree}}").strip(), "src", new_src)

    def replaced_tree(self) -> None:
        """The edit on disk, and the pinned src/ tree replaced by the one holding it (refs/replace)."""
        src, new_src, _ = self.substitutes()
        self.answer("replace", src, new_src)

    def replaced_commit(self) -> None:
        """The edit on disk, and the pinned commit replaced by a copy of it whose tree holds the edit; HEAD still
        names the pin."""
        _, _, new_root = self.substitutes()
        commit = self.answer("cat-file", "commit", self.pin)
        old_root = self.answer("rev-parse", f"{self.pin}^{{tree}}").strip()
        if not commit.startswith(f"tree {old_root}\n"):
            raise Refusal(f"the pinned commit {self.pin[:8]} does not begin with its tree")
        copy = self.answer("hash-object", "-t", "commit", "-w", "--stdin",
                           stdin=commit.replace(old_root, new_root, 1)).strip()
        self.answer("replace", self.pin, copy)

    def grafted(self) -> None:
        """A source edited, and a graft file in the clone's repository that makes the pinned commit a root."""
        self.append("src/adp.c")
        (self.path / ".git/info/grafts").write_text(f"{self.pin}\n", encoding="utf-8")

    def filtered(self) -> None:
        """A source edited, and a clean filter given it through the clone's attributes that cuts the edit off, so
        a hash through the filter is the pinned blob (checked here, or the control would prove nothing)."""
        size = (self.path / "src/adp.c").stat().st_size
        self.append("src/adp.c")
        self.answer("config", "filter.pin-control.clean", f"head -c {size}")
        (self.path / ".git/info/attributes").write_text("src/adp.c filter=pin-control\n", encoding="utf-8")
        if self.answer("hash-object", "src/adp.c").strip() != self.answer("rev-parse", f"{self.pin}:src/adp.c").strip():
            raise Refusal("the pin control's clean filter does not turn its edit back into the pinned blob")

    def direct(self) -> tuple[bool, str]:
        """The pin check itself on the clone: accepted, and what it said."""
        try:
            return True, f"accepted {stack_pin(self.path, self.pin)}"
        except Refusal as exc:
            return False, str(exc)


def unplanted() -> tuple[bool, str]:
    """The pin proof as the checkout holds it, run under its audit hook (exercised): accepted when it reaches its
    verdict with no refusal, and what it ended with."""
    found = exercised({p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF})
    return not found, "; ".join(found) or "the pin check's verdict, no refusal"


def planted(rel: str, old: str | None, new: str, word: str, at_plant: bool) -> tuple[bool, str]:
    """The pin proof run under its audit hook (exercised) with `new` in place of `old` in one of its modules (`rel`,
    its name; `old` None: `new` added at its end): accepted unless a refusal of the hook holds `word` and, if
    `at_plant`, names a line of `new`; and that refusal."""
    texts = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}
    key = (HERE / rel).relative_to(ROOT).as_posix()
    text = texts[key]
    if old is not None and text.count(old) != 1:
        return True, f"the hook control's anchor occurs {text.count(old)} times in {rel}"
    at = len(text) if old is None else text.index(old)
    first = text[:at].count("\n") + 1
    last = first + new.count("\n")
    lines = [f"{key}:{n} " for n in range(first, last + 1)] if at_plant else [""]
    texts[key] = text[:at] + new + text[at + len(old or ""):]
    found = exercised(texts)
    named = [f for f in found if word in f and any(f.startswith(line) for line in lines)]
    where = f" at {key}:{first} to {last}" if at_plant else ""
    return not named, named[0] if named else f"no refusal{where} that holds {word}: {found}"


def census_arms() -> list[tuple]:
    """The pin proof's standing controls under its audit hook, each run before any build: each plant of HOOK_PLANTS
    ends in the hook's refusal, by its words, at a line of the plant (or, for the helper's own, anywhere)."""
    return [(f"the audit hook, {what}", lambda: None,
             lambda r=rel, o=old, n=new, w=word, a=at_plant: planted(r, o, n, w, a), word)
            for what, rel, old, new, word, at_plant in HOOK_PLANTS]


def pin_controls(work: Path, makefiles: list[Path]) -> tuple[int, int]:
    """The shared pin check passes a clone of the stack at its gitlink and refuses, by name, the clone with a
    source, a test, a script, a CMake file or a file no gate builds edited, with an edit the index hides, with a
    header the gitlink's tree does not hold, with a symbolic link standing in for a file, with a file made
    executable, and at another revision; and, by the edited source's name, the clone whose src/ tree or whose
    pinned commit is replaced by one holding the edit, and the clone with a graft file beside the edit; and, by the
    filter's key, the clone whose attributes give the edited source a clean filter that turns it back into the
    pinned bytes. The pin proof runs to its verdict under its audit hook, and ends in the hook's refusal with each
    plant of HOOK_PLANTS. The controls of the inherited environment (ctrl_pin_env.py), and of the object store and
    the repositories' own configuration (ctrl_pin_store.py), hold.
    The MAAP differential (both modes) and the AECP lane's arms, campaign and wire comparison refuse an edited
    clone before building it; every Makefile builder's target that reaches the stack refuses a poisoned one on
    the pin check.
    Returns the misbehaving count and the number of controls."""
    pin = stack_gitlink()
    clone = Clone(work, pin)
    edited = f"differs from the pinned {pin[:8]}: "

    def tool(argv: list[str], env: dict[str, str] | None = None) -> tuple[bool, str]:
        """A gate run on the clone: accepted (exit 0), and its last line about the stack."""
        rc, out = run(argv, env=env)
        said = [ln for ln in out.splitlines() if "tsn-c-stack" in ln]
        return rc == 0, f"exit {rc}: {said[-1].strip() if said else 'no pin verdict'}"

    def differential(*extra: str) -> tuple[bool, str]:
        """The MAAP differential on the clone, with a simulator that always fails."""
        return tool([sys.executable, "-B", str(HERE / "maap_differential.py"), "--stack", str(clone.path), *extra],
                    {"VERILATOR": "false"})

    def aecp(script: str, *extra: str) -> tuple[bool, str]:
        """One of the AECP lane's tools on the clone, with a simulator that always fails."""
        return tool([sys.executable, "-B", str(HERE / script), "--stack", str(clone.path), "--output",
                     str(work / "aecp-out"), *extra], {"VERILATOR": "false"})

    arms = [("the pinned clone, unmodified", lambda: None, clone.direct, ""),
            ("a core source edited", lambda: clone.append("src/adp.c"), clone.direct, edited + "src/adp.c"),
            ("a core test edited", lambda: clone.append("tests/test_adp.cpp"), clone.direct,
             edited + "tests/test_adp.cpp"),
            ("a stack script edited", lambda: clone.append("scripts/check_boundary.py"), clone.direct,
             edited + "scripts/check_boundary.py"),
            ("a CMake file edited", lambda: clone.append("CMakeLists.txt"), clone.direct, edited + "CMakeLists.txt"),
            ("a file no gate builds edited", lambda: clone.append("LICENSE"), clone.direct, edited + "LICENSE"),
            ("an edit the index hides (assume-unchanged)", clone.hidden, clone.direct, edited + "src/adp.c"),
            ("a header the pinned tree does not hold", lambda: (clone.path / "include/stdint.h").write_text(""),
             clone.direct, edited + "include/stdint.h"),
            ("a symbolic link standing in for a source, to its own bytes", clone.linked, clone.direct,
             edited + "src/adp.c"),
            ("a script made executable (a mode change)", clone.executable, clone.direct,
             edited + "scripts/check_boundary.py"),
            ("another revision checked out", lambda: clone.answer("checkout", "--quiet", "HEAD~1"), clone.direct,
             "is not the pinned"),
            ("a source edited, the pinned src/ tree replaced by one holding the edit", clone.replaced_tree,
             clone.direct, edited + "src/adp.c"),
            ("a source edited, the pinned commit replaced by one holding the edit", clone.replaced_commit,
             clone.direct, edited + "src/adp.c"),
            ("a source edited beside a graft file", clone.grafted, clone.direct, edited + "src/adp.c"),
            ("a source edited, a clean filter given through attributes turning it back into the pinned blob",
             clone.filtered, clone.direct, UNLISTED + "filter.pin-control.clean (local)"),
            ("the pin proof as the checkout holds it, under its audit hook", lambda: None, unplanted, ""),
            *census_arms(),
            ("the MAAP differential, a core source edited", lambda: clone.append("src/maap.c"), differential,
             edited + "src/maap.c"),
            ("the MAAP differential's self-test, a core source edited", lambda: clone.append("src/maap.c"),
             lambda: differential("--self-test"), edited + "src/maap.c"),
            ("the AECP arms, a core source edited", lambda: clone.append("src/acmp.c"),
             lambda: aecp("aecp_arms.py", "--app"), edited + "src/acmp.c"),
            ("the AECP campaign, a core source edited", lambda: clone.append("src/acmp.c"),
             lambda: aecp("aecp_mutants.py", "--shard", "0", "1000"), edited + "src/acmp.c"),
            ("the AECP wire comparison, the stack's wire layer edited", lambda: clone.append("include/wire.h"),
             lambda: aecp("aecp_wire.py", "--reference", str(PP), "--verilator", "false"), edited + "include/wire.h")]
    texts = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}
    arms += inherited_arms(clone.path, pin, work, lambda stack, env: proof_run(texts, stack, env))
    arms += store_arms(clone.path, pin, work, edited)
    for shape, extra in (("1", ()), ("8", ()), ("1", ("--build-only",))):
        arms.append((f"the F5 gap check shape {shape} {extra}, the stack's wire layer edited",
                     lambda: clone.append("include/wire.h"),
                     lambda s=shape, e=extra: tool([sys.executable, "-B",
                         str(ROOT / "tb/verilator/milan_dp/stream_counter_f5.py"),
                         "--stack", str(clone.path), "--shape", s, *e]), edited + "include/wire.h"))
    arms.append(("the F5 gap check, another revision checked out",
                 lambda: clone.answer("checkout", "--quiet", "HEAD~1"),
                 lambda: tool([sys.executable, "-B", str(ROOT / "tb/verilator/milan_dp/stream_counter_f5.py"),
                               "--stack", str(clone.path)]), "is not the pinned"))
    clone.fresh()
    arms += bench_arms(makefiles, clone.path, work, edited)
    bad = 0
    for what, spoil, check, needle in arms:
        clone.fresh()
        spoil()
        accepted, detail = check()
        ok = accepted if not needle else (not accepted and needle in detail)
        print(f"[{'ok' if ok else 'ESCAPED'}] tsn-c-stack pin control, {what}: {detail}", flush=True)
        bad += not ok
    lifecycle_bad, lifecycle_count = lifecycle_controls(clone)
    bad += lifecycle_bad
    for scratch in (clone.path, *(work / d for d in ("aecp-out", "bench", "unpinned", "inherited", "store"))):
        shutil.rmtree(scratch, ignore_errors=True)
    (work / "adp.c").unlink(missing_ok=True)
    return bad, len(arms) + lifecycle_count
