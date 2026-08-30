#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The tracked tree is bare-metal only: zero retired-stack references (#259).

WHY THIS EXISTS. #259 (USER directive 2026-08-25) removes the retired host
software stack from the product AND from the tracked checkout: no kernel,
rootfs, Buildroot, OpenSBI, device-tree boot, ALSA host plane, linuxptp
daemon, or host-service path may appear in first-party sources, docs,
generated artifacts or test fixtures. Git history keeps the story; the
checkout does not. This gate REPLACES the transitional
check_baremetal_scope.py, whose anchored retired-history allowance #259
retires: an anchor excused prose, and #259 wants the terms gone.

INVENTORY BY DISCOVERY. The content scan set is ``git ls-files`` minus
submodule gitlinks, ``third_party/``, binary file extensions and this gate
itself (its term table and self-test fixtures must be free to name
what they refuse). Path policy runs before the binary-content exclusions.
Nothing else is excluded: docs, configs, RTL, testbenches, test suites,
generated .svg/.drawio text and archive pages are all scanned. A symlink's
stored link text is scanned without following it. Thus neither a generator,
fixture nor link target can reintroduce a term this gate cannot see. A failed
or EMPTY content inventory is rc 2, never a zero count, and an unreadable
inventory file is a finding, never a skip.

POLICY CLASSES (each finding names its class). EVERY class is judged on
every line: one line can carry two findings, because a `continue` between
them would mean a correct scrub REVEALS a new finding and the gate could
never be driven green in one pass.

T. retired-stack TERM, anywhere, any context: the appearance itself is the
   finding. Comments, prose, strings, fixture data and generated text all
   count; there is no anchor allowance. The one suppression is the
   cross-toolchain TRIPLET allowlist below (issue #259 non-goal: host-side
   development tooling is not the product target, and the RV32 cross
   compiler's triplet names its libc and the pinned sv2v release asset's
   file name names the host OS its binary runs on, not a product path).
P. protected product documentation: even an embedded ``linux`` substring is
   forbidden. Host-tooling masks never apply there. Deleting the protected
   document is also a failure, preventing removal from bypassing this class.
R. retired target RUNTIME/service surface: the former helper services and
   target-OS interfaces are forbidden even when a line avoids the broader
   class-T vocabulary. This includes exact absolute pseudo-filesystem/device
   paths; similar words such as ``/procedure`` are not matches. The one
   read-only workstation PHC probe is masked only in its exact host-tool file.
P. retired PRODUCT PATH: a tracked first-party path itself cannot retain an
   OS tree, target service, host-audio plane or retired target-driver-tree
   name while carrying clean (or binary) contents. Path scanning uses the
   same narrow host-tooling mask as content scanning, and still excludes
   submodules and ``third_party/``.
O. retired launcher option token: ``--sound-card``, ``--flashboot full``,
   ``--flashboot kernel`` (any run of spaces/tabs or ``=`` between them);
   and ``--no-fabric-gptp`` anywhere but its one code home,
   ``sw/litex/milan_soc.py`` (the verification-only door), and the
   launch-recipe gate that proves recipes never carry it.
Y. a false-like ``fabric_gptp`` value in any tracked YAML, found by PARSING
   the file
   (yaml.safe_load, falling back to the structure-only BaseLoader for a
   custom application tag, full mapping walk), so spacing and case in the
   KEY as well as the value cannot hide it and a substring is never the
   check. A tag safe_load refuses is retried, never certified clean.
S. retired sound/host-media surface: the exact parameters, ports, modules,
   configuration keys and prose phrase that once kept the target sound-card
   lane buildable are forbidden. The gPTP option-OFF exception does not
   extend to a dormant PCM capture/playback ring.
H. retired HOST-PLANE surface: exact target-driver, memory-ring, descriptor-
   tree and launch/config carriers are forbidden. Generic ``driver`` and
   ``DMA`` words remain legal because verification drivers and unrelated bus
   engines exist; the semantic names of the removed product plane do not.

``--selftest`` builds pristine scratch git trees (with the git environment
scrubbed, so a hook's GIT_DIR cannot redirect the fixtures at the real
repository) and proves: every term in the table is caught on its own; a term
planted in a generated .svg is caught (generated outputs are scanned); the
protected product document rejects embedded and host-tooling spellings;
deleting that document fails; each option token bites, including the
aligned-spaces and tab spellings; the
parsed YAML arm bites through key case, a custom tag and a self-referential
anchor; the host-tooling allowlist suppresses the WHOLE triplet family in
either case and still cannot launder a second term on the same line; the
door is exempt at its home and caught away from it; a missing/unreadable
inventory fails rather than counting zero; and the clean control stays clean.
planted in a generated .svg is caught (generated outputs are scanned); every
runtime token and exact target-OS path is caught; the exact workstation PHC
probe stays legal but cannot launder another target path; every retired
sound- and host-plane-surface token is caught; every retired product-path
class bites even with clean or binary contents, while near-miss and
host-tooling paths stay clean; each option token bites, including the
aligned-spaces and tab spellings; the parsed YAML arm bites through key case,
a custom tag and a self-referential anchor; the host-tooling allowlist
suppresses the WHOLE triplet family in either case and still cannot launder a
second term on the same line; the door is exempt at its home and caught away
from it; a missing/unreadable inventory fails rather than counting zero; and
the clean control stays clean.
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:  # the YAML class is load-bearing; refuse to run blind
    yaml = None

