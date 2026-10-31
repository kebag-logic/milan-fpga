set -euo pipefail
python3 -m pip install --quiet pyyaml
python3 sw/mailbox/publication_census.py --check --selftest --jobs "$CI_CENSUS_JOBS"
