# [A386] Reconnect measurement handoff

Refs #75. Branch: 75-reconnect-bench.
Base: 8bc97021f28fb7f729418d3a00851c84ea0b50fd.
Identity: PASS. All 200 numbered reconnects PASS.
Full restoration PASS. No bench lock held; all children exited.
The temporary driver and remote scripts are removed.
Local head: 0e8ec0d2bd78b1d87f84d96e095966ae7c07c525.
Only the new findings page is committed; no push.
All nine assigned gates return 0 at this exact head.
REVIEW READY published and read back exactly:
https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860095671
Packet manifests verify; every retained file is at most 200,000 bytes.

## Verified restoration and operating constraints

All 18 original stream states unbound; both clocks internal.
No rate, format, clock, power, firmware or wiring change.
CRF pairs: reference output 2 to DUT input 1;
DUT output 1 to reference input 8, one direction at a time.
Full original census: census-start.jsonl.
The active pair was unbound after each direction.
Staged scripts and the temporary capture driver were removed.
Each action releases its lock and joins every child before returning.
No detached process. Raw captures stay under /tmp/a386.

## Distribution in seconds

| Direction | Cycles | Min | Median | p95 | Max | Bound result |
|---|---|---|---|---|---|---|
| DUT listener | 100 | 0.006641168 | 0.110279505 | 0.188503018 | 0.204858977 | PASS |
| DUT talker | 100 | 0.000296777 | 0.019165141 | 0.039613701 | 0.117736084 | PASS |

## Cycle ledger

Times are relative tap nanoseconds; holds are seconds.