ROOT = pathlib.Path(__file__).resolve().parent.parent
#: Derived, never mirrored: renaming or moving this file must not silently
#: stop excluding it (its policy tables would then find this gate itself).
SELF = pathlib.Path(__file__).resolve().relative_to(ROOT).as_posix()

#: The verification-only door's one code home, plus the gate that proves
#: launch recipes never carry it.
OPTION_HOMES = ("sw/litex/milan_soc.py", "sw/builder/test_builder.py")

#: Product-facing architecture must never imply another runtime. This class
#: intentionally uses substring matching. It catches names such as vmlinux,
#: and it does not inherit host-tooling exemptions.
PRODUCT_DOCS = ("docs/overview/FULL_FPGA_SOLUTION.md",)
PRODUCT_TERM_RE = re.compile("linux", re.IGNORECASE)

#: Binary payloads: nothing greppable lives here. Generated TEXT formats
#: (.svg, .drawio) are deliberately NOT in this set.
SKIP_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".pdf",
    ".bit", ".bin", ".fbi", ".hex", ".xz", ".gz", ".zip",
    ".tar", ".7z", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".vcd",
    ".fst", ".wav", ".mp3", ".mp4", ".dcp",
}

#: Class T: the retired stack, one token per row. Word-bounded and
#: case-insensitive; the appearance is the finding.
TERMS = (
    "linux", "linuxptp", "ptp4l", "phc2sys", "rootfs", "initramfs",
    "buildroot", "opensbi", "alsa", "pipewire", "aplay", "systemd",
    "udev", "devicetree", "dtb", "dtc", "dts", "dtsi", "jffs2", "mtd",
)
# Underscore is a separator for policy tokens. A word-bound expression would
# miss spellings such as an ALSA-prefixed identifier because Python treats
# `_` as a word character.
TERM_RE = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(TERMS)
                     + r")(?![A-Za-z0-9])", re.IGNORECASE)
#: multi-word spellings the word-bound row above cannot carry
PHRASE_RE = re.compile(r"device.?tree", re.IGNORECASE)

#: Class R: target-only runtime/service names and OS surfaces which do not
#: all belong in the older stack vocabulary above. Keep the service names
#: explicit: ``statd`` catches a standalone legacy spelling, while the
#: longer spelling makes ``milan-statd`` an independently self-tested policy
#: token rather than an accidental substring consequence.
RUNTIME_TERMS = (
    "gptp2csr", "milan-statd", "statd", "kernel", "napi", "skb",
    "ethtool", "devmem", "arecord", "userspace", "user-space",
    "target shell", "target filesystem", "background service",
    "target background process", "software gPTP owner",
    "retired software owner", "retired software agents",
    "host boot profile", "host boot chain", "host boot chains",
    "software process", "shared-service", "bulk/timing service path",
    "target-side process", "software packet service",
    "secondary management socket",
    "retired software", "retired software clock-owner", "software fallback owner",
    "retired software-owner test", "software media owner",
    "software pairing race", "retired host-media", "retired host route",
    "old software", "retired CLKV", "tu lease",
    "lease was taken or lapsed", "AS_PATH software-publication",
)
RUNTIME_RE = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(re.escape(term) for term in
                       sorted(RUNTIME_TERMS, key=len, reverse=True))
    + r")(?![A-Za-z0-9])", re.IGNORECASE)

#: Class S: exact remnants of the retired target-audio lane. These are
#: semantic carriers rather than a generic ban on audio words: fabric AAF
#: receive/render, I2S/TDM and sample processing remain product functionality.
#: Every PCM ring in this tree belonged to the removed host capture/playback
#: surface, so that phrase is part of the policy too.
RETIRED_SOUND_SURFACES = (
    "SOUND_CARD_P", "sound_card", "AAF_PLAYBACK_P", "AAF_PB_STREAMS_P",
    "--pcm-ring", "--aaf-playback", "KL_pcm_tx", "KL_pcm_ring_bram",
    "m_axis_pcm", "playback_rings", "PCMRingNxN", "PCM ring", "PCM-ring",
    "pcm_ring", "sound-card",
    "host audio", "audio-host", "host PCM", "host-capture", "host capture",
    "host-playback", "host playback",
)
SOUND_SURFACE_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:" + "|".join(
        re.escape(term) for term in
        sorted(RETIRED_SOUND_SURFACES, key=len, reverse=True))
    + r")(?![A-Za-z0-9])",
    re.IGNORECASE)
TARGET_OS_PATHS = ("/proc", "/sys/class/net", "/dev/mem", "/dev/ptp")
# A pseudo-filesystem/device root is a path COMPONENT, never a prefix of a
# repository name. The delimiter lookahead admits a child slash, end of line,
# or punctuation surrounding a literal path, while refusing `/processor` and
# `scripts/processor_*`.
_PATH_COMPONENT_END = r"(?=/|$|[\s'\"`<>(){}\[\],;:.!?=#|])"
TARGET_OS_PATH_RE = re.compile(
    "(" + "|".join(re.escape(path) + _PATH_COMPONENT_END
                   for path in TARGET_OS_PATHS)
    + ")", re.IGNORECASE)
TARGET_OS_DEVICE_RE = re.compile(
    r"/dev/ptp(?:N|[0-9]+)" + _PATH_COMPONENT_END, re.IGNORECASE)

