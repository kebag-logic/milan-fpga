#!/usr/bin/env bash
# Does `make stale` catch a draw.io source committed after its export, in a full
# clone and in a depth-1 clone (what actions/checkout@v4 gives docs-gates)?
set -u
REPO=$1; S=$2; HEAD_SHA=91cef52b3c56cc69f66966b004782a69d2940a46
git clone -q "$REPO" "$S/full" && cd "$S/full" && git checkout -q --detach $HEAD_SHA
git -c user.name=probe -c user.email=probe@invalid commit -q --allow-empty -m "export unchanged" >/dev/null
sleep 2
sed -i 's/MAC RX&#10;async FIFO/MAC RX&#10;async FIFO (edited)/' docs/diagrams/src/01-top-level.drawio
git -c user.name=probe -c user.email=probe@invalid commit -q -am "source edited after its export"
make stale; echo "full clone: make stale rc=$?"
git clone -q --depth 1 "file://$S/full" "$S/shallow" && cd "$S/shallow"
echo "shallow commits: $(git rev-list --count HEAD)"
make stale; echo "depth-1 clone: make stale rc=$?"
