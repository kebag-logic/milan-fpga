#!/usr/bin/env bash
# release.sh CLONE MODE WORK: every tracked config's builder output at one clone, and the AX7101 configs' SoC exports
# without --build or software (--no-compile-software). MODE "base" runs the builder on each config as it stands (the
# base's configs are all-fabric); MODE "head" runs it with --placement all-fabric for the AX7101 configs (the release
# recipe BUILD_PLACEMENT=all-fabric names) and as it stands for the rest. Outputs: WORK/builder/<stem>/ (a copy of
# sw/builder/out/<stem>) and WORK/export-<stem>/.
set -euo pipefail
C=$(realpath "$1"); MODE=$2; W=$(realpath -m "$3"); T=$(dirname "$(realpath "$0")")
source "$T/env.sh"
mkdir -p "$W/builder"; cd "$C"
echo "head $(git rev-parse HEAD) porcelain $(git status --porcelain | wc -l)"
for cfg in configs/*.yaml; do
  stem=$(basename "$cfg" .yaml); extra=()
  if [ "$MODE" = head ] && [[ $stem == endstation_ax7101_* ]]; then extra=(--placement all-fabric); fi
  /usr/bin/python3 sw/builder/endstation_builder.py "$cfg" "${extra[@]}" > "$W/builder-$stem.log" 2>&1
  rm -rf "$W/builder/$stem"; cp -r "sw/builder/out/$stem" "$W/builder/$stem"
  if [[ $stem == endstation_ax7101_* ]]; then
    mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$stem/soc_params.json)
    printf '%s\n' "${ARGV[@]}" > "$W/argv-$stem.txt"
    rm -rf "$W/export-$stem"
    (cd sw/litex && python3 milan_soc.py "${ARGV[@]}" --entity-gen-dir "$C/configs/generated/$stem" \
       --no-compile-software --output-dir "$W/export-$stem" > "$W/export-$stem.log" 2>&1)
  fi
done
echo "porcelain after: $(git status --porcelain | tr '\n' ' ')"; echo RELEASE_DONE
