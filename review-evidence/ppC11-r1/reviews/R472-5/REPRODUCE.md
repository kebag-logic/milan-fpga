R472-5 focused review receipts
=============================

Run from a clean detached processor checkout at
`7124bde172a523179a2788dca825587aa5a2a1e6`. Keep this packet outside that
checkout. Scripts derive their packet directory from their own location.
Use Python 3, Git, Make, a C++ compiler, and the diagram CLI version 11.16.0.
The gate runner creates its own Python environment under packet `scratch/`
and installs the source renderer at the CI-pinned version. It installs nothing
in a shared environment.

Commands, with `/path/to/packet` replaced by this packet's location:

```sh
rtk proxy python3 /path/to/packet/scripts/review.py integrity-before
rtk proxy python3 /path/to/packet/scripts/review.py audit
rtk proxy python3 /path/to/packet/scripts/review.py gates
rtk proxy python3 /path/to/packet/scripts/review.py probes
rtk proxy python3 -B /path/to/packet/scripts/focused-notify.py
rtk proxy python3 -B /path/to/packet/scripts/prior-controls.py
rtk proxy python3 /path/to/packet/scripts/review.py integrity-final
```

`review.py` accepts `--repo PATH`; the two other scripts accept the repository
path as their optional positional argument. The notification script accepts
`REVIEW_PINNED_SIM` as the executable path, defaulting to the scoped 5.050 path
in the assignment. It checks the version and records the wrapper hash before
use. Its disposable wrapper caps compilation at four jobs per arm. The driver
uses `--jobs 3` and `MAKEFLAGS=-j16`, so at most twelve compiler jobs run.
The full processor and parent banks are not invoked.

All commands run under foreground coordinators which await every child.
Independent documentation gates run concurrently, and the three notification
mutations run concurrently after their common golden. Every disposable clone,
environment, generated script and build is under `scratch/`; it is excluded
from publication. Tests never modify the original processor checkout.

Each test has a log and return-code receipt. Negative ID controls expect rc 1
from the checker and rc 2 from Make. Deliberately weakened self-tests expect
rc 1. A mutation campaign succeeds when its golden passes and every selected
mutation fails its named checks. The notification campaign's results include
completion and named-diagnostic checks, not merely a nonzero process status.

`structural-audit.json` records exact parent ownership of all changed paths,
clean re-merge tree equality, the independent three-way document merge, and
the C11 code comparison after removing comments and whitespace.
`integrity-*.json` records every tracked blob, mode, file SHA256, index tree,
and required gitlink. This processor repository has no gitlinks.

Public source evidence was fetched read-only from the immutable parent packet
at `4a3ae4a1a4bf5a2fcd85b6d0aeff441f3f853a9f`. All six published hashes were
verified; downloaded source files remain in scratch. The manifest and hash
verification are publishable receipts. The public packet is historical
evidence for `91cef52`, not raw bank receipts for the reviewed merge.

The independent verdict and ledger were sealed before reading prior reviewer
bodies. `prior-review-index.json` lists the public comment URLs and hashes;
the other reports themselves are not republished. Formal reviews and inline
comments were empty. `REPORT.md` records their dispositions.

Hosted run/job/check snapshots are read-only observations. The two docs logs
were retrieved after permitting raw terminal escape bytes in the API output;
the initial `.error` receipts describe the downloader's output restriction,
not failed workflow jobs. Final `.rc` files report successful retrieval.

Only files named by `MANIFEST.sha256`, plus `REPORT.md`, are publishable. Check:

```sh
rtk proxy sha256sum -c MANIFEST.sha256
```
