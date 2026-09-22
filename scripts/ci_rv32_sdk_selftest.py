#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Offline installer controls use a tiny fixture archive and its own digest.

These controls are not Bootlin compatibility evidence. The real archive and
gate must also run, with no replacement of the production digest.
"""

import contextlib
import io
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import ci_rv32_sdk as sdk


class InstallerTests(unittest.TestCase):
    """Exercise installation, cache validation, and refusal before execution."""

    def setUp(self) -> None:
        """Construct a self-contained SDK with a real relocation step."""
        self.tmp = tempfile.TemporaryDirectory(prefix="rv32-installer-test-")
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.destination = root / "installed"
        source = root / sdk.RELEASE
        (source / "bin").mkdir(parents=True)
        (source / "sysroot").mkdir()
        (source / "share/buildroot/sdk-location").parent.mkdir(parents=True)
        (source / "share/buildroot/sdk-location").write_text("/old/prefix\n")
        tool = source / "bin/fixture-gcc"
        tool.write_text("#!/bin/sh\nset -eu\n"
                        'root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"\n'
                        'case "$1" in\n'
                        '  --version) echo "fixture GCC 14.3.0" ;;\n'
                        '  -dumpfullversion) echo 14.3.0 ;;\n'
                        '  -dumpmachine) echo riscv32-buildroot-linux-gnu ;;\n'
                        '  -print-sysroot) echo "$root/sysroot" ;;\n'
                        '  *) exit 9 ;;\nesac\n')
        tool.chmod(0o755)
        (source / sdk.COMPILER).symlink_to("fixture-gcc")
        relocation = source / "relocate-sdk.sh"
        relocation.write_text('#!/bin/sh\nset -eu\npwd > share/buildroot/sdk-location\n')
        relocation.chmod(0o755)
        self.archive = root / "fixture.tar.xz"
        with tarfile.open(self.archive, "w:xz") as stream:
            stream.add(source, arcname=sdk.RELEASE)
        self.addCleanup(patch.stopall)
        patch.object(sdk, "ARCHIVE_SHA256", sdk.digest(self.archive)).start()

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
        """A wrong download never reaches tar or creates an installation."""
        self.archive.write_bytes(b"not the pinned archive")
        self.refuses_without_execution("archive digest mismatch")
        self.assertFalse(self.destination.exists())

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
        for key in original["provenance"]:
            with self.subTest(key=key):
                receipt = json.loads(json.dumps(original))
                receipt["provenance"][key] = "wrong"
                self.write_receipt(receipt)
                self.refuses_without_execution("provenance mismatch")

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