# A developer workstation may compare captured CRF to its own PHC. That
# read-only probe is #259's explicit host-tooling non-goal, not a product
# runtime. Mask only its literal PHC spellings in the one tracked tool; a
# second target path on the same line must still fail.
HOST_RUNTIME_MASKS = {
    "tb/tools/crf_vs_phc.py": re.compile(r"/dev/ptp(?:N|[0-9]+)\b",
                                         re.IGNORECASE),
}

# Class H: concrete names and phrases that carried the removed target host
# plane. These are deliberately more specific than generic ``DMA`` or
# ``driver``, which remain valid vocabulary for verification and buses. In
# particular, an upstream CPU wrapper's ``with_dma``/``with_coherent_dma``
# attribute names its dedicated memory attachment; only the removed product
# option spellings and engines below are policy carriers.
RETIRED_HOST_SURFACES = (
    "RingDMAReader", "RingDMAWriter", "RingDMA", "WishboneDMA", "RxSteer",
    "MilanDMA", "MilanDebug",
    "milan_dma_wrapper", "milan_top", "hostplane", "kl-eth", "milan-nic",
    "rx_queues", "hs_page_bytes", "--with-dma",
    "--coherent-dma", "--all-blocks", "DMA ring", "DMA-ring", "dma_ring",
    "Ring DMA", "ring-DMA", "NIC DMA", "NIC TX DMA", "network DMA",
    "Direct DMA", "packet DMA", "TX-DMA", "RX-DMA", "DMA/MAC",
    "DMA coherency", "DMA consumer",
    "DMA engine", "DMA engines", "DMA lane", "DMA lanes", "DMA path",
    "DMA paths", "DMA descriptor", "DMA descriptors", "DMA queue",
    "DMA queues", "DMA control", "AXIS-to-DMA", "AXIS to DMA",
    "AXIS→DMA", "AXIS↔DMA", "RX steering", "TX descriptor ring",
    "TX ring", "NIC queue", "NIC queues", "host queue", "host queues",
    "host plane", "host-plane", "host software", "CPU packet",
    "CPU data plane", "packet-data ABI", "packet-data boundary",
    "to/from the CPU", "stack working set",
    "software-facing media sink", "software-facing media buffer",
    "software-facing pool", "processor consumer", "target software queue",
    "packet rings", "packet data masters", "timestamp writer",
    "rx_axis_to_dma",
    "dma_tx_cdc", "dma_rx_cdc", "dma_ts_cdc", "dma_pcm_cdc",
    "dma-tx", "dma-rx", "dma-ts", "DMA-done", "simple-mode DMA",
    "strip_probes", "--strip-probes", "no_rx_rsc", "--no-rx-rsc",
    "legacy_ring", "--legacy-ring", "RX_BD", "TX_BD", "hsplit",
    "--rx-queues", "--hs-page-bytes", "header split", "header-split",
    "page pool", "page-pool", "page_pool", "BD ring", "BD-ring", "bd_ring",
    "driver ABI", "driver-ABI", "driver visible", "driver-visible",
)
HOST_SURFACE_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:" + "|".join(
        re.escape(term) for term in
        sorted(RETIRED_HOST_SURFACES, key=len, reverse=True))
    + r")(?![A-Za-z0-9])",
    re.IGNORECASE)
# These abbreviations are host offload names only in upper-case prose. Keep the
# matcher case-sensitive so ordinary short variables (for example a row-source
# count named ``rsc`` in a mapping test) do not become policy violations.
HOST_OFFLOAD_RE = re.compile(r"(?<![A-Za-z0-9])(?:RSC|TSO|GRO)(?![A-Za-z0-9])")
# Kernel network-device operation callbacks are an entire target-driver API
# family.  Gate the namespace, not only the one callback spelling found by the
# #259 audit, so renaming the retained example cannot reopen the same surface.
TARGET_DRIVER_CALLBACK_RE = re.compile(
    r"(?<![A-Za-z0-9])ndo_[a-z0-9_]+(?![A-Za-z0-9])", re.IGNORECASE)

#: Issue #259 non-goal: the host-side tooling a developer builds WITH is not
#: a product path. Three families qualify, and ONLY these three families are
#: suppressed, nothing wider:
#:   * the cross toolchain, whose TRIPLET names the toolchain's libc - the
#:     whole triplet-prefixed tool name, because the tree drives `-ld` and
#:     `-objcopy` from the same triplet as `-gcc` and one exemption cannot
#:     cover one binary and refuse its siblings;
#:   * the pinned sv2v release asset, whose file name carries the host OS the
#:     binary runs on (the CI jobs and the install recipes must be able to
#:     name the artifact they download);
#:   * the draw.io export User-Agent platform token embedded in a rendered
#:     .svg/.drawio. DOC_GENERATION.md says "edit the master, never the
#:     render", so this token is unfixable by hand and the next export
#:     re-plants it - it records which host ran the exporter, never a
#:     product path.
#: Case-insensitive, because a Makefile spells the same triplet in upper case.
#: Suppression is a MASK, not a line skip: a second, unmasked occurrence on
#: the same line still fires, which the selftest proves for all three.
ALLOWED_HOST_TOOLING = (r"riscv(?:32|64)-linux(?:-gnu)?-[a-z0-9.+_]+",
                        r"sv2v-Linux(?:\.zip)?",
                        r"\(X11; Linux [A-Za-z0-9_]+\)")
TRIPLET_RE = re.compile("|".join(ALLOWED_HOST_TOOLING), re.IGNORECASE)


