Use a clean detached checkout of `375dbe132c6f1498f2f3e714ce5905d34456c9d5` and an output packet directory.
Set `CHECKOUT` and `PACKET` to those directories. Run each command to completion.
The command proxy, a C compiler, build utilities, Python, the scenario runner, YAML parser, and authenticated read access are prerequisites.

```sh
rtk proxy mkdir -p "$PACKET/receipts"
rtk proxy curl --fail --silent --show-error --location https://www.apache.org/licenses/LICENSE-2.0.txt -o "$PACKET/receipts/apache-canonical.txt"
rtk proxy python3 "$PACKET/scripts/build_dependency.py" "$PACKET"
rtk proxy python3 "$PACKET/scripts/run_validation.py" "$CHECKOUT" "$PACKET" --jobs 16 --with-local-dependency
rtk proxy python3 "$PACKET/scripts/audit.py" "$CHECKOUT" "$PACKET"
```

The validation script waits for every subprocess. Independent lightweight checks run concurrently. Builds use sixteen jobs.
All dependency sources, builds, virtual environments and unredacted process logs stay under `scratch/`.
The dependency is fetched from its public 1.7.0 release. Its archive digest is recorded in `receipts/unit-dependency-source.json`.
The configuration parser is installed only under `scratch/parser-deps`, pinned to 14.1.0.
The script archives the exact reviewed commit into a disposable source tree before executing suites.
Its host test commands use that tree's root build directory, as required by the scenario hook.

The first review attempt lacked the unit dependency. `prerequisite-configure.log` and its exit code retain that observation.
The later configure/build/suite receipts are the completed validation with the disposable dependency present.
Published logs replace checkout and packet paths with role placeholders. Raw logs remain in unpublished scratch storage.
`validation-index.json` records original process-output hashes and path-redaction flags.

For external links, run `doc/tools/check_links.py --github-auth` with Python from the original checkout root.
The recorded run returned one for the standards publisher's HTTP 403. Six repository links passed with authentication.
For the queue unit omitted by the normal build, run the C compiler with `-std=c11 -fsyntax-only -Isrc/include -Isrc src/core/switch_ctrl.c`.

`audit.py` exits zero after completing mechanical checks, even when its receipts demonstrate review findings.
Read `history-reachability.json` and `shifted-citations.json`; zero is not an approval verdict.
The history check records object identifiers and line numbers without republishing restricted strings.
The full independent inspection covered thirteen commits and 109 unique blobs.
The official licence digest is `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.

Only `MANIFEST.sha256` entries and `REPORT.md` are intended for publication. Never publish `scratch/`.
