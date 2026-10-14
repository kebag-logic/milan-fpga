. /jobs/lib.sh
step "behave present" 'behave --version'
step "Specification-facing suite (tests/)" 'cd tests; behave --no-capture -f plain'
