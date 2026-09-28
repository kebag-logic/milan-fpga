"""Drive the composed milan_soc.main() for the shipping AX7101 config.

Usage (LiteX interpreter): python3 -B probe_composed_build_path.py <repository root> <work dir>

Checks, on the real main() with only Builder.build replaced by a recorder so
neither software compilation nor Vivado runs:
  positive: the #577 deployed-image check runs on the exact bytes main()
    CRC-binds and writes, before the build step; the #395 part/conditions reach
    the platform's pre-placement commands and the post-route report hook, and
    the AX7101 PLL speed grade derives from the declared part; the #582
    contract clock (recipe CPU_HZ) is the clock the PLL produces for the Milan
    domain, so the corner reports analyse the contract clock.
  negative: a planted image-check refusal stops main() before the build step
    and before aem_desc.bin is written, with the #395 hooks already installed.
"""
from pathlib import Path
import binascii
import os
import sys
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
soc_dir = root / "sw/litex"
os.chdir(soc_dir)
sys.path[:0] = [str(soc_dir), str(root / "sw/builder"), str(root)]

import endstation_builder as eb  # noqa: E402
import milan_soc  # noqa: E402
from platforms.ax7101_timing import TIMING_GRADE, configure_commands  # noqa: E402
from sw.builder import aem_image_checks  # noqa: E402
from tb.verilator.nvm_capture_cpu.recipe import CPU_HZ  # noqa: E402

cfg_path = root / "configs/endstation_ax7101_1x1_tdm8.yaml"
cfg = eb.load_config(cfg_path)
eb.build(cfg_path, root / "sw/builder/out")  # where milan_soc reads platform_shape.json
gen = root / "configs/generated" / cfg["name"]
base_argv = eb.emit_soc_argv(cfg) + ["--entity-gen-dir", str(gen)]
print("argv:", " ".join(base_argv))

real_validate = aem_image_checks.validate_shipping_image
real_pll = milan_soc.S7PLL


def run(label, planted=None):
    out = work / label
    events, clkouts, plls = [], [], []

    def validate(blob):
        events.append(("validate", binascii.crc32(blob) & 0xFFFFFFFF, len(blob)))
        if planted:
            raise aem_image_checks.ImageCheckError(planted)
        return real_validate(blob)

    def record_build(builder, *args, **kwargs):
        tc = builder.soc.platform.toolchain
        events.append(("build", kwargs.get("run", args[0] if args else None)))
        record_build.pre = [c.format(build_name="candidate") for c in tc.pre_placement_commands.resolve(None)]
        record_build.post = [c.format(build_name="candidate") for c in tc.bitstream_commands]
        record_build.device = builder.soc.platform.device
        record_build.constants = dict(builder.soc.constants)
        record_build.aem_on_disk_before_build = (Path(builder.output_dir) / "aem_desc.bin").exists()
        Path(builder.output_dir).mkdir(parents=True, exist_ok=True)  # as the real build step does

    class PLL(real_pll):
        def __init__(self, *a, **k):
            plls.append(k.get("speedgrade"))
            super().__init__(*a, **k)

        def create_clkout(self, cd, freq, *a, **k):
            clkouts.append((cd.name, freq))
            return super().create_clkout(cd, freq, *a, **k)

    argv = ["milan_soc.py", *base_argv, "--output-dir", str(out)]
    error = None
    with patch.object(sys, "argv", argv), \
            patch.object(aem_image_checks, "validate_shipping_image", validate), \
            patch.object(milan_soc.Builder, "build", record_build), \
            patch.object(milan_soc, "S7PLL", PLL):
        try:
            milan_soc.main()
        except RuntimeError as exc:
            error = str(exc)
    return out, events, clkouts, plls, error, record_build


# Positive composed path.
out, events, clkouts, plls, error, rec = run("positive")
assert error is None, error
kinds = [e[0] for e in events]
assert kinds == ["validate", "build"], events
crc, size = events[0][1], events[0][2]
image = (out / "aem_desc.bin").read_bytes()
assert (binascii.crc32(image) & 0xFFFFFFFF, len(image)) == (crc, size), "written image differs from checked bytes"
assert rec.constants.get("MILAN_AEM_IMAGE_CRC32") == crc, rec.constants.get("MILAN_AEM_IMAGE_CRC32")
assert rec.constants.get("MILAN_AEM_IMAGE_BYTES") == size
assert rec.aem_on_disk_before_build is False
print(f"positive: image checked before build, {size} bytes, CRC32 {crc:#010x} is what is bound and written")
assert rec.device == TIMING_GRADE["part"], rec.device
setup = configure_commands()
pos = [i for i, c in enumerate(rec.pre) if c in setup]
assert [rec.pre[i] for i in pos] == setup and pos == list(range(pos[0], pos[0] + len(setup))), rec.pre
assert rec.post[0] == "kl_timing_grade_reports candidate_signoff", rec.post
print("positive: pre-placement commands carry", setup)
print("positive: post-route hook first:", rec.post[0])
assert plls and plls[0] == -int(TIMING_GRADE["part"].rsplit("-", 1)[1]), plls
print("positive: PLL speed grades constructed:", plls)
print("positive: PLL outputs:", clkouts)
freqs = {name: f for name, f in clkouts}
assert CPU_HZ in freqs.values(), (CPU_HZ, clkouts)
milan = [n for n, f in clkouts if "milan" in n.lower()]
assert milan and all(freqs[n] == CPU_HZ for n in milan), (milan, clkouts, CPU_HZ)
print(f"positive: Milan clock domain(s) {milan} run at recipe CPU_HZ {CPU_HZ}")

# Negative: planted refusal from the deployed-image check.
out, events, clkouts, plls, error, rec = run("negative", planted="planted composition refusal")
assert error == "aem_desc.bin: planted composition refusal", error
assert [e[0] for e in events] == ["validate"], events
assert not (out / "aem_desc.bin").exists()
print("negative: planted image refusal raised", repr(error), "before the build step; no aem_desc.bin written")
print("COMPOSED BUILD PATH PROBE PASS")
