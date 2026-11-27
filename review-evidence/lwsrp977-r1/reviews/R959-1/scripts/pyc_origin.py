# SPDX-License-Identifier: Apache-2.0
"""Report, without disclosing it, where a committed CPython bytecode file was
compiled: whether its embedded source path is absolute, how deep it is, its
sha256, and whether it ends at the repository-relative source.

usage: python3 -I pyc_origin.py <checkout> <repo-relative .pyc> <repo-relative source>
"""
import hashlib
import marshal
from pathlib import Path, PurePosixPath
import subprocess
import sys

root, pyc, source = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
blob = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{pyc}"], capture_output=True, check=True).stdout
added = subprocess.run(["git", "-C", str(root), "log", "--format=%h", "--diff-filter=A", "--", pyc],
                       capture_output=True, text=True, check=True).stdout.split()
code = marshal.loads(blob[16:])
name = PurePosixPath(code.co_filename)
print(f"tracked file: {pyc}")
print(f"added by commit: {' '.join(added)}")
print(f"blob sha256: {hashlib.sha256(blob).hexdigest()}")
print(f"embedded co_filename is absolute: {name.is_absolute()}")
print(f"embedded co_filename components: {len(name.parts)}")
print(f"embedded co_filename ends with {source}: {str(name).endswith('/' + source)}")
print(f"embedded co_filename sha256: {hashlib.sha256(code.co_filename.encode()).hexdigest()}")
print(f"embedded co_filename lies under the checkout: {str(name).startswith(str(root.resolve()) + '/')}")