| Direction | Cycle | Disconnect hold | Response | First AVTP | Latency seconds | Consecutive overruns | Capture | Result |
|---|---|---|---|---|---|---|---|---|
| listener | listener-001 | 2.000248 | 4740074802 | 4852592034 | 0.112517232 | 0 | listener-001/tap.pcap | PASS |
| listener | listener-002 | 2.000246 | 4974424876 | 5152598839 | 0.178173963 | 0 | listener-002/tap.pcap | PASS |
| listener | listener-003 | 2.000322 | 5021840512 | 5148599234 | 0.126758722 | 0 | listener-003/tap.pcap | PASS |
| listener | listener-004 | 2.000229 | 5069998685 | 5148598438 | 0.078599753 | 0 | listener-004/tap.pcap | PASS |
| listener | listener-005 | 2.000254 | 4963284618 | 5048597034 | 0.085312416 | 0 | listener-005/tap.pcap | PASS |
| listener | listener-006 | 2.000245 | 5025595131 | 5148600036 | 0.123004905 | 0 | listener-006/tap.pcap | PASS |
| listener | listener-007 | 2.000331 | 5012084023 | 5150601276 | 0.138517253 | 0 | listener-007/tap.pcap | PASS |
| listener | listener-008 | 2.000309 | 5009232785 | 5148599840 | 0.139367055 | 0 | listener-008/tap.pcap | PASS |
| listener | listener-009 | 2.000301 | 5039521817 | 5048472190 | 0.008950373 | 0 | listener-009/tap.pcap | PASS |
| listener | listener-010 | 2.000245 | 5025916737 | 5148600025 | 0.122683288 | 0 | listener-010/tap.pcap | PASS |
| listener | listener-011 | 2.000250 | 4986201817 | 5146600001 | 0.160398184 | 0 | listener-011/tap.pcap | PASS |
| listener | listener-012 | 2.000285 | 5024672747 | 5148598263 | 0.123925516 | 0 | listener-012/tap.pcap | PASS |
| listener | listener-013 | 2.000271 | 4977776737 | 5148598633 | 0.170821896 | 0 | listener-013/tap.pcap | PASS |
| listener | listener-014 | 2.000272 | 4985117816 | 5050596650 | 0.065478834 | 0 | listener-014/tap.pcap | PASS |
| listener | listener-015 | 2.000233 | 4965308839 | 5048597650 | 0.083288811 | 0 | listener-015/tap.pcap | PASS |
| listener | listener-016 | 2.000258 | 4968624475 | 5048597031 | 0.079972556 | 0 | listener-016/tap.pcap | PASS |
| listener | listener-017 | 2.000305 | 5056080251 | 5246599898 | 0.190519647 | 0 | listener-017/tap.pcap | PASS |
| listener | listener-018 | 2.000218 | 5059268017 | 5148598666 | 0.089330649 | 0 | listener-018/tap.pcap | PASS |
| listener | listener-019 | 2.000238 | 4983502039 | 5150599111 | 0.167097072 | 0 | listener-019/tap.pcap | PASS |
| listener | listener-020 | 2.000223 | 5054805998 | 5246601663 | 0.191795665 | 0 | listener-020/tap.pcap | PASS |
| listener | listener-021 | 2.000232 | 4988019658 | 5046598452 | 0.058578794 | 0 | listener-021/tap.pcap | PASS |
| listener | listener-022 | 2.000261 | 5028369364 | 5148600062 | 0.120230698 | 0 | listener-022/tap.pcap | PASS |
| listener | listener-023 | 2.000245 | 5011752655 | 5046572049 | 0.034819394 | 0 | listener-023/tap.pcap | PASS |
| listener | listener-024 | 2.000287 | 5058239839 | 5146598846 | 0.088359007 | 0 | listener-024/tap.pcap | PASS |
| listener | listener-025 | 2.000327 | 5045600506 | 5148474660 | 0.102874154 | 0 | listener-025/tap.pcap | PASS |
| listener | listener-026 | 2.000284 | 5017981717 | 5050597505 | 0.032615788 | 0 | listener-026/tap.pcap | PASS |
| listener | listener-027 | 2.000228 | 5019027160 | 5146474683 | 0.127447523 | 0 | listener-027/tap.pcap | PASS |
| listener | listener-028 | 2.000287 | 4974687185 | 5146599293 | 0.171912108 | 0 | listener-028/tap.pcap | PASS |
| listener | listener-029 | 2.000271 | 5031811051 | 5148598293 | 0.116787242 | 0 | listener-029/tap.pcap | PASS |
| listener | listener-030 | 2.000326 | 5026261178 | 5046596242 | 0.020335064 | 0 | listener-030/tap.pcap | PASS |
| listener | listener-031 | 2.000273 | 5058082033 | 5249300082 | 0.191218049 | 0 | listener-031/tap.pcap | PASS |
| listener | listener-032 | 2.000260 | 5030682791 | 5046473444 | 0.015790653 | 0 | listener-032/tap.pcap | PASS |
| listener | listener-033 | 2.000295 | 5066373319 | 5246602487 | 0.180229168 | 0 | listener-033/tap.pcap | PASS |
| listener | listener-034 | 2.000247 | 5001799370 | 5047035436 | 0.045236066 | 0 | listener-034/tap.pcap | PASS |
| listener | listener-035 | 2.000247 | 5013746489 | 5047660265 | 0.033913776 | 0 | listener-035/tap.pcap | PASS |
| listener | listener-036 | 2.000262 | 4965986515 | 5146598281 | 0.180611766 | 0 | listener-036/tap.pcap | PASS |
| listener | listener-037 | 2.000255 | 4973257159 | 5146599077 | 0.173341918 | 0 | listener-037/tap.pcap | PASS |
| listener | listener-038 | 2.000238 | 5035551671 | 5046471664 | 0.010919993 | 0 | listener-038/tap.pcap | PASS |
| listener | listener-039 | 2.000262 | 5027996193 | 5044597840 | 0.016601647 | 0 | listener-039/tap.pcap | PASS |
| listener | listener-040 | 2.000276 | 4981308822 | 5148474502 | 0.167165680 | 0 | listener-040/tap.pcap | PASS |
| listener | listener-041 | 2.000245 | 4976657060 | 5046596536 | 0.069939476 | 0 | listener-041/tap.pcap | PASS |
| listener | listener-042 | 2.000251 | 5009986527 | 5148598972 | 0.138612445 | 0 | listener-042/tap.pcap | PASS |
| listener | listener-043 | 2.000275 | 4980315056 | 5044596695 | 0.064281639 | 0 | listener-043/tap.pcap | PASS |
| listener | listener-044 | 2.000212 | 4991539739 | 5046597092 | 0.055057353 | 0 | listener-044/tap.pcap | PASS |
| listener | listener-045 | 2.000251 | 5022839407 | 5046596527 | 0.023757120 | 0 | listener-045/tap.pcap | PASS |
| listener | listener-046 | 2.000246 | 5009143283 | 5144473695 | 0.135330412 | 0 | listener-046/tap.pcap | PASS |
| listener | listener-047 | 2.000232 | 5059544884 | 5146848496 | 0.087303612 | 0 | listener-047/tap.pcap | PASS |
| listener | listener-048 | 2.000292 | 4966674168 | 5144598906 | 0.177924738 | 0 | listener-048/tap.pcap | PASS |
| listener | listener-049 | 2.000220 | 4982884049 | 5044593250 | 0.061709201 | 0 | listener-049/tap.pcap | PASS |
| listener | listener-050 | 2.000230 | 4987194757 | 5046597337 | 0.059402580 | 0 | listener-050/tap.pcap | PASS |
| listener | listener-051 | 2.000235 | 5032454105 | 5044471701 | 0.012017596 | 0 | listener-051/tap.pcap | PASS |
| listener | listener-052 | 2.000267 | 4964925953 | 5146598547 | 0.181672594 | 0 | listener-052/tap.pcap | PASS |
| listener | listener-053 | 2.000224 | 4990143953 | 5044597313 | 0.054453360 | 0 | listener-053/tap.pcap | PASS |
| listener | listener-054 | 2.000256 | 5033480309 | 5044598311 | 0.011118002 | 0 | listener-054/tap.pcap | PASS |
| listener | listener-055 | 2.000237 | 5031745084 | 5046596311 | 0.014851227 | 0 | listener-055/tap.pcap | PASS |
| listener | listener-056 | 2.000249 | 5059211515 | 5247714533 | 0.188503018 | 0 | listener-056/tap.pcap | PASS |
| listener | listener-057 | 2.000327 | 4991523576 | 5044599116 | 0.053075540 | 0 | listener-057/tap.pcap | PASS |
| listener | listener-058 | 2.000303 | 5006840072 | 5144474499 | 0.137634427 | 0 | listener-058/tap.pcap | PASS |
| listener | listener-059 | 2.000296 | 5019085365 | 5145504917 | 0.126419552 | 0 | listener-059/tap.pcap | PASS |
| listener | listener-060 | 2.000266 | 5039391712 | 5242476076 | 0.203084364 | 0 | listener-060/tap.pcap | PASS |
| listener | listener-061 | 2.000302 | 5037831102 | 5044472270 | 0.006641168 | 0 | listener-061/tap.pcap | PASS |
| listener | listener-062 | 2.000312 | 4970699122 | 5045063249 | 0.074364127 | 0 | listener-062/tap.pcap | PASS |
| listener | listener-063 | 2.000239 | 4964562932 | 5043564877 | 0.079001945 | 0 | listener-063/tap.pcap | PASS |
| listener | listener-064 | 2.000309 | 4995934382 | 5042595267 | 0.046660885 | 0 | listener-064/tap.pcap | PASS |
| listener | listener-065 | 2.000273 | 4991586156 | 5144851915 | 0.153265759 | 0 | listener-065/tap.pcap | PASS |
| listener | listener-066 | 2.000237 | 5016558143 | 5046595701 | 0.030037558 | 0 | listener-066/tap.pcap | PASS |
| listener | listener-067 | 2.000291 | 5014263934 | 5043788883 | 0.029524949 | 0 | listener-067/tap.pcap | PASS |
| listener | listener-068 | 2.000291 | 5004422030 | 5042594672 | 0.038172642 | 0 | listener-068/tap.pcap | PASS |
| listener | listener-069 | 2.000238 | 5031632873 | 5044473495 | 0.012840622 | 0 | listener-069/tap.pcap | PASS |
| listener | listener-070 | 2.000250 | 5002105252 | 5142599718 | 0.140494466 | 0 | listener-070/tap.pcap | PASS |
| listener | listener-071 | 2.000220 | 4990356567 | 5144599130 | 0.154242563 | 0 | listener-071/tap.pcap | PASS |
| listener | listener-072 | 2.000250 | 5004710059 | 5144474499 | 0.139764440 | 0 | listener-072/tap.pcap | PASS |
| listener | listener-073 | 2.000224 | 5037117145 | 5241976122 | 0.204858977 | 0 | listener-073/tap.pcap | PASS |
| listener | listener-074 | 2.000268 | 4981147880 | 5168724928 | 0.187577048 | 0 | listener-074/tap.pcap | PASS |
| listener | listener-075 | 2.000258 | 4998325813 | 5042597077 | 0.044271264 | 0 | listener-075/tap.pcap | PASS |
| listener | listener-076 | 2.000342 | 5013787968 | 5142599318 | 0.128811350 | 0 | listener-076/tap.pcap | PASS |
| listener | listener-077 | 2.000239 | 5030903706 | 5145723343 | 0.114819637 | 0 | listener-077/tap.pcap | PASS |
| listener | listener-078 | 2.000249 | 5027127465 | 5142599504 | 0.115472039 | 0 | listener-078/tap.pcap | PASS |
| listener | listener-079 | 2.000261 | 5025456440 | 5042847297 | 0.017390857 | 0 | listener-079/tap.pcap | PASS |
| listener | listener-080 | 2.000229 | 5002454047 | 5142598711 | 0.140144664 | 0 | listener-080/tap.pcap | PASS |
| listener | listener-081 | 2.000238 | 5024773859 | 5042597901 | 0.017824042 | 0 | listener-081/tap.pcap | PASS |
| listener | listener-082 | 2.000262 | 4988143551 | 5042597302 | 0.054453751 | 0 | listener-082/tap.pcap | PASS |
| listener | listener-083 | 2.000245 | 5010452927 | 5142973533 | 0.132520606 | 0 | listener-083/tap.pcap | PASS |
| listener | listener-084 | 2.000603 | 5022819041 | 5042721496 | 0.019902455 | 0 | listener-084/tap.pcap | PASS |
| listener | listener-085 | 2.000270 | 4980591674 | 5042596883 | 0.062005209 | 0 | listener-085/tap.pcap | PASS |
| listener | listener-086 | 2.000246 | 5031868895 | 5140473076 | 0.108604181 | 0 | listener-086/tap.pcap | PASS |
| listener | listener-087 | 2.000264 | 4962356717 | 5142598874 | 0.180242157 | 0 | listener-087/tap.pcap | PASS |
| listener | listener-088 | 2.000247 | 5021600207 | 5142473874 | 0.120873667 | 0 | listener-088/tap.pcap | PASS |
| listener | listener-089 | 2.000272 | 4975079012 | 5040596661 | 0.065517649 | 0 | listener-089/tap.pcap | PASS |
| listener | listener-090 | 2.000248 | 4978326440 | 5140598850 | 0.162272410 | 0 | listener-090/tap.pcap | PASS |
| listener | listener-091 | 2.000315 | 5056830260 | 5140975257 | 0.084144997 | 0 | listener-091/tap.pcap | PASS |
| listener | listener-092 | 2.000256 | 5028644291 | 5140599121 | 0.111954830 | 0 | listener-092/tap.pcap | PASS |
| listener | listener-093 | 2.000223 | 5003875462 | 5140474079 | 0.136598617 | 0 | listener-093/tap.pcap | PASS |
| listener | listener-094 | 2.000280 | 5016428206 | 5142599150 | 0.126170944 | 0 | listener-094/tap.pcap | PASS |
| listener | listener-095 | 2.000262 | 4987725143 | 5140598102 | 0.152872959 | 0 | listener-095/tap.pcap | PASS |
| listener | listener-096 | 2.000229 | 5050920284 | 5140723503 | 0.089803219 | 0 | listener-096/tap.pcap | PASS |
| listener | listener-097 | 2.000230 | 5045124841 | 5144599770 | 0.099474929 | 0 | listener-097/tap.pcap | PASS |
| listener | listener-098 | 2.000225 | 5015383557 | 5140598682 | 0.125215125 | 0 | listener-098/tap.pcap | PASS |
| listener | listener-099 | 2.000267 | 5061780559 | 5240601306 | 0.178820747 | 0 | listener-099/tap.pcap | PASS |
| listener | listener-100 | 2.000243 | 5014047562 | 5038847276 | 0.024799714 | 0 | listener-100/tap.pcap | PASS |
| talker | talker-001 | 2.000245 | 4724328879 | 4842064963 | 0.117736084 | 0 | talker-001/tap.pcap | PASS |
| talker | talker-002 | 2.000315 | 5011901690 | 5038067568 | 0.026165878 | 0 | talker-002/tap.pcap | PASS |
| talker | talker-003 | 2.000307 | 4973971294 | 4992066952 | 0.018095658 | 0 | talker-003/tap.pcap | PASS |
| talker | talker-004 | 2.000275 | 5002108687 | 5022067358 | 0.019958671 | 0 | talker-004/tap.pcap | PASS |
| talker | talker-005 | 2.000291 | 5034237551 | 5054067821 | 0.019830270 | 0 | talker-005/tap.pcap | PASS |
| talker | talker-006 | 2.000287 | 5013518906 | 5032067526 | 0.018548620 | 0 | talker-006/tap.pcap | PASS |
| talker | talker-007 | 2.000256 | 4962611480 | 4982066830 | 0.019455350 | 0 | talker-007/tap.pcap | PASS |
| talker | talker-008 | 2.000253 | 4983892338 | 5004067146 | 0.020174808 | 0 | talker-008/tap.pcap | PASS |
| talker | talker-009 | 2.000263 | 5040080285 | 5060067868 | 0.019987583 | 0 | talker-009/tap.pcap | PASS |
| talker | talker-010 | 2.000240 | 5041171520 | 5060067885 | 0.018896365 | 0 | talker-010/tap.pcap | PASS |
| talker | talker-011 | 2.000232 | 5024341193 | 5044067639 | 0.019726446 | 0 | talker-011/tap.pcap | PASS |
| talker | talker-012 | 2.000234 | 5050531768 | 5070068029 | 0.019536261 | 0 | talker-012/tap.pcap | PASS |
| talker | talker-013 | 2.000262 | 4993703367 | 4994066935 | 0.000363568 | 0 | talker-013/tap.pcap | PASS |
| talker | talker-014 | 2.000261 | 5012409052 | 5030067453 | 0.017658401 | 0 | talker-014/tap.pcap | PASS |
| talker | talker-015 | 2.000263 | 5007701764 | 5026067415 | 0.018365651 | 0 | talker-015/tap.pcap | PASS |
| talker | talker-016 | 2.000297 | 5060893493 | 5080068106 | 0.019174613 | 0 | talker-016/tap.pcap | PASS |
| talker | talker-017 | 2.000276 | 5017082110 | 5038067616 | 0.020985506 | 0 | talker-017/tap.pcap | PASS |
| talker | talker-018 | 2.000331 | 5037286355 | 5056067855 | 0.018781500 | 0 | talker-018/tap.pcap | PASS |
| talker | talker-019 | 2.000301 | 4986453735 | 5026067436 | 0.039613701 | 0 | talker-019/tap.pcap | PASS |
| talker | talker-020 | 2.000262 | 4977657199 | 4996067058 | 0.018409859 | 0 | talker-020/tap.pcap | PASS |
| talker | talker-021 | 2.000271 | 5020340440 | 5040067623 | 0.019727183 | 0 | talker-021/tap.pcap | PASS |
| talker | talker-022 | 2.000263 | 4976510760 | 4996067046 | 0.019556286 | 0 | talker-022/tap.pcap | PASS |
| talker | talker-023 | 2.000335 | 5024648937 | 5044067663 | 0.019418726 | 0 | talker-023/tap.pcap | PASS |
| talker | talker-024 | 2.000244 | 5041770854 | 5042067631 | 0.000296777 | 0 | talker-024/tap.pcap | PASS |
| talker | talker-025 | 2.000240 | 4997940911 | 5016067274 | 0.018126363 | 0 | talker-025/tap.pcap | PASS |
| talker | talker-026 | 2.000242 | 5024031674 | 5044067681 | 0.020036007 | 0 | talker-026/tap.pcap | PASS |
| talker | talker-027 | 2.000231 | 5073270129 | 5092068341 | 0.018798212 | 0 | talker-027/tap.pcap | PASS |
| talker | talker-028 | 2.000256 | 5069403270 | 5088068266 | 0.018664996 | 0 | talker-028/tap.pcap | PASS |
| talker | talker-029 | 2.000259 | 5004587880 | 5024067382 | 0.019479502 | 0 | talker-029/tap.pcap | PASS |
| talker | talker-030 | 2.000235 | 4964756568 | 4984066877 | 0.019310309 | 0 | talker-030/tap.pcap | PASS |
| talker | talker-031 | 2.000281 | 5054944619 | 5074068095 | 0.019123476 | 0 | talker-031/tap.pcap | PASS |
| talker | talker-032 | 2.000251 | 5048123490 | 5066067972 | 0.017944482 | 0 | talker-032/tap.pcap | PASS |
| talker | talker-033 | 2.000231 | 4985212435 | 5004067127 | 0.018854692 | 0 | talker-033/tap.pcap | PASS |
| talker | talker-034 | 2.000301 | 4999393544 | 5018067324 | 0.018673780 | 0 | talker-034/tap.pcap | PASS |
| talker | talker-035 | 2.000262 | 5023585233 | 5044067665 | 0.020482432 | 0 | talker-035/tap.pcap | PASS |
| talker | talker-036 | 2.000248 | 5020759209 | 5040067614 | 0.019308405 | 0 | talker-036/tap.pcap | PASS |
| talker | talker-037 | 2.000339 | 4992942530 | 5012067255 | 0.019124725 | 0 | talker-037/tap.pcap | PASS |
| talker | talker-038 | 2.000365 | 5023022021 | 5042067650 | 0.019045629 | 0 | talker-038/tap.pcap | PASS |
| talker | talker-039 | 2.000296 | 4995191832 | 5014067260 | 0.018875428 | 0 | talker-039/tap.pcap | PASS |
| talker | talker-040 | 2.000240 | 5023274674 | 5042067638 | 0.018792964 | 0 | talker-040/tap.pcap | PASS |
| talker | talker-041 | 2.000264 | 5048461296 | 5068067974 | 0.019606678 | 0 | talker-041/tap.pcap | PASS |
| talker | talker-042 | 2.000251 | 4975629775 | 4994066995 | 0.018437220 | 0 | talker-042/tap.pcap | PASS |
| talker | talker-043 | 2.000293 | 4991812699 | 5010067190 | 0.018254491 | 0 | talker-043/tap.pcap | PASS |
| talker | talker-044 | 2.000328 | 5043900361 | 5126068769 | 0.082168408 | 0 | talker-044/tap.pcap | PASS |
| talker | talker-045 | 2.000310 | 4945070501 | 4964066609 | 0.018996108 | 0 | talker-045/tap.pcap | PASS |
| talker | talker-046 | 2.000231 | 4979115413 | 4998067033 | 0.018951620 | 0 | talker-046/tap.pcap | PASS |
| talker | talker-047 | 2.000277 | 4983204337 | 5002067093 | 0.018862756 | 0 | talker-047/tap.pcap | PASS |
| talker | talker-048 | 2.000294 | 5019016870 | 5040067584 | 0.021050714 | 0 | talker-048/tap.pcap | PASS |
| talker | talker-049 | 2.000403 | 5018816005 | 5038067602 | 0.019251597 | 0 | talker-049/tap.pcap | PASS |
| talker | talker-050 | 2.000266 | 5035267385 | 5054067829 | 0.018800444 | 0 | talker-050/tap.pcap | PASS |
| talker | talker-051 | 2.000278 | 5001199809 | 5020067349 | 0.018867540 | 0 | talker-051/tap.pcap | PASS |
| talker | talker-052 | 2.000334 | 5004261549 | 5022067359 | 0.017805810 | 0 | talker-052/tap.pcap | PASS |
| talker | talker-053 | 2.000264 | 5047211318 | 5066067978 | 0.018856660 | 0 | talker-053/tap.pcap | PASS |
| talker | talker-054 | 2.000265 | 4981389864 | 5000067068 | 0.018677204 | 0 | talker-054/tap.pcap | PASS |
| talker | talker-055 | 2.000253 | 4987585128 | 5006067163 | 0.018482035 | 0 | talker-055/tap.pcap | PASS |
| talker | talker-056 | 2.000232 | 4995763247 | 5014067218 | 0.018303971 | 0 | talker-056/tap.pcap | PASS |
| talker | talker-057 | 2.000270 | 5064852272 | 5084068149 | 0.019215877 | 0 | talker-057/tap.pcap | PASS |
| talker | talker-058 | 2.000325 | 4987022753 | 5006067134 | 0.019044381 | 0 | talker-058/tap.pcap | PASS |
| talker | talker-059 | 2.000234 | 4959100875 | 5026067400 | 0.066966525 | 0 | talker-059/tap.pcap | PASS |
| talker | talker-060 | 2.000262 | 4997298387 | 5018067284 | 0.020768897 | 0 | talker-060/tap.pcap | PASS |
| talker | talker-061 | 2.000315 | 5002459596 | 5022067345 | 0.019607749 | 0 | talker-061/tap.pcap | PASS |
| talker | talker-062 | 2.000252 | 5000599216 | 5020067326 | 0.019468110 | 0 | talker-062/tap.pcap | PASS |
| talker | talker-063 | 2.000248 | 4983720752 | 5026067396 | 0.042346644 | 0 | talker-063/tap.pcap | PASS |
| talker | talker-064 | 2.000276 | 5036897635 | 5056067792 | 0.019170157 | 0 | talker-064/tap.pcap | PASS |
| talker | talker-065 | 2.000235 | 4980976456 | 5000067061 | 0.019090605 | 0 | talker-065/tap.pcap | PASS |
| talker | talker-066 | 2.000278 | 5014147559 | 5034067494 | 0.019919935 | 0 | talker-066/tap.pcap | PASS |
| talker | talker-067 | 2.000239 | 5043325020 | 5062067888 | 0.018742868 | 0 | talker-067/tap.pcap | PASS |
| talker | talker-068 | 2.000239 | 4993512885 | 5014067245 | 0.020554360 | 0 | talker-068/tap.pcap | PASS |
| talker | talker-069 | 2.000264 | 5023600808 | 5042067611 | 0.018466803 | 0 | talker-069/tap.pcap | PASS |
| talker | talker-070 | 2.000230 | 5050783891 | 5070067992 | 0.019284101 | 0 | talker-070/tap.pcap | PASS |
| talker | talker-071 | 2.000250 | 4961958080 | 4982066815 | 0.020108735 | 0 | talker-071/tap.pcap | PASS |
| talker | talker-072 | 2.000251 | 5018640609 | 5036067530 | 0.017426921 | 0 | talker-072/tap.pcap | PASS |
| talker | talker-073 | 2.000273 | 5061818803 | 5080068101 | 0.018249298 | 0 | talker-073/tap.pcap | PASS |
| talker | talker-074 | 2.000238 | 5047015853 | 5066067930 | 0.019052077 | 0 | talker-074/tap.pcap | PASS |
| talker | talker-075 | 2.000252 | 5050203663 | 5052067739 | 0.001864076 | 0 | talker-075/tap.pcap | PASS |
| talker | talker-076 | 2.000257 | 5053408056 | 5072068027 | 0.018659971 | 0 | talker-076/tap.pcap | PASS |
| talker | talker-077 | 2.000279 | 5015575654 | 5036067551 | 0.020491897 | 0 | talker-077/tap.pcap | PASS |
| talker | talker-078 | 2.000241 | 4991658490 | 5012067226 | 0.020408736 | 0 | talker-078/tap.pcap | PASS |
| talker | talker-079 | 2.000279 | 5026829732 | 5046067681 | 0.019237949 | 0 | talker-079/tap.pcap | PASS |
| talker | talker-080 | 2.000327 | 5065000053 | 5084068210 | 0.019068157 | 0 | talker-080/tap.pcap | PASS |
| talker | talker-081 | 2.000300 | 4997096611 | 5016067288 | 0.018970677 | 0 | talker-081/tap.pcap | PASS |
| talker | talker-082 | 2.000333 | 5057212970 | 5076068094 | 0.018855124 | 0 | talker-082/tap.pcap | PASS |
| talker | talker-083 | 2.000276 | 5015330494 | 5034067562 | 0.018737068 | 0 | talker-083/tap.pcap | PASS |
| talker | talker-084 | 2.000258 | 5049391608 | 5068068020 | 0.018676412 | 0 | talker-084/tap.pcap | PASS |
| talker | talker-085 | 2.000255 | 5033453334 | 5054067791 | 0.020614457 | 0 | talker-085/tap.pcap | PASS |
| talker | talker-086 | 2.000312 | 4987546034 | 5006067174 | 0.018521140 | 0 | talker-086/tap.pcap | PASS |
| talker | talker-087 | 2.000249 | 4992580266 | 5012067256 | 0.019486990 | 0 | talker-087/tap.pcap | PASS |
| talker | talker-088 | 2.000276 | 5021652561 | 5040067644 | 0.018415083 | 0 | talker-088/tap.pcap | PASS |
| talker | talker-089 | 2.000240 | 4988740555 | 5008067193 | 0.019326638 | 0 | talker-089/tap.pcap | PASS |
| talker | talker-090 | 2.000314 | 5007897613 | 5124068775 | 0.116171162 | 0 | talker-090/tap.pcap | PASS |
| talker | talker-091 | 2.000293 | 5092985202 | 5114068636 | 0.021083434 | 0 | talker-091/tap.pcap | PASS |
| talker | talker-092 | 2.000296 | 5034147524 | 5054067819 | 0.019920295 | 0 | talker-092/tap.pcap | PASS |
| talker | talker-093 | 2.000286 | 5017234569 | 5038067618 | 0.020833049 | 0 | talker-093/tap.pcap | PASS |
| talker | talker-094 | 2.000309 | 4998351809 | 5018067336 | 0.019715527 | 0 | talker-094/tap.pcap | PASS |
| talker | talker-095 | 2.000272 | 5075485250 | 5096068403 | 0.020583153 | 0 | talker-095/tap.pcap | PASS |
| talker | talker-096 | 2.000271 | 5040547484 | 5060067923 | 0.019520439 | 0 | talker-096/tap.pcap | PASS |
| talker | talker-097 | 2.000253 | 4988719325 | 5008067210 | 0.019347885 | 0 | talker-097/tap.pcap | PASS |
| talker | talker-098 | 2.000262 | 5028907619 | 5048067744 | 0.019160125 | 0 | talker-098/tap.pcap | PASS |
| talker | talker-099 | 2.000271 | 5050985088 | 5070068045 | 0.019082957 | 0 | talker-099/tap.pcap | PASS |
| talker | talker-100 | 2.000275 | 5014108285 | 5034067573 | 0.019959288 | 0 | talker-100/tap.pcap | PASS |

## Handoff status

Both direction counts are complete; the early-stop rule never triggered.
All 18 states are unbound. Original settings and descriptors match.
Final image CRCs match; UART grader 10/10; final capture is quiescent.
Growth and sender-attributed MSRP analysis are complete.
The findings page records all three acceptance criteria as PASS for measured CRF.

The separate initial talker bind took 6.889398468 seconds.
Bridge Listener Ready arrived after 6.888605306 seconds, followed by
valid CRF after another 0.000793162 seconds. This initial bind is excluded
from the numbered reconnect distribution and remains an observed limitation.
AAF is unmeasured. The issue is not closed by this evidence.

All 206 raw captures remain under /tmp/a386 and are indexed by size and
SHA-256. The packet contains analysis, controller and console observations,
restoration evidence, exact gate logs, and recursive manifests.
Independent reviews remain required; no bench work remains.
