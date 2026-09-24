#!/usr/bin/env bash
# Extract the specific 802.1AS / Milan lines this review relies on, with the
# PDF hashes, from a local standards directory. Needs pdftotext (poppler).
# Only single matched lines are printed (formula rows, table rows, headings).
# Usage: clause_receipts.sh <standards-dir> <scratch-dir>
set -u
std=${1:?standards dir}; out=${2:?scratch dir}
mkdir -p "$out"
conv() { pdftotext -layout "$std/$1.pdf" "$out/$1.txt"; printf '%s  %s.pdf (%s text lines)\n' "$(sha256sum "$std/$1.pdf" | cut -c1-64)" "$1" "$(wc -l < "$out/$1.txt")"; }
echo "## PDF identities"
for f in 802.1AS-2011 802.1AS-2011_Cor1-2013 802.1AS-2011_Cor_2-2015 802.1AS-2020 802.1BA-2011; do conv "$f"; done
cp "$std/Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf" "$out/milan12.pdf"
pdftotext -layout "$out/milan12.pdf" "$out/milan12.txt"
printf '%s  Milan_Specification_Consolidated_v1.2_Final_Approved 20231130.pdf\n' "$(sha256sum "$out/milan12.pdf" | cut -c1-64)"
g() { local f=$1; shift; echo "### $f :: $*"; grep -n -E "$@" "$out/$f.txt" | sed 's/  */ /g'; echo "matches=$(grep -c -E "$@" "$out/$f.txt")"; }
A=802.1AS-2011; C1=802.1AS-2011_Cor1-2013; C2=802.1AS-2011_Cor_2-2015; N=802.1AS-2020
echo "## 2011: every line naming delayAsymmetry (count and clause context lines)"
grep -n -c -i 'delayAsymmetry' "$out/$A.txt"
g $A 'This standard does not explicitly require the measurement of delayAsymmetry|defined to be positive when the responder'
g $A '^ *10\.2\.4\.8 delayAsymmetry|^ *delayAsymmetry is zero\.'
g $A 'neighborPropDelay\*\(rcvdPSSyncPtr->rateRatio/neighborRateRatio\) \+ delayAsymmetry|delayAsymmetry/rcvdPSSyncPtr->rateRatio'
g $A 'Figure 10-9.ClockSlaveSync state machine$|Figure 10-4.PortSyncSyncReceive state machine$|rateRatio \+= \(neighborRateRatio'
g $A 'delayAsymmetry \(see 10\.2\.4\.8\) for this port divided by rateRatio|same is true of any delayAsymmetry'
g $A 'd\)    The quantity delayAsymmetry|The quantity \(ts,i . upstreamTxTime\)\(rateRatioi\)'
g $A '^ *11\.2\.14\.2\.3 setFollowUp|the quantity delayAsymmetry is used in the|Table 11-5.Value of correction field$'
g $A 'causes time-synchronization information to be'
g $A '^ *11\.2\.15\.2\.4 computePropTime'
g $A 'CSN egress port also modifies the ClockSlaveSync|upstreamTxTime, neighborPropDelay, neighborRateRatio, and delayAsymmetry values'
g $A '^ *14\.6\.9 delayAsymmetry|delayAsymmetry +scaledNs +RW +Tdot3FD|Tdot3FD = Required|It is recommended that the *$|^ *data type be scaledNs|offsetFromMaster +ScaledNs'
g $A -A1 'delayAsymmetry +scaledNs +RW +Tdot3FD'
g $A '^ *MGT +Is management|synchronization in Bridges supported|^ *MIB +Is the IEEE 8021-AS-MIB|MINTA-8'
g $A '^ *10\.2\.4\.5 syncInterval'
echo "## Cor1: Table 14-6 replacement keeps the row; 11.2.13.2.1 f) restated"
g $C1 'Change Table 14-6 as follows|delayAsymmetry +scaledNs +RW +Tdot3FD|Change 11\.2\.13\.2\.1 as follows|Change 10\.2\.12\.2\.1 as follows'
echo "## Cor2: scope and absence of delayAsymmetry"
g $C2 'This corrigendum only makes changes to Figure 11-8'
echo "delayAsymmetry lines in Cor2: $(grep -c -i 'asymmetry' "$out/$C2.txt")"
echo "## 2020 comparison row"
g $N '^ *10\.2\.13 ClockSlaveSync|^ *11\.2\.14\.2\.1 setMDSyncReceiveMDSR|^ *11\.2\.15\.2\.3 setFollowUp|^ *11\.2\.17\.2 Differences'
g $N 'adds$|delayAsymmetry separately when computing upstreamTxTime|corrects the computed mean link'
echo "## 802.1BA-2011: management/MIB requirement lines"
echo "MIB or management-of lines: $(grep -c -i -E '\bMIB\b|management of' "$out/802.1BA-2011.txt")"
echo "## Milan v1.2"
echo "asymmetr lines: $(grep -c -i 'asymmetr' "$out/milan12.txt")"
g milan12 'defined by \[802\.1AS\], \[802\.1AS-2011/Cor1\]|Seamless network redundancy is not a mandatory|R-PAAD shall have at least two AVB-capable|^ *31 +0x00000001 +REDUNDANCY|^ *1 +NOT_IMPLEMENTED'
