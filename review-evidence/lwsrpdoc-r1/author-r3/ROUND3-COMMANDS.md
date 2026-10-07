# Round 3 nested commands

| Command | rc |
| --- | --- |
| `rtk proxy git ls-files -z` (snapshot inventory) | 0 |
| `rtk proxy cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` (README.md:35; scratch snapshot; log page-command-01.log) | 0 |
| `rtk proxy cmake --build build --parallel 2` (README.md:36; scratch snapshot; log page-command-02.log) | 0 |
| `rtk proxy ctest --test-dir build --output-on-failure` (README.md:37; scratch snapshot; log page-command-03.log) | 0 |
| `rtk proxy behave` (README.md:38; scratch snapshot; log page-command-04.log) | 0 |
| `rtk proxy cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` (doc/tester.md:15; scratch snapshot; log page-command-05.log) | 0 |
| `rtk proxy cmake --build build --parallel 2` (doc/tester.md:16; scratch snapshot; log page-command-06.log) | 0 |
| `rtk proxy ctest --test-dir build --output-on-failure` (doc/tester.md:17; scratch snapshot; log page-command-07.log) | 0 |
| `rtk proxy ./build/unit_tests` (doc/tester.md:18; scratch snapshot; log page-command-08.log) | 0 |
| `rtk proxy behave` (doc/tester.md:19; scratch snapshot; log page-command-09.log) | 0 |
| `rtk proxy behave --dry-run` (doc/tester.md:20; scratch snapshot; log page-command-10.log) | 0 |
| `rtk proxy cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests <<'C'<br>#include <cgreen/cgreen.h><br>TestSuite *mrp_pdu_suite(void);<br>int main(void)<br>{<br>    return run_test_suite(mrp_pdu_suite(), create_text_reporter());<br>}<br>C` (doc/tester.md:45; scratch snapshot; log page-command-11.log) | 0 |
| `rtk proxy ./build/mrp_pdu_tests` (doc/tester.md:53; scratch snapshot; log page-command-12.log) | 0 |
| `rtk proxy python3 doc/tools/check_sentences.py` (doc/tools/README.md:14; scratch snapshot; log page-command-13.log) | 0 |
| `rtk proxy python3 doc/tools/check_references.py` (doc/tools/README.md:15; scratch snapshot; log page-command-14.log) | 0 |
| `rtk proxy python3 doc/tools/check_references.py --self-test` (doc/tools/README.md:16; scratch snapshot; log page-command-15.log) | 0 |
| `rtk proxy python3 doc/tools/check_links.py --github-auth` (doc/tools/README.md:17; scratch snapshot; log page-command-16.log) | 1 |
| `rtk proxy python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` (doc/tools/README.md:18; scratch snapshot; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/CONTRIBUTING.md-48.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/CONTRIBUTING.md-48.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/README.md-14.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/README.md-14.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-10.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-10.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-34.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-34.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-56.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-56.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-29.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-29.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-78.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-78.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-116.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-116.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-148.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-148.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-184.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-184.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-220.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-220.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-249.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-249.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-275.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-275.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-46.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-46.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-81.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-81.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-127.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-127.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-158.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-158.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-183.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-183.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-215.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-215.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-manager.md-44.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-manager.md-44.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-62.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-62.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-92.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-92.svg -b white` (render subprocess; log page-command-17.log) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/CONTRIBUTING.md-48.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/CONTRIBUTING.md-48.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/README.md-14.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/README.md-14.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-10.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-10.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-34.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-34.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-56.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-architecture.md-56.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-29.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-29.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-78.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-78.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-116.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-116.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-148.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-148.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-184.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-184.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-220.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-220.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-249.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-249.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-275.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-developer.md-275.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-46.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-46.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-81.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-81.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-127.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-127.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-158.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-158.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-183.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-183.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-215.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-integrator.md-215.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-manager.md-44.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-manager.md-44.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-62.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-62.svg -b white` (final render with scratch temporary directory) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-92.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/round3/render/graphs/doc-tester.md-92.svg -b white` (final render with scratch temporary directory) | 0 |
