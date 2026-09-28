#!/usr/bin/env python3
"""sha256 of aem_desc.bin from _entity_model_image for the five shipping configs.
Usage: image_hashes.py <checkout-root>"""
import hashlib, os, sys
root = os.path.abspath(sys.argv[1]); sys.path.insert(0, os.path.join(root, "sw", "builder")); os.chdir(root)
import endstation_builder as eb, test_builder as tb
print("checker present:", hasattr(eb, "aem_image_checks"))
for name, path in tb.CONFIGS.items():
    cfg = eb.load_config(path)
    blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
    print(name, len(blob), hashlib.sha256(blob).hexdigest())
