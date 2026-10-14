base="$(git merge-base HEAD refs/remotes/origin/dev)"; echo base=$base; git cat-file -e "$base^{commit}"; python3 scripts/check_em_dash.py --base "$base"
