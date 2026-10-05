The scripts take the reviewed source directory and this packet directory as positional arguments. All disposable dependencies, clones, generated images and builds belong under `scratch/`. Nothing in `scratch/` is publishable.

Prerequisites are Python, Git, make, a C++ compiler, the scoped simulator, the diagram CLI, its browser driver, and the standalone SVG renderer. Exact observed versions, simulator entry hash and installed font families are in `receipts/environment.txt`; the browser version is in `receipts/browser-bounds.json`. Python rendering dependencies were installed in `scratch/python` only. The diagram CLI was already available. No shared installation was changed.

| Script | Purpose |
|---|---|
| `scripts/run-focused.py SOURCE PACKET` | Runs `make -j16 check`, `make -j16 ids`, and three small native suites concurrently, joining in the foreground. Requires a detached exact-head clone in `scratch/suites` and the rendering environment in `scratch/python`. Set `VERILATOR_BIN` to relocate the scoped simulator. Each of three native builds uses four compilation workers. Every command has its own raw log and rc file. |
| `scripts/probe-ids.py SOURCE PACKET` | Sixteen independent positive/negative forms; both round-2 weakened parsers pass their old self-test and fail the new one; the previous parser fails the revised tests. Uses disposable fixture repositories. |
| `scripts/probe-render.py SOURCE PACKET` | Run using `scratch/python/bin/python`. Checks margin geometry, unchanged children/height, invalid input rejection, and actual freshness failures. Restores the scratch clone's edited page in `finally`. |
| `scripts/measure-browser.cjs SOURCE PACKET PUPPETEER_MODULE` | Run with Node; the third argument locates the browser driver module. Measures every text element after fonts load under six selections, captures both current figures, and requires both old figures to fail the default-font control. |
| `scripts/measure-raster.py SOURCE PACKET` | Run using `scratch/python/bin/python`. Measures text-only ink in a padded canvas with the standalone SVG renderer, and renders the unmodified current figures. Font variants replace the existing stylesheet's family. Each original figure must fail at least one font control. |
| `scripts/check-artifacts.py SOURCE PACKET` | Checks C11 executable-token identity, port names, historical source identity and removed PNGs; kills four prior figure mutants; exercises three negative ID plants and one positive plant through the full make target. |
| `scripts/check-integrity.py SOURCE` | Re-hashes every tracked blob, checks executable modes, exact HEAD/tree/index, any gitlinks and clean status. Writes JSON to stdout. |

Six font selections mean six requested configurations, not six distinct installed fonts. Only two actual families are installed here. Browser and standalone fallback choices differ; the receipts preserve measurements rather than assuming identical fallback. Bounds are measured relative to each SVG viewport. The standalone bounds are ink pixel bounds; browser bounds are text-element rectangles.

Expected negative controls have checker/self-test rc 1 or make rc 2. Those receipts are successful fault detection, not failed golden checks. `round2-*.rc` is deliberately 0: it demonstrates the old self-test's insensitivity. The final scripts and JSON receipts use the exact skipping mutation, which drops the line-broken optional member without inventing a malformed-list diagnostic.

Public evidence was fetched with read-only API requests. The supplied immutable packet's handoff describes round 1; it is retained with its verified published hash, not relabelled as round-3 execution. Hosted logs and job metadata retain their original public content. `receipts/independent-verdict.md` records the first independent verdict and ledger before prior public findings were opened.

Only `REPORT.md` and files listed in `MANIFEST.sha256` are publishable. Paths in the manifest are relative to this packet.
