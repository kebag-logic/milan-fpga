python3 -m pip install --quiet pyyaml
python3 scripts/ci_builder_legs.py run 0 --receipt "$RUNNER_TEMP/gate-results/builder-leg-0.json" -- python3 sw/builder/test_builder.py --require-rv32
