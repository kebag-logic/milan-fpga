#!/bin/sh
# Build disposable locales for the probes. Usage: mklocales.sh <outdir>
# Never touches installed locale data; output is used through LOCPATH only.
out=${1:?outdir}
mkdir -p "$out"
for spec in zh_TW:BIG5 zh_HK:BIG5-HKSCS ko_KR:JOHAB ja_JP:WINDOWS-31J en_US:ISO-8859-1 en_US:UTF-8; do
  src=${spec%%:*}; cm=${spec#*:}
  localedef --no-archive -c -i "$src" -f "$cm" "$out/$src.$cm" >/dev/null 2>&1
  echo "localedef $src.$cm exit $?"
done