def _path_term_re(terms):
    """Build a path-token matcher where '-' and '_' are separators.

    ``\b`` treats an underscore as part of a word, which would let a retired
    name hide in paths such as ``rootfs_overlay`` or ``milan_statd.service``.
    Conversely, alphanumeric embedding such as ``microkernel`` is a clean
    near-miss and must not be rejected.
    """
    alternatives = "|".join(
        re.escape(term) for term in sorted(terms, key=len, reverse=True))
    return re.compile(r"(?<![A-Za-z0-9])(" + alternatives
                      + r")(?![A-Za-z0-9])", re.IGNORECASE)


#: Class P: path names are input too. These are deliberately concrete
#: product-path families, not a generic rejection of words such as "driver"
#: anywhere in the repository (testbench drivers remain legitimate).
RETIRED_PATH_CLASSES = (
    ("target-os-tree", _path_term_re((
        "linux", "kernel", "rootfs", "initramfs", "buildroot", "opensbi",
        "devicetree", "device-tree", "device_tree", "dts", "dtsi", "dtb",
        "dtc", "jffs2", "mtd", "napi", "skb",
    ))),
    ("target-service", _path_term_re((
        "linuxptp", "ptp4l", "phc2sys", "gptp2csr", "milan-statd",
        "statd", "systemd", "udev", "ethtool", "devmem",
    ))),
    ("host-audio-plane", _path_term_re((
        "alsa", "pipewire", "aplay", "arecord",
    ))),
    ("target-driver-tree", re.compile(r"^sw/drivers?(?:/|$)",
                                      re.IGNORECASE)),
    ("target-host-plane", _path_term_re((
        "hostplane", "milan-nic", "kl-eth", "milan_dma_wrapper",
        "milan_top", "ring-dma", "ring_dma", "ring-bd", "ring_bd",
        "ring-tx", "ring_tx", "ring-writeback", "ring_writeback",
        "rx-steer", "rx_steer", "tx-bd", "tx_bd", "dma-bus",
        "dma_bus", "tx-sf", "tx_sf",
    ))),
)

#: Class O: retired option tokens. The separator run is `+`, not one
#: character: a column-aligned recipe and a tab-indented Makefile body carry
#: the same token and must not walk past the gate.
OPT_RE = re.compile(r"--sound-card\b|--flashboot[ =\t]+(?:full|kernel)\b")
DOOR_RE = re.compile(r"--no-fabric-gptp\b")


def git_env():
    """`git -C <root>` must mean the repo AT root, never an inherited one.

    Every hook, ``git rebase --exec`` and ``git bisect run`` exports GIT_DIR /
    GIT_INDEX_FILE / GIT_WORK_TREE. Inheriting them makes the selftest's
    ``git init`` a no-op and points its ``git add -A`` at the real
    repository's index.
    """
    return {k: v for k, v in os.environ.items()
            if not k.startswith(("GIT_DIR", "GIT_INDEX", "GIT_WORK_TREE",
                                 "GIT_OBJECT", "GIT_COMMON_DIR"))}


def inventory(root):
    """Return tracked first-party text files and all eligible path names."""
    try:
        # -z: NUL-separated and UNQUOTED. Without it git C-quotes any path
        # holding a non-ASCII byte ("caf\303\251.md"), the scanner then opens
        # a path that does not exist, and a file no edit can reach becomes a
        # permanent "[inventory] unreadable" finding.
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-sz"],
            capture_output=True, text=True, check=True, env=git_env())
    except (subprocess.CalledProcessError, OSError) as exc:
        raise InventoryError(f"git ls-files failed: {exc}")
    files = []
    paths = []
    for record in out.stdout.split("\0"):
        if not record:
            continue
        meta, _, path = record.partition("\t")
        mode = meta.split(None, 1)[0]
        if mode == "160000":
            continue  # submodule gitlink
        if path.startswith("third_party/") or path == SELF:
            continue
        # Path policy is evaluated before content exclusions: a binary or
        # symlink with a retired product name is still a tracked path.
        paths.append(path)
        if mode == "120000":
            files.append(path)  # stored link text is always text, whatever suffix
            continue
        if pathlib.Path(path).suffix.lower() in SKIP_EXTS:
            continue
        files.append(path)
    if not files:
        raise InventoryError("the inventory is empty: a tree with no "
                             "first-party files is a broken scan, not a "
                             "clean one")
    return files, paths


class InventoryError(RuntimeError):
    pass


def scan_path(path):
    """Reject retired product path families without reading their payload."""
    findings = []
    probe = TRIPLET_RE.sub("", path)
    for path_class, pattern in RETIRED_PATH_CLASSES:
        m = pattern.search(probe)
        if m:
            findings.append(
                f"{path}: [P] retired {path_class} path {m.group(0)!r}: "
                f"tracked first-party paths are part of the #259 surface")
    return findings


