# receipt.sh SRC DST: one sanitized copy (sourced paths come from the environment, not this file)
python3 -I "$SAN" "$1" "$2" "$SCRATCH=<scratch>" "$REPO=<repo>" "$TOOLS=<tools>" "$HOME=<home>" "$DATA=<data>"
