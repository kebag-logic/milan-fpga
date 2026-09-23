import json
from pathlib import Path
SEL = [["        selections = arm_selections(firmware)\n        if selections is not None:",
        "        selections = None\n        if selections is not None:"],
       ["    for label, accepted in accepted_cases.items():\n",
        "    for label, accepted in {}.items():\n"]]
E = [["        assert_preprocessed_boot_path(firmware, source,\n                                      preprocess_take(source))\n", ""]]
H = [["            assert_include_resolution_is_pinned(\n                include_resolution_planted(listing, source))\n",
      "            pass\n"]]
R = [["        compiled_census_verdict = assert_compiled_census_is_clean(\n            source, taken=census_taken)\n",
      "        compiled_census_verdict = (assert_compiled_census_is_clean if source == firmware_source else (lambda *a, **k: {'ran': True}))(\n            source, taken=census_taken)\n"],
     ["            compiled_census_verdict[\"resolved\"] = assert_resolved_boot_flow(\n",
      "            compiled_census_verdict[\"resolved\"] = (assert_resolved_boot_flow if source == firmware_source else (lambda *a, **k: {}))(\n"]]
sets = {"sel": SEL, "e": E, "h": H, "r": R, "er": E + R}
for name, patch in sets.items():
    Path(f"patch-{name}.json").write_text(json.dumps(patch, indent=1))
L = {}
L["sel"] = ["a pasted call name in an arm the stub tree drops",
 "a spliced call name in an arm the stub tree drops",
 "a spliced call name in an arm only the product compiles",
 "a spliced call name onto a literal address in a dropped arm",
 "a struct-overlay store at the ADP_CTRL address in a dropped arm",
 "an arm only the product compiles, short-circuiting the choke point's verdict test",
 "entity enabled through a pasted call name in an arm only the product compiles, in a UART command handler",
 "entity enabled through a fifth pointer cast in an arm only the product compiles, in a UART command handler",
 "entity enabled by a lui-based inline-asm store in an arm only the product compiles, in a UART command handler",
 "AEM guard selected by a build flag",
 "pre-AEM clear behind a build flag",
 "a dropped arm inside a CSR write's argument",
 "CRC comparison itself put behind a build flag",
 "ADP_CTRL's name moved to another register by an arm only the product compiles",
 "more preprocessor arm selections than gate 1b grades"]
L["e"] = ["entity enabled through a phase-2-spliced call name",
 "entity enabled through a space phase-2 token splice",
 "entity enabled through a tab phase-2 token splice",
 "entity enabled through a form-feed phase-2 token splice",
 "entity enabled through a vertical-tab phase-2 token splice",
 "entity enabled through a pasted call name",
 "a pasted call name in an arm the stub tree drops",
 "a spliced call name in an arm the stub tree drops",
 "a spliced call name in an arm only the product compiles",
 "a spliced call name onto a literal address in a dropped arm"]
L["er"] = L["e"] + ["entity enabled through a spliced call name in a UART command handler",
 "entity enabled through a pasted call name in an arm only the product compiles, in a UART command handler"]
L["h"] = ["pinned include shadowed by a file beside the firmware",
 "the second pinned quoted include shadowed by a file beside the firmware",
 "pinned include shadowed by a LINK beside the firmware to a file outside this repository"]
L["r"] = ["entity enabled by an inline-asm store to the CSR address",
 "entity enabled by a lui-based inline-asm store",
 "entity enabled through a widened pointer cast",
 "entity enabled through a reordered pointer cast",
 "entity enabled through a pointer held in a local",
 "entity enabled through a fifth pointer cast in an arm only the product compiles, in a UART command handler",
 "entity enabled by a lui-based inline-asm store in an arm only the product compiles, in a UART command handler",
 "a struct-overlay store at the ADP_CTRL address in a dropped arm",
 "the verifier's QSPI-slot condition made false in the census stub tree"]
for name, labels in L.items():
    Path(f"labels-{name}.txt").write_text("\n".join(labels) + "\n")
print({k: len(v) for k, v in L.items()})
