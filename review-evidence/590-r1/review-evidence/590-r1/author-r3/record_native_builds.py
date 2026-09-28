"""Record identities of retained build binaries without copying them."""
from pathlib import Path
import hashlib
import json

root = Path("$VALIDATION_STORAGE/590-a411")
rows = []
for pattern in ("*/native/Vsim", "*/software/bios/bios.bin", "*/software/bios/bios.elf"):
    for path in sorted(root.glob(pattern)):
        rows.append(dict(path=str(path), size=path.stat().st_size,
                         sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(Path(__file__).parent / "native-build-identities.json").write_text(json.dumps(rows, indent=2) + "\n")
print(str(len(rows)) + " build identities recorded; no binaries copied")