def scan_file(root, path):
    findings = []
    try:
        candidate = root / path
        # read_text follows a symlink and can leave the checkout. The tracked
        # blob is its link text, so inspect that text directly and never open
        # the destination.
        if candidate.is_symlink():
            text = os.readlink(candidate)
        else:
            text = candidate.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"{path}: [inventory] unreadable ({exc}) - an unreadable "
                f"file is a finding, never a skip"]
    for n, line in enumerate(text.splitlines(), 1):
        # Every class is judged on every line. A `continue` here would hide
        # another class hit behind the class-T hit on the same line, so a
        # correct scrub would REVEAL a new finding and the gate could never
        # be driven green in one pass.
        probe = TRIPLET_RE.sub("", line)
        m = TERM_RE.search(probe) or PHRASE_RE.search(probe)
        if m:
            findings.append(
                f"{path}:{n}: [T] retired-stack term {m.group(0)!r}: "
                f"{line.strip()[:100]!r} (#259: the checkout is bare-metal "
                f"only; history lives in git)")
        if path in PRODUCT_DOCS:
            m = PRODUCT_TERM_RE.search(line)
            if m:
                findings.append(
                    f"{path}:{n}: [P] protected product document contains "
                    f"{m.group(0)!r}: {line.strip()[:100]!r} (the full FPGA "
                    f"solution is bare-metal only)")
        runtime_probe = probe
        runtime_mask = HOST_RUNTIME_MASKS.get(path)
        if runtime_mask is not None:
            runtime_probe = runtime_mask.sub("", runtime_probe)
        m = (RUNTIME_RE.search(runtime_probe)
             or TARGET_OS_PATH_RE.search(runtime_probe)
             or TARGET_OS_DEVICE_RE.search(runtime_probe))
        if m:
            findings.append(
                f"{path}:{n}: [R] prohibited target runtime/service "
                f"surface {m.group(0)!r}: {line.strip()[:100]!r} "
                f"(#259: no target OS or retired helper-service plane)")
        m = SOUND_SURFACE_RE.search(line)
        if m:
            findings.append(
                f"{path}:{n}: [S] retired target-audio surface "
                f"{m.group(0)!r}: {line.strip()[:100]!r} "
                f"(#259: no dormant host capture/playback lane)")
        m = HOST_SURFACE_RE.search(line)
        if m is None:
            m = HOST_OFFLOAD_RE.search(line)
        if m is None:
            m = TARGET_DRIVER_CALLBACK_RE.search(line)
        if m:
            findings.append(
                f"{path}:{n}: [H] retired target host-plane surface "
                f"{m.group(0)!r}: {line.strip()[:100]!r} "
                f"(#259: no dormant target driver/memory-ring contract)")
        m = OPT_RE.search(line)
        if m:
            findings.append(
                f"{path}:{n}: [O] retired option token {m.group(0)!r}: "
                f"{line.strip()[:100]!r}")
        if DOOR_RE.search(line) and path not in OPTION_HOMES:
            findings.append(
                f"{path}:{n}: [O] --no-fabric-gptp outside its code home "
                f"({', '.join(OPTION_HOMES)}): the verification-only door "
                f"is never a recipe")
    if path.endswith((".yaml", ".yml")) and yaml is not None:
        findings += scan_yaml(root, path, text)
    return findings


#: False-like ownership values accepted by neither loader. The structure-only
#: fallback returns every scalar as text; SafeLoader may return bool/None/zero.
_FALSE_SCALARS = {"false", "no", "off", "n", "0", "~", "null"}


def _is_false(value):
    if value is False or value is None:
        return True
    if (isinstance(value, (int, float)) and not isinstance(value, bool)
            and value == 0):
        return True
    return (isinstance(value, str)
            and value.strip().lower() in _FALSE_SCALARS)


def scan_yaml(root, path, text):
    def walk(node, crumb, seen):
        # Aliases can make a genuinely cyclic container; without this guard a
        # self-referential anchor is a RecursionError no handler catches, and
        # CI reads the resulting rc as "the gate found violations".
        if isinstance(node, (dict, list)):
            if id(node) in seen:
                return []
            seen = seen | {id(node)}
        hits = []
        if isinstance(node, dict):
            for k, v in node.items():
                # The key is matched case- and space-insensitively: spelling
                # is not a hiding place, which is the whole point of parsing.
                if (str(k).strip().lower() == "fabric_gptp"
                        and _is_false(v)):
                    hits.append(f"{path}: [Y] {crumb}fabric_gptp is false "
                                f"(parsed): the fabric plane is the one "
                                f"product owner (#259)")
                hits += walk(v, f"{crumb}{k}.", seen)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                hits += walk(v, f"{crumb}[{i}].", seen)
        return hits

    try:
        docs = list(yaml.safe_load_all(text))
    except yaml.YAMLError:
        # A custom application tag is not malformed YAML - safe_load refuses
        # it, and returning [] here would CERTIFY the file clean. Retry with
        # the structure-only loader, which reads any tag.
        try:
            docs = list(yaml.load_all(text, Loader=yaml.BaseLoader))
        except yaml.YAMLError as exc:
            return [f"{path}: [Y] malformed/unscannable YAML "
                    f"({type(exc).__name__}): the ownership scan fails "
                    "closed rather than certifying an unreadable config"]
    hits = []
    for doc in docs:
        hits += walk(doc, "", frozenset())
    return hits


def check(root=ROOT):
    files, paths = inventory(root)
    findings = []
    present = set(files)
    for path in PRODUCT_DOCS:
        if path not in present:
            findings.append(
                f"{path}: [P] protected product document is missing; "
                f"deletion cannot bypass the product-runtime guard")
    for path in paths:
        findings += scan_path(path)
    for path in files:
        findings += scan_file(pathlib.Path(root), path)
    return findings, len(files)


