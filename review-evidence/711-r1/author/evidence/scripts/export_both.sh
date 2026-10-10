#!/bin/bash
$SCRATCH/scripts/export_shipping.sh base e8454e2751d05b02ee8e5a571857589ab358ab86 > $SCRATCH/res-export-base.log 2>&1; echo "base rc=$?" >> $SCRATCH/res-export.rc
$SCRATCH/scripts/export_shipping.sh cand 49b437f445e34b558106c8799c1ffc0a5dc844cf > $SCRATCH/res-export-cand.log 2>&1; echo "cand rc=$?" >> $SCRATCH/res-export.rc
