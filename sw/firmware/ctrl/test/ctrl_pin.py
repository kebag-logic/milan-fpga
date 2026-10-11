# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_pin.py - the TSN stack's pin, held at every gate that builds the stack (#697).

The pin check itself is ctrl_build.stack_pin: the submodule at its gitlink,
and its checkout the gitlink's whole tree (the same paths, types and modes,
every file hashing to the tree's blob). Every Python gate that builds the stack
calls it first. This module holds the rest, for the boundary gate
(ctrl_boundary.py).

THE CENSUS (census). The pin proof's modules are ctrl_build.py and this one.
In them only the helper, ctrl_build.git, starts a process: it runs git with
ctrl_build.git_env, which ignores replacement objects and names a graft file
that does not exist, so git reads the real objects only. The census reads the
two modules' syntax trees, not their text, so the program a call would name
does not matter. It refuses:
- outside the helper, any reference to a process-launch facility, by import,
  alias or attribute: the subprocess, pty and asyncio.subprocess modules and
  their members; os.system, os.popen, os.exec*, os.spawn*, os.posix_spawn*,
  os.fork, os.forkpty and os.startfile; asyncio's create_subprocess_exec and
  create_subprocess_shell. An attribute so named is refused on any object, so
  os reached through another module is refused too;
- eval, exec, compile, __import__, importlib and builtins; the reflection that
  reaches an object without naming it (getattr, setattr, delattr, vars,
  globals, locals, an attribute beginning with an underscore but __name__, a
  frame's attributes, sys.modules); a wildcard import;
- in what decides the pin (ROOTS: stack_gitlink, stack_pin and the command
  line's main) and every function, class and constant of ctrl_build.py they
  name, followed through each, any name outside the proof's vocabulary
  (VOCABULARY, BUILTINS, ATTRIBUTES): a few names of os, hashlib, stat,
  pathlib and argparse, and builtins and attributes of its own values, none of
  which starts a process. So the pin decision reaches no process but through
  the helper, by any route or name: ctrl_build.run, the harness's runner, is
  refused there;
- ctrl_build.py without the helper or with its name bound again, and a helper
  environment that would read a replacement or a graft.
What remains. A function of another module that starts a process is not a
facility the census knows: ctrl_build.py's build functions and run, and this
module's tool runs (run: make, and the gates the controls run), start their
processes through fw_gtest.run, outside the helper, and the census refuses
them only where the pin decision would reach them. It reads the modules as
written: code elsewhere that rebinds their names at run time, or a route of
Python's own to an object that none of the refused names opens, is not seen.

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
pinned, one beside a graft file, and one a clean filter given through the
clone's attributes turns back into the pinned bytes. The census refuses, each
at its planted line, a git command run outside the helper (by the harness's
runner, under a computed name and as a dashed program), an aliased import of
subprocess, os.system and exec of a string, and a helper environment without
either of its two settings. The MAAP differential (both its modes) and the AECP
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
import os
import re
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path

from ctrl_build import HERE, PP, ROOT, STACK, Refusal, git, git_env, stack_gitlink, stack_pin
from ctrl_capture import COMPILER
import fw_gtest

#: The pin proof's modules, in which only the helper (ctrl_build.git) starts a process.
PROOF = (HERE / "ctrl_build.py", HERE / "ctrl_pin.py")
#: The helper: the one function, of ctrl_build.py, that may name a process-launch facility.
HELPER = git.__name__
#: What decides the pin, in ctrl_build.py: these functions, and all they name, use only the proof's vocabulary.
ROOTS = ("stack_gitlink", "stack_pin", "main")
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
BUILTINS = frozenset({"Exception", "dict", "filter", "int", "len", "list", "print", "sorted", "str", "tuple",
                      "__file__"})
#: The attributes of its own values the pin proof may use: of paths, text, maps, the helper's answer, a hash, a
#: file's status and the command line's parser and arguments.
ATTRIBUTES = frozenset({"add_argument", "as_posix", "encode", "get", "hexdigest", "is_symlink", "join", "keys",
                        "lstat", "parent", "parents", "parse_args", "read_bytes", "relative_to", "resolve",
                        "returncode", "split", "st_mode", "stack_pin", "stderr", "stdout", "strip"})

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
#: How long one bench target may run against the poisoned clone before it is a failure.
BENCH_TIMEOUT_S = 900
#: The pin check's read of the pinned tree, where most census controls plant.
TREE_READ = 'tree = git(stack, "ls-tree", "-r", "-t", "-z", "--full-tree", pin)'
#: The census's standing controls: what each plants; in which pin-proof module; the anchor it replaces there
#: (None: it is added at the module's end); the planted text, whose first line the census must name; and the
#: words the finding there must hold. Each starts a process outside the helper, whatever the program it names.
CENSUS_PLANTS = (
    ("a Git command run by the harness's runner (ctrl_build.run)", "ctrl_build.py",
     'head = git(stack, "rev-parse", "HEAD")', 'head = run(["git", "-C", str(stack), "rev-parse", "HEAD"])',
     "names run"),
    ("a program named by a computed name (git.__name__)", "ctrl_build.py", TREE_READ,
     'tree = run([git.__name__, "-C", str(stack), "ls-tree", "-r", "-t", "-z", "--full-tree", pin])', "names run"),
    ("a dashed program (git-ls-tree)", "ctrl_build.py", TREE_READ,
     'tree = run(["git-ls-tree", "-r", "-t", "-z", "--full-tree", pin], cwd=stack)', "names run"),
    ("an aliased import (from subprocess import run as r)", "ctrl_build.py", TREE_READ,
     'from subprocess import run as r\n    tree = r(["git", "-C", str(stack), "ls-tree", "-r", "-t", "-z", '
     '"--full-tree", pin])', "imports subprocess.run as r"),
    ("os.system, in a line added to ctrl_pin.py", "ctrl_pin.py", None, 'LISTED = os.system("git ls-files")\n',
     "names os.system"),
    ("exec of a string", "ctrl_build.py", 'entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()',
     'exec("entry = run([\'git\', \'ls-files\', \'--stage\', \'--\', rel], cwd=root).stdout.split()")',
     "names exec"),
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


def launches(rel: str, tree: ast.Module, exempt: set[int]) -> list[str]:
    """Outside the helper (`exempt`: its nodes), each reference of a pin-proof module to a process-launch
    facility, to dynamic code or to reflection, by import, alias, name or attribute; and each wildcard import."""
    found, facility = [], {}
    for node in ast.walk(tree):
        if id(node) in exempt:
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias, name, _ in imported(node):
                dotted = alias.name if isinstance(node, ast.Import) else f"{node.module or ''}.{alias.name}"
                parts = set(dotted.split("."))
                if alias.name == "*":
                    found.append(f"{rel}:{node.lineno} imports every name of {node.module}, which the census "
                                 f"cannot follow")
                elif parts & (LAUNCH_NAMES | DYNAMIC):
                    facility[name] = dotted
                    found.append(f"{rel}:{node.lineno} imports {dotted}" + (f" as {name}" if alias.asname else "") +
                                 f", {'a process-launch facility' if parts & LAUNCH_NAMES else 'dynamic code'}")
        elif isinstance(node, ast.Name) and node.id in DYNAMIC:
            found.append(f"{rel}:{node.lineno} names {node.id}, dynamic code or reflection")
        elif isinstance(node, ast.Name) and node.id in facility and isinstance(node.ctx, ast.Load):
            found.append(f"{rel}:{node.lineno} names {node.id}, which is {facility[node.id]}")
        elif isinstance(node, ast.Attribute) and node.attr in LAUNCH_NAMES:
            found.append(f"{rel}:{node.lineno} names {ast.unparse(node)}, a process-launch facility")
        elif isinstance(node, ast.Attribute) and REFLECTIVE.match(node.attr):
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


def census(texts: dict[str, str], env: dict[str, str]) -> list[str]:
    """Each way the pin proof's modules (`texts`: each one's path and text) could start a process other than
    through the helper (THE CENSUS), and each setting of the helper's environment (`env`) that would let git read
    a replacement object or a graft."""
    findings = []
    builds = [rel for rel in texts if Path(rel).name == "ctrl_build.py"]
    if len(builds) != 1:
        findings.append(f"the census was given {len(builds)} ctrl_build.py, which holds the helper, where it needs one")
    for rel, text in texts.items():
        tree = ast.parse(text, rel)
        exempt: set[int] = set()
        if rel in builds:
            helper = scope(tree).get(HELPER, [])
            defs = [node for kind, node, _ in helper if kind == "def"]
            if not defs:
                findings.append(f"{rel} holds no helper ({HELPER})")
            findings += [f"{rel}:{node.lineno} binds the helper's name {HELPER} again" for _, node, _ in helper
                         if node is not defs[0]]
            exempt = {id(n) for helper_def in defs[:1] for n in ast.walk(helper_def)}
            findings += reach(rel, tree)
        findings += launches(rel, tree, exempt)
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
    return [f for makefile in makefiles for f in stack_targets(makefile, link)[2]]


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


def bench_arms(makefiles: list[Path], clone: Path, work: Path, edited: str) -> list[tuple]:
    """For every target of every Makefile builder that reaches the stack in its dry run: run it in a scratch
    copy of its directory against the clone with wire.h poisoned, with no simulator; it must refuse on the pin
    check and never reach the poisoned header; each target that runs the pin check passes the clone
    unpoisoned. And the planted Makefile without the pin prerequisite."""
    simulator = work / "no_simulator.py"
    simulator.write_text(NO_SIMULATOR, encoding="utf-8")

    def poison() -> None:
        """The clone's wire.h, which every firmware build reads, ends in an #error."""
        wire = clone / "include/wire.h"
        wire.write_text(wire.read_text(encoding="utf-8") + f"\n{POISON}\n", encoding="utf-8")

    def bench(makefile: Path, target: str) -> tuple[bool, str]:
        """The target run for real in a fresh scratch copy: accepted, and its verdict on the stack."""
        copy = mirror(makefile.parent, work / "bench") / makefile.name
        rc, out = make(copy, f"STACK_DIR={clone}", f"VERILATOR={sys.executable} -I {simulator}", target,
                       timeout=BENCH_TIMEOUT_S)
        said = [ln for ln in out.splitlines() if "tsn-c-stack" in ln or "PIN-POISON" in ln]
        if "PIN-POISON" in out:
            return True, f"exit {rc}: compiled the poisoned header: {said[-1].strip()}"
        return rc == 0, f"exit {rc}: {said[-1].strip() if said else 'no pin verdict'}"

    def unpinned() -> tuple[bool, str]:
        """The planted Makefile, judged as the gate judges every Makefile builder."""
        makefile, old, new, _ = UNPINNED
        copy = mirror(makefile.parent, work / "bench") / makefile.name
        text = copy.read_text(encoding="utf-8")
        if text.count(old) != 1:
            raise Refusal(f"the planted Makefile control's anchor occurs {text.count(old)} times")
        copy.write_text(text.replace(old, new), encoding="utf-8")
        found = makefile_findings([copy], work / "unpinned")
        return not found, found[0] if found else "no finding"

    arms = []
    for makefile in makefiles:
        where = makefile.relative_to(ROOT).as_posix()
        reaching, pins, _ = stack_targets(makefile, clone)
        arms += [(f"{where} make {pin}, the pinned clone", lambda: None, lambda m=makefile, t=pin: bench(m, t), "")
                 for pin in pins]
        for target in reaching:
            arms.append((f"{where} make {target}, the stack's wire.h poisoned", poison,
                         lambda m=makefile, t=target: bench(m, t), edited + "include/wire.h"))
    arms.append((f"{UNPINNED[0].relative_to(ROOT).as_posix()} planted with {UNPINNED[3]} unpinned", lambda: None,
                 unpinned, f"{UNPINNED[3]} builds against tsn-c-stack without the pin check"))
    return arms


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
            shutil.rmtree(self.path)
        if git(self.work, "clone", "--quiet", "--no-hardlinks", str(STACK), str(self.path)).returncode or \
                git(self.path, "-c", "advice.detachedHead=false", "checkout", "--quiet", self.pin).returncode:
            raise Refusal(f"cannot clone {STACK.relative_to(ROOT)} at {self.pin} for the pin controls")

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


def counted(env: dict[str, str], name: str) -> tuple[bool, str]:
    """The census of the pin proof with a planted helper environment: accepted unless a finding names the
    setting `name`, and that finding."""
    found = census({p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}, env)
    named = [f for f in found if name in f]
    return not named, named[0] if named else f"no finding names {name}: {found}"


def planted(rel: str, old: str | None, new: str, word: str) -> tuple[bool, str]:
    """The census of the pin proof with `new` in place of `old` in one of its modules (`rel`, its name; `old`
    None: `new` added at its end): accepted unless a finding names `new`'s first line and `word`, and that
    finding."""
    texts = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in PROOF}
    key = (HERE / rel).relative_to(ROOT).as_posix()
    text = texts[key]
    if old is not None and text.count(old) != 1:
        return True, f"the census control's anchor occurs {text.count(old)} times in {rel}"
    at = len(text) if old is None else text.index(old)
    line = text[:at].count("\n") + 1
    texts[key] = text[:at] + new + text[at + len(old or ""):]
    found = census(texts, git_env())
    named = [f for f in found if f.startswith(f"{key}:{line} ") and word in f]
    return not named, named[0] if named else f"no finding at {key}:{line} that {word}: {found}"


def without(name: str) -> dict[str, str]:
    """The helper's environment without one of its settings."""
    return {k: v for k, v in git_env().items() if k != name}


def census_arms() -> list[tuple]:
    """The census's standing controls: each process start of CENSUS_PLANTS refused at its line, by what it names,
    and the helper's environment without each of its two settings refused by the setting's name."""
    arms: list[tuple] = [(f"the census, {what}", lambda: None,
                          lambda r=rel, o=old, n=new, w=word: planted(r, o, n, w), word)
                         for what, rel, old, new, word in CENSUS_PLANTS]
    return arms + [(f"the census, the helper's environment without {name}", lambda: None,
                    lambda n=name: counted(without(n), n), name)
                   for name in ("GIT_NO_REPLACE_OBJECTS", "GIT_GRAFT_FILE")]


def pin_controls(work: Path, makefiles: list[Path]) -> tuple[int, int]:
    """The shared pin check passes a clone of the stack at its gitlink and refuses, by name, the clone with a
    source, a test, a script, a CMake file or a file no gate builds edited, with an edit the index hides, with a
    header the gitlink's tree does not hold, with a symbolic link standing in for a file, with a file made
    executable, and at another revision; and, by the edited source's name, the clone whose src/ tree or whose
    pinned commit is replaced by one holding the edit, the clone with a graft file beside the edit, and the clone
    whose attributes give the edited source a clean filter that turns it back into the pinned bytes. The census
    refuses each process start of CENSUS_PLANTS at its line and a helper environment without either setting.
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
             clone.filtered, clone.direct, edited + "src/adp.c"),
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
    for scratch in (clone.path, work / "aecp-out", work / "bench", work / "unpinned"):
        shutil.rmtree(scratch, ignore_errors=True)
    (work / "adp.c").unlink(missing_ok=True)
    return bad, len(arms)
