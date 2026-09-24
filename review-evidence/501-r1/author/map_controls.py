import importlib.util
from pathlib import Path
import sys
import tempfile
sys.path.insert(0, str(Path.cwd() / "scripts"))
from nvm_contract import Donor, Shape
from nvm_shape import build, inventory, binding_base, layout_version
from check_nvm_record_space import expected_payloads
source = Path("scripts/nvm_map_checks.py").read_text()
donor = Donor(binding_base(), layout_version())
with tempfile.TemporaryDirectory(prefix="501-map-controls.") as tmp:
    cfg = Path("configs/endstation_ax7101_8x8.yaml")
    names, dc, spi, spo = build(cfg, Path(tmp))
    shape = Shape(cfg, names, dc, spi, spo)
    recs = inventory(shape, donor.base)
    for label, old, new, reason in (
        ("uncleared", "    live.clear()", "    pass", "not cleared before restore"),
        ("no_replay", "    live.update(_restore(applied[group, port]))", "    pass", "restore lost keys"),
    ):
        assert source.count(old) == 1
        path = Path(tmp) / (label + ".py")
        path.write_text(source.replace(old, new))
        spec = importlib.util.spec_from_file_location(label, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        findings = module.check_output_maps(shape, recs, donor, expected_payloads(shape))
        assert findings and all(reason in f for f in findings), findings
        print(label, "detected:", len(findings), "cases;", findings[0])
