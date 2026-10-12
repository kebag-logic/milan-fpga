"""Record the audit events each form raises, after the pin-proof modules are imported."""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, "$LANES/697-consume/sw/firmware/ctrl/test")
import ctrl_build  # noqa
import ctrl_pin  # noqa
print("cached:", {m: m in sys.modules for m in ("importlib", "importlib.util", "importlib.machinery", "pkgutil",
                                                  "inspect", "subprocess", "pty", "asyncio", "multiprocessing",
                                                  "concurrent.futures", "ctypes", "_posixsubprocess", "builtins")})
LAUNCH = {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "pty.spawn", "os.fork",
          "os.forkpty", "os.startfile"}
log = []
armed = [False]

class Stop(Exception):
    pass

inside = [False]
def hook(event, args):
    if not armed[0] or inside[0]:
        return
    inside[0] = True
    try:
        hook2(event, args)
    finally:
        inside[0] = False

def hook2(event, args):
    if event in ("sys._getframe",):
        return
    f = sys._getframe(2)
    where = f"{f.f_code.co_filename.rsplit('/', 1)[-1]}:{f.f_code.co_name}:{f.f_lineno}"
    if event in ("open", "marshal.loads", "os.listdir", "sys._getframemodulename", "os.scandir", "os.stat"): return
    log.append((event, where, (args[0] if event == "import" else repr(args)[:60])))
    if event in LAUNCH:
        raise Stop(event)

sys.addaudithook(hook)
import os
forms = {
    "helper git": lambda: ctrl_build.git(ctrl_build.ROOT, "--version"),
    "fw_gtest.run": lambda: ctrl_build.run(["git", "--version"]),
    "os.system": lambda: os.system("true"),
    "os.popen": lambda: os.popen("true"),
    "os.execvp": lambda: os.execvp("true", ["true"]),
    "os.spawnv": lambda: os.spawnv(os.P_WAIT, "/bin/true", ["true"]),
    "os.posix_spawn": lambda: os.posix_spawn("/bin/true", ["true"], {}),
    "os.fork": lambda: os.fork(),
    "pty.spawn": lambda: __import__("pty").spawn(["true"]),
    "asyncio": lambda: __import__("asyncio").run(__import__("asyncio").create_subprocess_exec("true")),
    "_posixsubprocess": lambda: __import__("_posixsubprocess").fork_exec(
        [b"/bin/true"], [b"/bin/true"], True, (), None, None, -1, -1, -1, -1, -1, -1, -1, -1, False, False,
        -1, None, None, None, -1, None, False) if sys.version_info < (3, 14) else None,
    "ctypes system": lambda: __import__("ctypes").CDLL(None)["system"](b"true"),
    "multiprocessing spawn": lambda: __import__("multiprocessing").get_context("spawn").Process(target=print).start(),
    "eval": lambda: eval("1"),
    "exec": lambda: exec("pass"),
    "compile": lambda: compile("pass", "<p>", "exec"),
    "__import__ os": lambda: __import__("os"),
    "import importlib": lambda: exec("import importlib") ,
    "inspect.builtins.exec": lambda: __import__("inspect").builtins.exec("pass"),
    "pkgutil.importlib": lambda: __import__("pkgutil").importlib.import_module("os"),
    "import_module new": lambda: __import__("importlib").import_module("colorsys"),
    "dataclass": lambda: __import__("dataclasses").make_dataclass("X", ["a"]),
    "namedtuple": lambda: __import__("collections").namedtuple("N", "a b"),
    "types.FunctionType": lambda: __import__("types").FunctionType(ctrl_build.git.__code__, {}),
    "code.replace": lambda: ctrl_build.git.__code__.replace(co_name="x"),
    "set __code__": lambda: setattr((lambda: 0), "__code__", (lambda: 1).__code__),
    "gc.get_referrers": lambda: __import__("gc").get_referrers(ctrl_build),
    "closure set": lambda: None,
}
for name, form in forms.items():
    log.clear()
    armed[0] = True
    try:
        form()
        result = "returned"
    except Stop as e:
        result = f"stopped at {e}"
    except BaseException as e:  # noqa
        result = f"{type(e).__name__}: {e}"[:80]
    armed[0] = False
    print(f"== {name}: {result}")
    for ev in log:
        print("   ", *ev)
