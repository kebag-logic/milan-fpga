"""plant_tokens.py TREE OUT : for every mutant of TREE's control-firmware campaign (ctrl_mutants.MUTANTS),
the planted file's comment-free token stream digest, as JSON {name: [path, digest, occurrences]}. The file is
read from TREE's sw/firmware/ctrl, or from its tsn-c-stack submodule for a stack-prefixed path."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
test = tree / "sw/firmware/ctrl/test"
sys.path[:0] = [str(test), str(tree / "sw/firmware/gtest")]
import ctrl_mutants  # noqa: E402
TOK = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_]\w*|\.?\d(?:[\w.]|[eEpP][+-])*|'
                 r'<<=|>>=|\.\.\.|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^!=<>]=|##|\S')
def digest(text, suffix):
    lang = "c++" if suffix in (".cpp", ".hpp") else "c"
    out = subprocess.run(["gcc", "-x", lang, "-fpreprocessed", "-dD", "-E", "-P", "-"], input=text,
                         capture_output=True, text=True, check=True).stdout
    return hashlib.sha256("\x00".join(TOK.findall(out)).encode()).hexdigest()
res = {}
prefix = getattr(ctrl_mutants, "STACK_PREFIX", None)
for m in ctrl_mutants.MUTANTS:
    if prefix and m.path.startswith(prefix):
        f = tree / "third_party/tsn-c-stack" / m.path.removeprefix(prefix)
    else:
        f = tree / "sw/firmware/ctrl" / m.path
    text = f.read_text(encoding="utf-8")
    n = text.count(m.old)
    res[m.name] = [m.path, digest(text.replace(m.old, m.new), f.suffix), n]
Path(sys.argv[2]).write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
print(len(res), "mutants")