def selftest():
    problems, arms = [], 0

    _GIT_ENV = git_env()

    def scratch_tree(build):
        d = tempfile.TemporaryDirectory(prefix="bmonly.")
        root = pathlib.Path(d.name)
        subprocess.run(["git", "-C", str(root), "init", "-q"],
                       check=True, env=_GIT_ENV)
        (root / "clean.md").write_text("The bare-metal firmware owns boot "
                                       "policy and identity.\n")
        product = root / PRODUCT_DOCS[0]
        product.parent.mkdir(parents=True)
        product.write_text("The full FPGA solution uses bare-metal firmware.\n")
        build(root)
        subprocess.run(["git", "-C", str(root), "add", "-A"],
                       check=True, env=_GIT_ENV)
        return d, root

    def arm(name, build, expect_hit, needle=None):
        nonlocal arms
        arms += 1
        findings = []
        d, root = scratch_tree(build)
        try:
            findings, _ = check(root)
        except InventoryError as exc:
            findings = [f"[inventory] {exc}"]
        finally:
            d.cleanup()
        hit = bool(findings)
        text = "\n".join(findings)
        if expect_hit and not hit:
            problems.append(f"[{name}] planted defect not caught")
        elif expect_hit and needle and needle not in text:
            problems.append(f"[{name}] caught, but not by the right class: "
                            f"wanted {needle!r} in\n{text}")
        elif not expect_hit and hit:
            problems.append(f"[{name}] clean fixture flagged:\n{text}")

    # the clean control
    arm("clean-control", lambda r: None, False)

    # T: every term in the table bites on its own, in a plain doc line
    for term in sorted(set(TERMS)):
        arm(f"term-{term}",
            lambda r, t=term: (r / "page.md").write_text(
                f"the product boots {t} at power-on\n"), True, "[T]")
    arm("term-phrase-device-tree",
        lambda r: (r / "page.md").write_text(
            "boot is described by a device tree blob\n"), True, "[T]")

    # R: every newly named runtime/service token and exact target-OS path
    # bites independently. Near-miss words and longer non-path strings stay
    # clean, so this is not an unbounded substring search.
    for term in sorted(set(RUNTIME_TERMS)):
        arm(f"runtime-{term}",
            lambda r, t=term: (r / "page.md").write_text(
                f"the retired target surface invokes {t}\n"), True, "[R]")
    for target_path in TARGET_OS_PATHS:
        arm(f"runtime-path-{target_path.strip('/').replace('/', '-')}",
            lambda r, p=target_path: (r / "page.md").write_text(
                f"the target opens {p}/status\n"), True, "[R]")
    arm("runtime-near-misses-clean",
        lambda r: (r / "page.md").write_text(
            "microkernel napiform skbuff ethtools nodevmemory arecorder "
            "upstatd gptp2csrx /procedure /sys/class/network /dev/memory\n"),
        False)
    arm("runtime-proc-prefix-clean",
        lambda r: (r / "page.md").write_text(
            "the helper lives under /processor/control\n"), False)
    arm("runtime-repository-processor-path-clean",
        lambda r: (r / "page.md").write_text(
            "see ../../scripts/processor_yosys_tops.budget\n"), False)
    arm("runtime-proc-child-caught",
        lambda r: (r / "page.md").write_text(
            "the target reads /proc/mtd\n"), True, "[R]")
    for label, punctuation in (("dot", "."), ("bang", "!"),
                               ("question", "?"), ("equals", "="),
                               ("hash", "#"), ("pipe", "|")):
        arm("runtime-path-terminal-punctuation-" + label,
            lambda r, p=punctuation: (r / "page.md").write_text(
                f"the target reads /proc{p}\n"), True, "[R]")

    def plant_host_phc(r, payload):
        target = r / "tb" / "tools" / "crf_vs_phc.py"
        target.parent.mkdir(parents=True)
        target.write_text(payload)

    arm("runtime-host-phc-tool-allowed",
        lambda r: plant_host_phc(
            r, "probe = '/dev/ptp0'  # read-only workstation input\n"),
        False)
    arm("runtime-host-phc-generic-spelling-allowed",
        lambda r: plant_host_phc(
            r, "help = 'read a workstation /dev/ptpN clock'\n"), False)
    arm("runtime-host-phc-wrong-file-caught",
        lambda r: (r / "page.md").write_text(
            "the target opens /dev/ptp0\n"), True, "[R]")
    arm("runtime-host-phc-does-not-launder",
        lambda r: plant_host_phc(
            r, "compare /dev/ptp0 after reading /proc/status\n"),
        True, "[R]")

    # S: every semantic carrier of the retired sound-card lane bites on its
    # own. Near-miss identifiers stay clean; this is not a substring policy.
    for token in RETIRED_SOUND_SURFACES:
        arm("sound-surface-" + re.sub(
                r"[^a-z0-9]+", "-", token.lower()).strip("-"),
            lambda r, t=token: (r / "page.md").write_text(
                f"retired surface carrier: {t}\n"), True, "[S]")
    arm("sound-surface-near-misses-clean",
        lambda r: (r / "page.md").write_text(
            "soundcardinality pcm ringing aaf playbacks axis pcmdata\n"),
        False)

    # H: every semantic carrier of the removed target host plane bites on its
    # own; the generic verification vocabulary deliberately stays legal.
    for token in RETIRED_HOST_SURFACES:
        arm("host-surface-" + re.sub(
                r"[^a-z0-9]+", "-", token.lower()).strip("-"),
            lambda r, t=token: (r / "page.md").write_text(
                f"retired target carrier: {t}\n"), True, "[H]")
    arm("host-surface-near-misses-clean",
        lambda r: (r / "page.md").write_text(
            "DMA verification driver topography host plan ring reader "
            "rsc tso gro cpu.with_coherent_dma = True\n"),
        False)
    for acronym in ("RSC", "TSO", "GRO"):
        arm(f"host-offload-{acronym.lower()}",
            lambda r, t=acronym: (r / "page.md").write_text(
                f"retired target offload: {t}\n"), True, "[H]")
    arm("host-driver-callback-family",
        lambda r: (r / "page.md").write_text(
            "retired target callback: ndo_open\n"), True, "[H]")

    # generated outputs are scanned: a term planted in an .svg text node
    arm("term-in-generated-svg",
        lambda r: (r / "diagram.svg").write_text(
            "<svg><text>rootfs hand-off</text></svg>\n"), True, "[T]")

    # the host-tooling allowlist suppresses ONLY the exact spellings
    arm("triplet-allowed",
        lambda r: (r / "notes.md").write_text(
            "the census drives riscv32-linux-gcc when present\n"), False)
    arm("triplet-does-not-launder",
        lambda r: (r / "notes.md").write_text(
            "riscv32-linux-gcc builds the linux image\n"), True, "[T]")
    arm("triplet-does-not-launder-runtime",
        lambda r: (r / "notes.md").write_text(
            "riscv32-linux-gcc builds the target kernel\n"), True, "[R]")
    # the exemption is the TRIPLET, so its other tools and its upper-case
    # spelling are exempt too - the tree drives -ld from the same triplet
    arm("triplet-sibling-tool-allowed",
        lambda r: (r / "make.mk").write_text(
            "\triscv32-linux-ld -r $@ -o $@\n"), False)
    arm("triplet-upper-case-allowed",
        lambda r: (r / "make.mk").write_text(
            "RISCV64-LINUX-GNU-OBJCOPY ?= objcopy\n"), False)
    arm("sv2v-asset-allowed",
        lambda r: (r / "install.sh").write_text(
            "curl -fsSL .../sv2v-Linux.zip -o /tmp/sv2v.zip\n"), False)
    arm("sv2v-asset-does-not-launder",
        lambda r: (r / "install.sh").write_text(
            "unzip sv2v-Linux.zip then boot the linux image\n"), True, "[T]")
    arm("drawio-export-agent-allowed",
        lambda r: (r / "d.svg").write_text(
            '<svg content="agent=&quot;Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit&quot;"/>\n'), False)
    arm("drawio-export-agent-does-not-launder",
        lambda r: (r / "d.svg").write_text(
            '<svg content="agent=&quot;Mozilla/5.0 (X11; Linux x86_64)&quot;">'
            '<text>rootfs</text></svg>\n'), True, "[T]")

    # P: the product page rejects embedded spellings and host-tool masks
    arm("product-doc-embedded-term",
        lambda r: (r / PRODUCT_DOCS[0]).write_text(
            "The debug artifact is vmlinux.\n"), True, "[P]")
    arm("product-doc-host-mask-disabled",
        lambda r: (r / PRODUCT_DOCS[0]).write_text(
            "Download sv2v-Linux.zip for this solution.\n"), True, "[P]")
    arm("product-doc-required",
        lambda r: (r / PRODUCT_DOCS[0]).unlink(), True, "[P]")
    # P: each retired product-path class bites even when its payload is clean.
    # Path policy runs before the binary-content exclusion, the narrow host
    # tooling spellings remain allowed, and masking one such spelling cannot
    # launder another retired path component.
    path_class_fixtures = (
        ("target-os-tree", "archive/rootfs_overlay/README.clean"),
        ("target-service", "tools/gptp2csr.service"),
        ("host-audio-plane", "configs/alsa.conf"),
        ("target-driver-tree", "sw/driver/README.clean"),
        ("target-host-plane", "tb/verilator/hostplane/fixture.clean"),
    )
    for path_class, fixture_path in path_class_fixtures:
        def plant_path(r, path=fixture_path):
            target = r / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("bare-metal fixture payload\n")
        arm(f"path-class-{path_class}", plant_path, True,
            f"[P] retired {path_class}")
    arm("path-binary-name-is-scanned",
        lambda r: (r / "board-kernel.bin").write_bytes(b"\x00\x01"),
        True, "[P]")
    arm("path-descriptor-source-is-scanned",
        lambda r: (r / "board.dtsi").write_text(
            "bare-metal fixture payload\n"), True, "[P]")
    arm("path-triplet-allowed",
        lambda r: (r / "riscv32-linux-gcc").write_text(
            "bare-metal host tool shim\n"), False)
    arm("path-sv2v-asset-allowed",
        lambda r: (r / "sv2v-Linux.zip").write_bytes(b"PK\x03\x04"), False)

    def plant_laundered_path(r):
        target = r / "riscv32-linux-gcc" / "kernel-notes.md"
        target.parent.mkdir(parents=True)
        target.write_text("bare-metal fixture payload\n")
    arm("path-host-tool-does-not-launder", plant_laundered_path, True, "[P]")

    def plant_near_miss_path(r):
        target = (r / "microkernel" / "buildrooted" / "statdaemon" /
                  "alsacean" / "driver-guide.md")
        target.parent.mkdir(parents=True)
        target.write_text("bare-metal fixture payload\n")
    arm("path-near-misses-clean", plant_near_miss_path, False)

    # O: option tokens, both spellings of the flashboot value
    arm("opt-sound-card",
        lambda r: (r / "run.sh").write_text("./soc --sound-card\n"),
        True, "[O]")
    arm("opt-flashboot-full",
        lambda r: (r / "run.sh").write_text("./soc --flashboot full\n"),
        True, "[O]")
    arm("opt-flashboot-eq-kernel",
        lambda r: (r / "run.sh").write_text("./soc --flashboot=kernel\n"),
        True, "[O]")
    # column-aligned recipes and tab-indented Makefile bodies carry the same
    # token: the separator run is not one character
    arm("opt-flashboot-aligned-spaces",
        lambda r: (r / "run.sh").write_text("./soc --flashboot   full\n"),
        True, "[O]")
    arm("opt-flashboot-tab",
        lambda r: (r / "Makefile").write_text("\t./soc --flashboot\tfull\n"),
        True, "[O]")
    arm("opt-door-outside-home",
        lambda r: (r / "recipe.sh").write_text("./soc --no-fabric-gptp\n"),
        True, "[O]")
    # ... and the door IS allowed at its one code home
    arm("opt-door-at-home",
        lambda r: (r / "sw" / "litex").mkdir(parents=True) or
        (r / "sw" / "litex" / "milan_soc.py").write_text(
            'ap.add_argument("--no-fabric-gptp", action="store_true")\n'),
        False)

    # Y: parsed YAML, spacing and case cannot hide it - in the KEY as well as
    # the value, and a custom application tag is not a certificate of health
    arm("yaml-fabric-gptp-false",
        lambda r: (r / "c.yaml").write_text(
            "board:\n  features:\n    fabric_gptp :   False\n"), True, "[Y]")
    arm("yaml-fabric-gptp-key-case",
        lambda r: (r / "c.yaml").write_text(
            "board:\n  FABRIC_GPTP: FALSE\n"), True, "[Y]")
    arm("yaml-fabric-gptp-behind-a-tag",
        lambda r: (r / "c.yaml").write_text(
            "board: !vendor/app\n  fabric_gptp: false\n"), True, "[Y]")
    arm("yaml-self-referential-anchor",
        lambda r: (r / "c.yaml").write_text(
            "&root\nfabric_gptp: false\nself: *root\n"), True, "[Y]")
    for scalar in ("0", "null", "~", "\"false\""):
        arm("yaml-fabric-gptp-false-like-" +
            re.sub(r"[^a-z0-9]+", "-", scalar.lower()).strip("-"),
            lambda r, v=scalar: (r / "c.yaml").write_text(
                f"board:\n  features:\n    fabric_gptp: {v}\n"),
            True, "[Y]")
    arm("yaml-fabric-gptp-true-clean",
        lambda r: (r / "c.yaml").write_text(
            "board:\n  features:\n    fabric_gptp: true\n"), False)
    arm("yaml-malformed-fails-closed",
        lambda r: (r / "c.yaml").write_text(
            "fabric_gptp: false\nbroken: [\n"), True, "[Y]")

    # A tracked symlink is a blob too: inspect its link text without following
    # it, including when the destination does not exist or leaves the tree.
    arm("symlink-target-term",
        lambda r: (r / "current").symlink_to("../retired/rootfs"),
        True, "[T]")
    arm("symlink-target-runtime-path",
        lambda r: (r / "current.png").symlink_to("/dev/mem"),
        True, "[R]")

    # inventory failure modes
    arms += 1
    with tempfile.TemporaryDirectory(prefix="bmonly.") as d:
        try:
            check(pathlib.Path(d))
            problems.append("[missing-inventory] a non-git directory "
                            "scanned as zero findings")
        except InventoryError:
            pass
    # root holds CAP_DAC_OVERRIDE, so mode 0 does not deny it the read and
    # this arm would report a FALSE failure in any container that does not
    # drop to a user (Containerfile.dev carries no USER directive). A loud
    # skip, never a silent pass.
    if os.geteuid() == 0:
        print("baremetal-only selftest: [unreadable-file] LOUD SKIP - running "
              "as root, where mode 0 does not deny a read", file=sys.stderr)
    else:
        arms += 1
        d, root = scratch_tree(lambda r: (r / "page.md").write_text("clean\n"))
        try:
            (root / "page.md").chmod(0)
            findings, _ = check(root)
            if not any("[inventory] unreadable" in f for f in findings):
                problems.append("[unreadable-file] an unreadable file scanned "
                                "as clean")
        finally:
            (root / "page.md").chmod(0o644)
            d.cleanup()

    return problems, arms


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if not (args.check or args.selftest):
        # a mode that is never read is a mode that cannot be got wrong loudly
        ap.error("pick a mode: --check (scan the tree) or --selftest")
    if yaml is None:
        print("baremetal-only: FATAL: pyyaml is unavailable and the parsed "
              "YAML class is load-bearing", file=sys.stderr)
        return 2
    if args.selftest:
        problems, arms = selftest()
        for p in problems:
            print("  -", p, file=sys.stderr)
        if problems:
            return 2
        print(f"baremetal-only selftest: PASS ({arms} arm(s))")
        return 0
    try:
        findings, n = check()
    except InventoryError as exc:
        print(f"baremetal-only: FATAL: {exc}", file=sys.stderr)
        return 2
    for f in findings[:40]:
        print("  -", f)
    if len(findings) > 40:
        print(f"  ... and {len(findings) - 40} more")
    if findings:
        print(f"baremetal-only: FAIL ({len(findings)} finding(s) across "
              f"{n} scanned file(s))")
        return 1
    print(f"baremetal-only: OK (0 findings across {n} tracked first-party "
          f"file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
