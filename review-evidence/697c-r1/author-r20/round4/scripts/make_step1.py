"""Build step 1's ctrl_boundary.py (C++ names and the flag refusals, no memo) from d1b22e80's and the final one
(scratch)."""
import sys
from pathlib import Path
d = Path(sys.argv[1])
base = (d / "base_boundary.py").read_text()
final = (d / "final_boundary.py").read_text()
plants_text = (d / "final_plants.py").read_text()

def block(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i)]

def swap(text, start, end, new):
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + new + text[j:]

t = base
# docstring: the language and values paragraphs as final
t = swap(t, "- Language. Every firmware unit", "- Build modes:", block(final, "- Language. Every firmware unit", "- Build modes:"))
t = swap(t, "- Values: a flag a builder computes", "- Shapes:", block(final, "- Values: a flag a builder computes", "- Shapes:"))
# imports
t = t.replace("from concurrent.futures import ThreadPoolExecutor\n",
              "from collections.abc import Callable\nfrom concurrent.futures import ThreadPoolExecutor\n")
t = t.replace("""from ctrl_configs import (DEFAULT_ENTITY, FLAG, FORCED, Read, Space, cxx_sources, derive, image_dim,  # noqa: E402
                          makefiles, mode_dims, modes, run, spaces, variants)""",
              """# modes stays importable from here: a caller judges in the modes a planted builder gives (judge's universe).
from ctrl_configs import (DEFAULT_ENTITY, FLAG, FORCED, Read, Space, cxx_sources, derive, image_dim,  # noqa: E402
                          makefiles, mode_dims, modes, run, spaces, variants)""")
# cxx_units with view and operands
t = swap(t, "def cxx_units(trees: Trees, work: Path)", "def firmware_side(",
         block(final, "def view(trees: Trees)", "def firmware_side("))
# judge: planted builders, derived inside
t = t.replace('''def judge(trees: Trees, rv32: str | None, work: Path, universe: dict[str, tuple[str, ...]] | None = None,
          computed: dict[str, str] | None = None) -> list[str]:
    """Every finding on both sides of the boundary for these trees, in every configuration and language."""
    derived = derive() if universe is None or computed is None else ({}, {})
    each = spaces(derived[0] if universe is None else universe, derived[1] if computed is None else computed)
''', '''def judge(trees: Trees, rv32: str | None, work: Path, universe: dict[str, tuple[str, ...]] | None = None,
          computed: dict[str, str] | None = None, control: Plant | None = None) -> list[str]:
    """Every finding on both sides of the boundary for these trees, in every configuration and language, as the
    builders compile them (with a `control`'s builder text replacing or adding one's), or in `universe`'s modes
    and with `computed`'s values where given."""
    planted = builder_plant(control) if control else None
    derived = derive(planted)
    each = spaces(derived[0] if universe is None else universe, derived[1] if computed is None else computed)
''')
t = t.replace('''    cxx, unfollowed = cxx_units(trees, work / "firmware-cxx")
''', '''    cxx, unfollowed = cxx_units(trees, work / "firmware-cxx", planted)
''')
# Plant and its new controls, planted(), builder_plant(), controls()
t = swap(t, "class Plant:", "#: A builder the checkout does not hold", block(plants_text, "class Plant:", "#: A builder the checkout does not hold"))
new_plants = block(plants_text, '''    Plant("a header only the MAAP differential's C++ source reaches''', '''    Plant("pass: the firmware includes a public header"''')
t = t.replace('''    Plant("pass: the firmware includes a public header"''', new_plants + '''    Plant("pass: the firmware includes a public header"''')
planted_fn = block(final, "def planted(plant: Plant, work: Path) -> Trees:", "def controls(") + "\n" + \
    plants_text[plants_text.index("def builder_plant(plant: Plant)"):].rstrip() + "\n\n\n"
t = swap(t, "def planted(plant: Plant, work: Path) -> Trees:", "def controls(", planted_fn)
t = swap(t, "def controls(rv32: str | None, work: Path) -> int:", "def configurations(", '''def controls(rv32: str | None, work: Path) -> int:
    """Every plant refused by the finding (or the refusal) it names, every pass control passing; the misbehaving
    count."""
    bad = 0
    for plant in PLANTS:
        trees = planted(plant, work / "plants")
        try:
            findings = judge(trees, rv32, work / "plants-build", control=plant)
        except Refusal as exc:
            findings = [f"REFUSED: {exc}"]
        shutil.rmtree(work / "plants-build", ignore_errors=True)
        ok = (not findings) if not plant.needle else any(plant.needle in f for f in findings)
        shown = next((f for f in findings if plant.needle and plant.needle in f), findings[0] if findings else "")
        print(f"[{'ok' if ok else 'ESCAPED'}] boundary control {plant.name}: {shown or 'passes'}", flush=True)
        bad += not ok
    shutil.rmtree(work / "plants", ignore_errors=True)
    return bad


''')
t = swap(t, "def configurations(", "def main(", block(final, "def configurations(", "def main("))
t = t.replace('''            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout", universe, computed)''',
              '''            findings = judge(Trees(CTRL, STACK), rv32, work / "checkout")''')
(d / "step1_boundary.py").write_text(t)
