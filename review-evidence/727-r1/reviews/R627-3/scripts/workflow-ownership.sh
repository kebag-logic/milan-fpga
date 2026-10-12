set -euo pipefail
python3 scripts/suite_shards.py --selftest
scripts/run_all_suites.sh --shard "$SHARD/$SHARDS" --list \
  > "$RUNNER_TEMP/owned-suites"
echo "Shard $SHARD owns:"
sed 's/^/  /' "$RUNNER_TEMP/owned-suites"
case "$SHARD" in
  1) grep -Fx tsn_fuzz "$RUNNER_TEMP/owned-suites" ;;
  3) grep -Fx chmap_capture "$RUNNER_TEMP/owned-suites" ;;
  4) test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp ;;
esac
