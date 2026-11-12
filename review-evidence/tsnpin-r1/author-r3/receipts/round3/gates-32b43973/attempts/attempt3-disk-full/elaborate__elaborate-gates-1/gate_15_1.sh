python3 scripts/ci_builder_legs.py run 1 --receipt "$RUNNER_TEMP/gate-results/builder-leg-1.json" -- python3 sw/builder/test_builder.py --require-elaboration --require-rv32
