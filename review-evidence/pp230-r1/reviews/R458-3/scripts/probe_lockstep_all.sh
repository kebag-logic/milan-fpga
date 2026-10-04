for p in r3-wtsp-write-ignores-ready r3-wsid-write-ignores-ready r3-wtsp-registered-read r3-wsid-registered-read; do
  $REVIEWS/pp230-r458-3-packet/scripts/lockstep_run.sh $p $REVIEWS/pp230-r458-3-packet/scratch/probes/$p 300000 3 n2:2:2:6:5:23:37 n35:3:5:7:4:17:29 n9:9:9:7:5:23:37
done
