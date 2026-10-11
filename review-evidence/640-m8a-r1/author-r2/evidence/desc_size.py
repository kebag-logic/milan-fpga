"""Size of the fabric's aem_desc.bin per shape, through milan_soc.build_desc_image's own calls."""
import json, sys, zlib
from pathlib import Path
R = Path(sys.argv[1])
sys.path.insert(0, str(R / "avdecc"))
sys.path.insert(0, str(R / "protocol-processor" / "hdl" / "aecp" / "desc"))
import gen_aem_store as _aem
import gen_desc_image as _img
import gen_aemi_image as _join
for ov in sys.argv[2:]:
    ovl = json.load(open(ov, encoding="utf-8"))
    model = _aem.build_model(_aem.spec_from_overlay(ovl))
    blob, report = _img.build(_join.model_to_document(model, _join.identity_from_overlay(ovl)), 576)
    print(ov.split("/")[-2], len(blob), f"{zlib.crc32(blob):08x}")
