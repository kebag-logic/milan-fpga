#!/bin/sh
# usage: identity_probe.sh; builds both shipped configs' builder artifacts at head, dev and 1516b2ff to one output path each
for t in wc wc_dev wc_old; do
 for c in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  rm -rf "$S/idout"; mkdir -p "$S/idout"
  (cd "$S/$t" && python3 sw/builder/endstation_builder.py configs/$c.yaml -o "$S/idout") > "$S/id-$t-$c.log" 2>&1 || echo "FAIL $t $c"
  (cd "$S/idout" && find . -type f | sort | xargs sha256sum) > "$S/id-$t-$c.sha"
 done
done
for c in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
 echo "$c files: $(wc -l < "$S/id-wc-$c.sha")"
 cmp -s "$S/id-wc-$c.sha" "$S/id-wc_dev-$c.sha" && echo "  head = dev: IDENTICAL" || { echo "  head vs dev differ"; diff "$S/id-wc-$c.sha" "$S/id-wc_dev-$c.sha" | cut -c1-140; }
 cmp -s "$S/id-wc-$c.sha" "$S/id-wc_old-$c.sha" && echo "  head = 1516b2ff: IDENTICAL" || { echo "  head vs 1516b2ff differ in:"; diff "$S/id-wc-$c.sha" "$S/id-wc_old-$c.sha" | awk '/^>/{print "    "$3}'; }
done
