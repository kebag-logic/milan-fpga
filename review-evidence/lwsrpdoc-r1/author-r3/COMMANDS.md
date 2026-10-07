# Command ledger

Commands execute in the foreground. No checks are piped.

| Command | rc |
| --- | --- |
| `rtk git remote get-url origin` | 0 |
| `rtk git rev-parse HEAD` | 0 |
| `rtk git status --short --branch` | 0 |
| `rtk rg --files -g AGENTS.md -g '*.md' -g '!node_modules' -g '!vendor'` | 0 |
| `rtk proxy python3` (create handoff skeleton and command recorder) | 0 |
| `rtk proxy bash -c 'for p in /AGENTS.md /data/AGENTS.md $VALIDATION_STORAGE/AGENTS.md $LANES/AGENTS.md; do if [ -f "$p" ]; then cat "$p"; fi; done'` | 0 |
| `rtk rg --files -g '!*.pdf'` | 0 |
| `rtk proxy cat README.md doc/architecture.md the removed agent-instruction page | 0 |
| `rtk proxy gh api repos/kebag-logic/lwSRP/issues/1 --jq .body` | 0 |
| `rtk proxy gh api repos/kebag-logic/lwSRP/issues/comments/6030336537 --jq .body` | 0 |
| `rtk proxy gh issue comment 1 --repo kebag-logic/lwSRP --body '[A561] TAKEN'` | 0 |
| `rtk proxy cat src/include/shish_lan/mrp.h src/include/shish_lan/mrp_pdu.h` | 0 |
| `rtk proxy cat CMakeLists.txt build.sh behave.ini Kconfig.zephyr zephyr/module.yml src/ports/alloc.h src/ports/alloc.c src/ports/timer.h src/ports/timer.c tests/features/environment.py` | 0 |
| `rtk proxy wc -l src/core/mrp_mad.c src/core/mrp_pdu.c src/core/switch_ctrl.c src/modules/mmrp.c src/modules/msrp.c src/modules/mvrp.c src/modules/sim_adapter.c tests/unit/mrp_pdu_test.c tests/unit/placeholder.c tests/features/steps/switch_steps.py tests/features/switch.feature` | 0 |
| `rtk proxy cat src/include/shish_lan/switch.h src/include/shish_lan/switch_ctrl.h src/core/switch_ctrl.c src/modules/sim_adapter.h` | 0 |
| `rtk proxy gh api repos/kebag-logic/lwSRP/issues --paginate --jq '.[] &#124; {number,title,html_url,state}'` | 0 |
| `rtk proxy sed -n 1,340p src/core/mrp_mad.c` | 0 |
| `rtk proxy sed -n 341,690p src/core/mrp_mad.c` | 0 |
| `rtk proxy sed -n 215,430p src/include/shish_lan/mrp.h` | 0 |
| `rtk proxy cat src/core/mrp_pdu.c` | 0 |
| `rtk proxy sed -n 691,1000p src/core/mrp_mad.c` | 0 |
| `rtk proxy cat src/modules/mvrp.c src/modules/mmrp.c` | 0 |
| `rtk proxy cat src/include/shish_lan/mvrp.h src/include/shish_lan/mmrp.h src/include/shish_lan/msrp.h` | 0 |
| `rtk proxy bash -c 'command -v cmake; command -v cc; command -v behave; command -v mmdc; command -v python3; pkg-config --modversion cgreen'` | 1 |
| `rtk proxy cat tests/unit/placeholder.c tests/unit/mrp_pdu_test.c tests/features/switch.feature tests/features/steps/switch_steps.py src/modules/sim_adapter.c` | 0 |
| `rtk proxy cat src/modules/msrp.c` | 0 |
| `rtk proxy git ls-files` | 0 |
| `rtk proxy sed -n 260,430p src/modules/msrp.c` | 0 |
| `rtk proxy cat tests/unit/placeholder.c tests/unit/mrp_pdu_test.c tests/features/switch.feature tests/features/steps/switch_steps.py src/modules/sim_adapter.c` | 0 |
| `rtk proxy ls -l /usr/include/cgreen /usr/local/include/cgreen /usr/local/lib/libcgreen.so` | 2 |
| `rtk proxy git clone --depth 1 https://github.com/cgreen-devs/cgreen.git $VALIDATION_STORAGE/lwsrpdoc-a561/cgreen-src` | 0 |
| `rtk proxy python3 -` | 0 |
| `rtk proxy git log -1 '--format=%h %s'` | 0 |
| `rtk proxy rg -n '/home/&#124;/data/&#124;@&#124;[Cc]laude&#124;[Cc]odex&#124;[Oo]pen[Aa][Ii]&#124;[Gg][Pp][Tt]&#124;[Gg]emini&#124;[Cc]opilot' --glob '!the removed agent-instruction page' --glob '!doc/architecture.drawio'` | 0 |
| `rtk proxy cat src/include/shish_lan/mvrp.h src/include/shish_lan/mmrp.h src/include/shish_lan/msrp.h` | 0 |
| `rtk proxy sed -n 1,220p $VALIDATION_STORAGE/lwsrpdoc-a561/cgreen-src/CMakeLists.txt` | 0 |
| `rtk proxy cat $WORKSPACE_HOME/.local/bin/mmdc` | 0 |
| `rtk proxy cmake -S $VALIDATION_STORAGE/lwsrpdoc-a561/cgreen-src -B $VALIDATION_STORAGE/lwsrpdoc-a561/cgreen-build -DCMAKE_INSTALL_PREFIX=$VALIDATION_STORAGE/lwsrpdoc-a561/deps -DCGREEN_WITH_UNIT_TESTS=OFF -DCGREEN_WITH_LIBXML2=OFF` | 0 |
| `rtk proxy cmake --build $VALIDATION_STORAGE/lwsrpdoc-a561/cgreen-build --parallel 2` | 0 |
| `rtk proxy cmake --install $VALIDATION_STORAGE/lwsrpdoc-a561/cgreen-build` | 0 |
| `rtk proxy env CMAKE_PREFIX_PATH=$VALIDATION_STORAGE/lwsrpdoc-a561/deps cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` | 0 |
| `rtk proxy cmake --build build --parallel 2` | 0 |
| `rtk proxy git -C $VALIDATION_STORAGE/lwsrpdoc-a561/cgreen-src rev-parse HEAD` | 0 |
| `rtk proxy ./build/unit_tests` | 0 |
| `rtk proxy ctest --test-dir build --output-on-failure` | 0 |
| `rtk proxy behave` | 1 |
| `rtk proxy env CPATH=$VALIDATION_STORAGE/lwsrpdoc-a561/deps/include LIBRARY_PATH=$VALIDATION_STORAGE/lwsrpdoc-a561/deps/lib cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests` | 0 |
| `rtk proxy env LD_LIBRARY_PATH=$VALIDATION_STORAGE/lwsrpdoc-a561/deps/lib ./build/mrp_pdu_tests` | 0 |
| `rtk proxy python3 -` | 0 |
| `rtk proxy python3 -` | 0 |
| `rtk proxy python3 doc/tools/check_sentences.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344649912288282.log`) | 0 |
| `rtk proxy python3 doc/tools/check_references.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344649913955093.log`) | 0 |
| `rtk proxy behave --dry-run` (cwd: `$VALIDATION_STORAGE/lwsrpdoc-a561/review`; log: `command-1791344649927634721.log`) | 0 |
| `rtk proxy python3 doc/tools/check_links.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344649915901404.log`) | 1 |
| `rtk proxy env DOC_SCRATCH=$VALIDATION_STORAGE/lwsrpdoc-a561 bash -c 'rtk proxy python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"'` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344662500288621.log`) | 0 |
| `rtk proxy git status --short` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344698593335439.log`) | 0 |
| `rtk proxy git diff --check` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344698599527301.log`) | 0 |
| `rtk proxy python3 -c 'import cairosvg; import PIL; print("Raster preview dependencies available")'` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344698592620196.log`) | 1 |
| `rtk proxy git diff --stat` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344698600756806.log`) | 0 |
| `rtk proxy gh api repos/kebag-logic/lwSRP --jq '{private,visibility}'` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344698593163631.log`) | 0 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344740055041368.log`) | 0 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344756155333940.log`) | 0 |
| `rtk proxy readlink -f $WORKSPACE_HOME/.local/bin/mmdc` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344768640413142.log`) | 0 |
| `rtk proxy node --input-type=module -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344780643736558.log`) | 0 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344857976573788.log`) | 0 |
| `rtk proxy cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` (scratch snapshot; log `page-command-01.log`) | 0 |
| `rtk proxy cmake --build build --parallel 2` (scratch snapshot; log `page-command-02.log`) | 0 |
| `rtk proxy ctest --test-dir build --output-on-failure` (scratch snapshot; log `page-command-03.log`) | 0 |
| `rtk proxy behave` (scratch snapshot; log `page-command-04.log`) | 1 |
| `rtk proxy cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug` (scratch snapshot; log `page-command-05.log`) | 0 |
| `rtk proxy cmake --build build --parallel 2` (scratch snapshot; log `page-command-06.log`) | 0 |
| `rtk proxy ctest --test-dir build --output-on-failure` (scratch snapshot; log `page-command-07.log`) | 0 |
| `rtk proxy ./build/unit_tests` (scratch snapshot; log `page-command-08.log`) | 0 |
| `rtk proxy behave` (scratch snapshot; log `page-command-09.log`) | 1 |
| `rtk proxy behave --dry-run` (scratch snapshot; log `page-command-10.log`) | 0 |
| `rtk proxy cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests <<'C'<br>#include <cgreen/cgreen.h><br>TestSuite *mrp_pdu_suite(void);<br>int main(void)<br>{<br>    return run_test_suite(mrp_pdu_suite(), create_text_reporter());<br>}<br>C` (scratch snapshot; log `page-command-11.log`) | 0 |
| `rtk proxy ./build/mrp_pdu_tests` (scratch snapshot; log `page-command-12.log`) | 0 |
| `rtk proxy python3 doc/tools/check_sentences.py` (scratch snapshot; log `page-command-13.log`) | 0 |
| `rtk proxy python3 doc/tools/check_references.py` (scratch snapshot; log `page-command-14.log`) | 0 |
| `rtk proxy python3 doc/tools/check_links.py` (scratch snapshot; log `page-command-15.log`) | 1 |
| `rtk proxy python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` (scratch snapshot; log `page-command-16.log`) | 0 |
| `rtk proxy python3 $VALIDATION_STORAGE/lwsrpdoc-a561/page_commands.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344858132090684.log`) | 0 |
| `rtk proxy python3 doc/tools/check_sentences.py` (deliberately invalid scratch fixture) | 1 |
| `rtk proxy python3 doc/tools/check_references.py` (deliberately invalid scratch fixture) | 1 |
| `rtk proxy python3 doc/tools/check_links.py --local-only` (deliberately invalid scratch fixture) | 1 |
| `rtk proxy python3 doc/tools/render_mermaid.py --output $VALIDATION_STORAGE/lwsrpdoc-a561/fixture-graphs` (deliberately invalid scratch fixture) | 1 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344902137664726.log`) | 0 |
| `rtk proxy python3 doc/tools/check_references.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344929601841514.log`) | 0 |
| `rtk proxy python3 doc/tools/check_references.py` (negative fixture after inline identifier fix) | 1 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344929762811833.log`) | 0 |
| `rtk proxy node --input-type=module -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344955875557062.log`) | 0 |
| `rtk proxy git diff --exit-code 19f5796 -- src tests CMakeLists.txt build.sh zephyr Kconfig.zephyr behave.ini` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344957120683084.log`) | 0 |
| `rtk proxy python3 doc/tools/check_sentences.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344957112253214.log`) | 0 |
| `rtk proxy python3 doc/tools/check_links.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344957113981237.log`) | 1 |
| `rtk proxy python3 doc/tools/render_mermaid.py --output $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs` (cwd: `$LANES/lwsrp-docs`; log: `command-1791344974304198400.log`) | 0 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345004526407194.log`) | 0 |
| `rtk proxy node --input-type=module -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345025741355979.log`) | 0 |

