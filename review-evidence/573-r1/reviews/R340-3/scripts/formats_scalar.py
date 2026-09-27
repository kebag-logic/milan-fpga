"""A non-list formats scalar (unquoted YAML int) at one tree: named refusal or crash.
Usage: python3 formats_scalar.py <tree root>"""
import sys, tempfile, yaml
from pathlib import Path
root=Path(sys.argv[1]); sys.path.insert(0,str(root/"sw/builder")); import endstation_builder as eb
raw=yaml.safe_load((root/"configs/endstation_arty_4x4.yaml").read_text())
raw["streams"]["talkers"][0]["formats"]="SLOT"; t=yaml.safe_dump(raw)
for s in ("0x0205022000806000",):
    p=Path(tempfile.mkdtemp())/"c.yaml"; p.write_text(t.replace("SLOT",s))
    try: eb.load_config(p); print("accepted")
    except eb.ConfigError as e: print("ConfigError",e)
    except Exception as e: print("crash",type(e).__name__,e)
