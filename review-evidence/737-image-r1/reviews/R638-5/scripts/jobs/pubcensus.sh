. /jobs/lib.sh
step "Yosys/sv2v version proof" 'yosys -V | grep -F "Yosys 0.66"; sv2v --version'
step "Publication census" 'python3 sw/mailbox/publication_census.py --check --selftest --jobs "$(nproc)"'