## Individual render commands

| Command | rc |
| --- | --- |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/CONTRIBUTING.md-47.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/CONTRIBUTING.md-47.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/README.md-14.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/README.md-14.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-architecture.md-10.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-architecture.md-10.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-architecture.md-34.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-architecture.md-34.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-architecture.md-56.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-architecture.md-56.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-28.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-28.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-75.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-75.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-103.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-103.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-124.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-124.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-143.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-143.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-166.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-166.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-186.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-186.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-201.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-developer.md-201.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-46.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-46.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-81.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-81.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-115.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-115.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-143.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-143.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-168.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-168.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-198.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-integrator.md-198.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-manager.md-41.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-manager.md-41.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-tester.md-61.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-tester.md-61.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-tester.md-91.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/graphs/doc-tester.md-91.svg -b white` (log `command-1791344662500288621.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/fixture-graphs/README.md-12.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/fixture-graphs/README.md-12.svg -b white` (log `command-1791344902137664726.log`) | 1 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/CONTRIBUTING.md-47.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/CONTRIBUTING.md-47.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/README.md-14.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/README.md-14.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-architecture.md-10.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-architecture.md-10.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-architecture.md-34.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-architecture.md-34.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-architecture.md-56.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-architecture.md-56.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-28.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-28.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-75.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-75.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-103.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-103.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-125.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-125.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-144.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-144.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-168.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-168.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-188.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-188.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-205.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-developer.md-205.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-46.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-46.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-81.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-81.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-115.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-115.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-143.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-143.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-168.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-168.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-198.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-integrator.md-198.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-manager.md-41.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-manager.md-41.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-tester.md-61.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-tester.md-61.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-tester.md-91.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-graphs/doc-tester.md-91.svg -b white` (log `command-1791344974304198400.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/fixture-graphs/README.md-12.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/fixture-graphs/README.md-12.svg -b white` (log `fixture-4.log`) | 1 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/CONTRIBUTING.md-47.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/CONTRIBUTING.md-47.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/README.md-14.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/README.md-14.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-architecture.md-10.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-architecture.md-10.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-architecture.md-34.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-architecture.md-34.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-architecture.md-56.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-architecture.md-56.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-28.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-28.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-75.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-75.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-103.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-103.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-125.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-125.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-144.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-144.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-168.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-168.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-188.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-188.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-204.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-developer.md-204.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-46.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-46.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-81.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-81.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-115.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-115.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-143.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-143.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-168.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-168.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-198.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-integrator.md-198.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-manager.md-41.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-manager.md-41.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-tester.md-61.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-tester.md-61.svg -b white` (log `page-command-16.log`) | 0 |
| `mmdc -i $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-tester.md-91.mmd -o $VALIDATION_STORAGE/lwsrpdoc-a561/final-render/graphs/doc-tester.md-91.svg -b white` (log `page-command-16.log`) | 0 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345085971278828.log`) | 0 |
| `rtk proxy git add README.md CONTRIBUTING.md doc the removed agent-instruction page (cwd: `$LANES/lwsrp-docs`; log: `command-1791345108852648650.log`) | 0 |
| `rtk proxy git diff --cached --name-status` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345108996353991.log`) | 0 |
| `rtk proxy git diff --cached --check` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345108987524561.log`) | 0 |
| `rtk proxy git diff --cached --stat` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345108996410946.log`) | 0 |
| `rtk proxy python3 doc/tools/check_references.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345108998698469.log`) | 0 |
| `rtk proxy python3 doc/tools/check_sentences.py` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345109004668888.log`) | 0 |
| `rtk proxy git -c 'user.name=Documentation Contributor' -c user.email=documentation@example.invalid -c commit.gpgsign=false commit -m 'docs: document public release usage and limitations'` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345117456708649.log`) | 0 |
| `rtk proxy git log -1 --format=fuller` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345117631388051.log`) | 0 |
| `rtk proxy git status --short --branch` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345117632817887.log`) | 0 |
| `rtk proxy git diff --exit-code 19f5796 HEAD -- src tests CMakeLists.txt build.sh zephyr Kconfig.zephyr behave.ini` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345117620966742.log`) | 0 |
| `rtk proxy git diff --check 19f5796 HEAD` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345117620967994.log`) | 0 |
| `rtk proxy git rev-parse HEAD` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345117616246529.log`) | 0 |

## Expanded initial dependency probes

| Command | rc |
| --- | --- |
| `command -v cmake` | 0 |
| `command -v cc` | 0 |
| `command -v behave` | 0 |
| `command -v mmdc` | 0 |
| `command -v python3` | 0 |
| `pkg-config --modversion cgreen` | 1 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345163934108353.log`) | 0 |
| `rtk proxy python3 -` (cwd: `$LANES/lwsrp-docs`; log: `command-1791345193627644879.log`) | 0 |
| `rtk proxy git rev-parse HEAD` | 0 |
| `rtk proxy git status --porcelain` | 0 |
| `rtk proxy git show -s --format=%B HEAD` | 0 |
| `rtk proxy gh issue comment 1 --repo kebag-logic/lwSRP --body '[A561] REVIEW READY 38fa78209264bbfd2444ceea638bdb5967d3ead8'` | 0 |
| `rtk proxy python3 $VALIDATION_STORAGE/lwsrpdoc-a561/finalize.py` | 0 |
