#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline installer controls use a tiny fixture archive and its own digest.

These controls are not Bootlin compatibility evidence. The real archive and
gate must also run, with no replacement of the production digest.
"""

import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import ci_rv32_sdk as sdk


#: The provenance fields a receipt binds, spelled HERE rather than read back
#: from the installer, so dropping one from provenance() cannot also drop
#: the check for it (R228-F3 on PR #521).
PROVENANCE_FIELDS = {"archive_url", "archive_sha256", "release",
                     "installer_revision", "installer_sha256", "host",
                     "destination"}
FIXTURE_TOOL = ("#!/bin/sh\nset -eu\n"
                'root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"\n'
                'case "$1" in\n'
                '  --version) echo "fixture GCC 14.3.0" ;;\n'
                '  -dumpfullversion) echo 14.3.0 ;;\n'
                '  -dumpmachine) echo riscv32-buildroot-linux-gnu ;;\n'
                '  -print-sysroot) echo "$root/sysroot" ;;\n'
                '  *) exit 9 ;;\nesac\n')


def fixture_archive(root: Path, name: str, relocation: str,
                    arcname: str = sdk.RELEASE) -> Path:
    """A well-formed SDK fixture archive, with `relocation` as its script."""
    source = root / f"{name}-tree"
    (source / "bin").mkdir(parents=True)
    (source / "sysroot").mkdir()
    (source / "share/buildroot/sdk-location").parent.mkdir(parents=True)
    (source / "share/buildroot/sdk-location").write_text("/old/prefix\n")
    for tool_name in ("fixture-gcc", "fixture-gcc-twin"):
        tool = source / "bin" / tool_name
        tool.write_text(FIXTURE_TOOL)
        tool.chmod(0o755)
    (source / sdk.COMPILER).symlink_to("fixture-gcc")
    script = source / "relocate-sdk.sh"
    script.write_text(relocation)
    script.chmod(0o755)
    archive = root / f"{name}.tar.xz"
    with tarfile.open(archive, "w:xz") as stream:
        stream.add(source, arcname=arcname)
    return archive


class InstallerTests(unittest.TestCase):
    """Exercise installation, cache validation, and refusal before execution."""

    def setUp(self) -> None:
        """Construct a self-contained SDK with a real relocation step."""
        self.tmp = tempfile.TemporaryDirectory(prefix="rv32-installer-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.destination = self.root / "installed"
        self.archive = fixture_archive(
            self.root, "fixture",
            '#!/bin/sh\nset -eu\npwd > share/buildroot/sdk-location\n')
        self.addCleanup(patch.stopall)
        patch.object(sdk, "ARCHIVE_SHA256", sdk.digest(self.archive)).start()

    def serve(self, payload: bytes) -> object:
        """Stand in for the hosted download: `payload` is what arrives."""
        return patch.object(sdk.urllib.request, "urlopen",
                            side_effect=lambda *_a, **_k: io.BytesIO(payload))

    def install(self) -> None:
        """Install the checksum-verified synthetic fixture."""
        with contextlib.redirect_stdout(io.StringIO()):
            sdk.install(self.destination, self.archive)

    def read_receipt(self) -> dict[str, object]:
        """Read a receipt for a deliberate corruption control."""
        return json.loads((self.destination / sdk.RECEIPT).read_text())

    def write_receipt(self, receipt: object) -> None:
        """Plant one precise receipt defect."""
        (self.destination / sdk.RECEIPT).write_text(json.dumps(receipt))

    def refuses_without_execution(self, reason: str) -> None:
        """Cache corruption must be refused before any restored program runs."""
        with patch.object(sdk.subprocess, "run") as run:
            with self.assertRaisesRegex((ValueError, FileNotFoundError), reason):
                sdk.install(self.destination, self.archive)
            run.assert_not_called()

    def test_fresh_and_cache_hit(self) -> None:
        """Extraction relocates; a valid hit neither downloads nor extracts."""
        self.install()
        receipt = self.read_receipt()
        self.assertEqual(receipt["provenance"]["destination"], str(self.destination))
        self.assertEqual(receipt["tools"]["realpath"],
                         str(self.destination / "bin/fixture-gcc"))
        with patch.object(sdk, "extract") as extract:
            with patch.object(sdk.urllib.request, "urlopen") as download:
                with contextlib.redirect_stdout(io.StringIO()):
                    sdk.install(self.destination)
                extract.assert_not_called()
                download.assert_not_called()
        self.assertEqual(receipt, self.read_receipt())

    def test_bad_archive(self) -> None:
        """A wrong offline --archive never reaches tar or creates an installation."""
        self.archive.write_bytes(b"not the pinned archive")
        self.refuses_without_execution("archive digest mismatch")
        self.assertFalse(self.destination.exists())

    def test_download_path(self) -> None:
        """The hosted path, with no --archive, installs what the pin names."""
        with self.serve(self.archive.read_bytes()) as download:
            self.install_downloaded()
        download.assert_called_once_with(sdk.ARCHIVE_URL, timeout=120)
        self.assertTrue((self.destination / sdk.RECEIPT).is_file())

    def install_downloaded(self) -> None:
        """Install exactly as the hosted jobs do: no offline archive."""
        with contextlib.redirect_stdout(io.StringIO()):
            sdk.install(self.destination)

    def test_download_path_refuses_unpinned_bytes(self) -> None:
        """A wrong download is refused before tar reads it or anything runs.

        The hosted jobs pass no --archive, so the digest check inside
        extract() is the only authentication on their path (R228-F2 on PR
        #521). The first payload is a WELL-FORMED SDK archive with the
        pinned root: with that check gone it would extract, run its own
        relocation script, and earn a verified receipt. The last payload is
        the fixture itself under a pin one hex digit away from its digest,
        so a comparison of any prefix of the digest is refused too.
        """
        marker = self.root / "unpinned-relocation-ran"
        unpinned = fixture_archive(
            self.root, "unpinned",
            f'#!/bin/sh\nset -eu\ntouch "{marker}"\n'
            'pwd > share/buildroot/sdk-location\n')
        pinned, pin = self.archive.read_bytes(), sdk.ARCHIVE_SHA256
        near_pin = pin[:-1] + ("1" if pin[-1] == "0" else "0")
        for label, payload, expected in (
                ("well-formed but unpinned", unpinned.read_bytes(), pin),
                ("truncated", pinned[:len(pinned) // 2], pin),
                ("empty", b"", pin),
                ("pinned one hex digit away", pinned, near_pin)):
            with self.subTest(payload=label), self.serve(payload) as download, \
                    patch.object(sdk, "ARCHIVE_SHA256", expected), \
                    patch.object(sdk.tarfile, "open", wraps=sdk.tarfile.open) as tar, \
                    patch.object(sdk.subprocess, "run", wraps=sdk.subprocess.run) as run:
                with self.assertRaisesRegex(ValueError, "archive digest mismatch"):
                    self.install_downloaded()
                download.assert_called_once()
                tar.assert_not_called()
                run.assert_not_called()
                self.assertFalse(self.destination.exists())
                self.assertFalse(marker.exists())

    def test_bad_archive_with_cache(self) -> None:
        """Explicit offline inputs are checked even beside a valid cache."""
        self.install()
        self.archive.write_bytes(b"corrupt")
        self.refuses_without_execution("archive digest mismatch")

    def test_missing_receipt(self) -> None:
        """An existing directory is not an installed SDK."""
        self.destination.mkdir()
        self.refuses_without_execution("incomplete install")

    def test_malformed_receipt(self) -> None:
        """JSON of the wrong type cannot pass as provenance."""
        self.install()
        self.write_receipt([])
        self.refuses_without_execution("malformed SDK provenance")

    def test_truncated_receipt(self) -> None:
        """An interrupted receipt write never becomes a usable cache."""
        self.install()
        (self.destination / sdk.RECEIPT).write_text('{"provenance":')
        self.refuses_without_execution("Expecting value")

    def test_symlink_receipt(self) -> None:
        """Provenance must be stored in the installation, not another tree."""
        self.install()
        receipt = self.destination / sdk.RECEIPT
        external = self.destination.parent / "receipt.json"
        receipt.rename(external)
        receipt.symlink_to(external)
        self.refuses_without_execution("missing regular SDK provenance receipt")

    def test_wrong_provenance(self) -> None:
        """Every cache input is bound, including the whole digest and prefix."""
        self.install()
        original = self.read_receipt()
        self.assertEqual(set(original["provenance"]), PROVENANCE_FIELDS)
        for key in sorted(PROVENANCE_FIELDS):
            with self.subTest(key=key):
                receipt = json.loads(json.dumps(original))
                receipt["provenance"][key] = "wrong"
                self.write_receipt(receipt)
                self.refuses_without_execution("provenance mismatch")

    def test_provenance_values(self) -> None:
        """The installer digest and host are the ones measured here, independently."""
        self.install()
        provenance = self.read_receipt()["provenance"]
        installer = Path(sdk.__file__).resolve()
        self.assertEqual(provenance["installer_sha256"],
                         hashlib.sha256(installer.read_bytes()).hexdigest())
        self.assertEqual(provenance["host"], {"os": platform.system(),
                                              "architecture": platform.machine()})
        self.assertEqual(provenance["destination"], str(self.destination))

    def test_changed_installer(self) -> None:
        """A cache made by other installer bytes is refused before its tools run."""
        self.install()
        changed = self.root / "ci_rv32_sdk.py"
        changed.write_bytes(Path(sdk.__file__).read_bytes() + b"# changed\n")
        with patch.object(sdk, "__file__", str(changed)):
            self.refuses_without_execution("provenance mismatch")

    def test_retargeted_symlink(self) -> None:
        """Pointing the selector at another installed tool is cache drift."""
        self.install()
        selector = self.destination / sdk.COMPILER
        selector.unlink()
        selector.symlink_to("fixture-gcc-twin")
        self.refuses_without_execution("inventory mismatch")

    def test_escaping_compiler(self) -> None:
        """A compiler whose realpath leaves the prefix is never executed."""
        self.install()
        outside = self.root / "outside-gcc"
        outside.write_text(FIXTURE_TOOL)
        outside.chmod(0o755)
        selector = self.destination / sdk.COMPILER
        selector.unlink()
        selector.symlink_to(outside)
        with patch.object(sdk.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "realpath escapes"):
                sdk.identify(self.destination)
            run.assert_not_called()

    def test_archive_root(self) -> None:
        """An authenticated archive with another root is still not extracted."""
        wrong_root = fixture_archive(
            self.root, "wrong-root",
            '#!/bin/sh\nset -eu\npwd > share/buildroot/sdk-location\n',
            arcname="another-release")
        with patch.object(sdk, "ARCHIVE_SHA256", sdk.digest(wrong_root)):
            with patch.object(sdk.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "archive root mismatch"):
                    sdk.install(self.destination, wrong_root)
                run.assert_not_called()
        self.assertFalse(self.destination.exists())

    def test_special_file(self) -> None:
        """A FIFO planted in the cache is refused before any tool runs."""
        self.install()
        os.mkfifo(self.destination / "sysroot/planted-fifo")
        self.refuses_without_execution("unexpected SDK entry")

    def test_extra_receipt_section(self) -> None:
        """A receipt carrying an unexpected section is malformed."""
        self.install()
        receipt = self.read_receipt()
        receipt["extra"] = {}
        self.write_receipt(receipt)
        self.refuses_without_execution("malformed SDK provenance")

    def test_incomplete_and_corrupt_tree(self) -> None:
        """Deletion, replacement, mode change and extra files all refuse."""
        self.install()
        tool = self.destination / "bin/fixture-gcc"
        content = tool.read_bytes()
        for label in ("missing", "bytes", "mode", "extra", "link"):
            with self.subTest(defect=label):
                tool.write_bytes(content)
                tool.chmod(0o755)
                if label == "missing":
                    tool.unlink()
                elif label == "bytes":
                    tool.write_text("corrupt")
                elif label == "mode":
                    tool.chmod(0o644)
                elif label == "extra":
                    (self.destination / "extra").write_text("extra")
                else:
                    tool.unlink()
                    tool.symlink_to("/bin/false")
                self.refuses_without_execution("inventory mismatch")
                if tool.is_symlink():
                    tool.unlink()
                (self.destination / "extra").unlink(missing_ok=True)

    def test_failed_relocation(self) -> None:
        """A failed relocation leaves no success receipt and cannot become a hit."""
        real_run = sdk.subprocess.run

        def fail_relocation(argv: list[str], **kwargs: object) -> object:
            """Extract normally, then fail the actual relocation invocation."""
            if argv[0].endswith("relocate-sdk.sh"):
                raise OSError("relocation failed")
            return real_run(argv, **kwargs)

        with patch.object(sdk.subprocess, "run", side_effect=fail_relocation):
            with self.assertRaisesRegex(OSError, "relocation failed"):
                self.install()
        self.assertFalse((self.destination / sdk.RECEIPT).exists())
        self.refuses_without_execution("incomplete install")

    def test_unrelocated_sdk(self) -> None:
        """Even a successful process must prove its relocation result."""
        self.install()
        (self.destination / "share/buildroot/sdk-location").write_text("/old/prefix\n")
        with self.assertRaisesRegex(ValueError, "relocation receipt mismatch"):
            sdk.identify(self.destination)

    def test_wrong_tool(self) -> None:
        """A compiler with the wrong version or target cannot create a receipt."""
        self.install()
        tool = self.destination / "bin/fixture-gcc"
        original = tool.read_text()
        for before, after, reason in (("14.3.0", "13.1.0", "version mismatch"),
                                      ("riscv32-", "riscv64-", "target mismatch"),
                                      ('echo "$root/sysroot"', 'echo /tmp', "sysroot")):
            with self.subTest(reason=reason):
                tool.write_text(original.replace(before, after))
                with self.assertRaisesRegex(ValueError, reason):
                    sdk.identify(self.destination)

    def test_wrong_tool_receipt(self) -> None:
        """Cached identification must agree with the program actually invoked."""
        self.install()
        receipt = self.read_receipt()
        receipt["tools"]["version"] = "wrong version"
        self.write_receipt(receipt)
        with self.assertRaisesRegex(ValueError, "tool identification mismatch"):
            sdk.verify(self.destination)

    def test_symlink_destination(self) -> None:
        """Do not overwrite or adopt a tree reached through a selector symlink."""
        target = self.destination.parent / "other"
        target.mkdir()
        self.destination.symlink_to(target, target_is_directory=True)
        self.refuses_without_execution("symlink parents")
        self.assertEqual(list(target.iterdir()), [])

    def test_unsupported_host(self) -> None:
        """The fixed x86-64 archive cannot silently adopt another host."""
        with patch.object(sdk.platform, "machine", return_value="aarch64"):
            self.refuses_without_execution("unsupported SDK host")

    def test_moved_cache(self) -> None:
        """A relocated tree is bound to the prefix where it was measured."""
        self.install()
        previous = self.destination
        self.destination = self.destination.parent / "moved"
        shutil.move(previous, self.destination)
        self.refuses_without_execution("provenance mismatch")


if __name__ == "__main__":
    unittest.main(verbosity=2)
