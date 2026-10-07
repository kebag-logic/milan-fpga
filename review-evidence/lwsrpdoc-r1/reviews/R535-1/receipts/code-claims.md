The comparison applies only to head 5f9b9d99e1d94485fc00a1b1539baf2ae861cb65.
The local normative reference was read directly; it is not included in this packet.
No statement below certifies complete protocol conformance.

| Documentation claim | Inspected authority | Result |
| --- | --- | --- |
| Declaration requests and registration indications; no complete transmit path | src/core/mrp_mad.c:780,793,843; pending_tx at 502; public header | Accurate. The public operations never assemble and send pending messages. |
| Optional propagation with 32-bit masks; no topology filter | src/core/mrp_mad.c:514,532; src/modules/msrp.c:112; VLAN and MAC callback templates | Accurate. Only the stream application supplies propagation callbacks. |
| Protocol identifiers and addresses | src/include/shish_lan/mrp.h:174; application templates | Present. No link-layer transport is supplied. |
| Applicant selected transitions and differences | Standard Table 10-3 and notes; src/core/mrp_mad.c:116-275,495-505 | All three displayed graphs match the selected normative transitions. Listed declaration, receive, recovery, periodic, conditional and scheduling differences are accurate. |
| Registrar selected transitions and differences | Standard Table 10-4; src/core/mrp_mad.c:311-395,550-582 | Displayed states match. Local New incorrectly registers; received Join in LV adds an indication. Both differences are disclosed. |
| LeaveAll selected transitions and differences | Standard Table 10-5; src/core/mrp_mad.c:639-673 | Displayed states match. Extra timer restart on active transmission, fixed interval and absent transmitted frame are disclosed. |
| PeriodicTransmission selected transitions and differences | Standard Table 10-6; src/core/mrp_mad.c:679-700,871-882 | Displayed states match. Extra disable cancellation, 20-centisecond interval and divergent Applicant handling are disclosed. |
| Timer values and lifetime | Standard 10.7.4.3,10.7.4.4,10.7.11; timer constants and src/ports/timer.c | Accurate. One-second normative periodic interval and randomized LeaveAll differ from code. Destruction leaves dangling timer links. |
| Vector parsing and one-value encoding | src/core/mrp_pdu.c:75-104,116-221 | Accurate. Encoder handles one value; subtype encoding is absent. |
| Receive validation limitations | src/core/mrp_pdu.c:128-138,154-155,215-216,224-255 | Accurate. Version/list length are ignored. Earlier callbacks can precede a later error. |
| MAC/service codecs without filtering database or mode enforcement | src/modules/mmrp.c and src/include/shish_lan/mmrp.h | Accurate. Constants use service=1/MAC=2; contradictory interface comments are disclosed. |
| VLAN codec without VLAN database, flush or propagation | src/modules/mvrp.c | Accurate. Decode validates 1–4094; declaration wrapper does not. |
| Talker Advertise, Talker Failed and Listener; no Domain/admission | src/modules/msrp.c and public stream structures | Accurate. Stored Talkers use host structures; Listeners use nine bytes. |
| Listener subtype decoding; ignored vector offsets | src/core/mrp_pdu.c:163-216; src/modules/msrp.c decode callback; standard 35.2.2.7.2 and 35.2.2.8 | Accurate. No claim of full Listener receive conformance is made. |
| Talker flooding and Listener propagation toward registered Talkers | src/modules/msrp.c map_join/map_leave; registered-port lookup | Accurate for implemented policy. Topology gating, resource admission and hardware reservation are absent. |
| Copied operation table, borrowed context, per-port and per-attribute state | src/core/mrp_mad.c:59-95,446-492,735-760 | Accurate in prose. The data-structure graph has the separately reported visual defect. |
| Global ticking and synchronous observation | src/core/mrp_mad.c:588-625,854-858,888-945; src/ports/timer.c | Accurate. Tick arguments are ignored. Observer reports changed Applicant/Registrar states. |
| Simulation versus real adapter | src/modules/sim_adapter.c; src/include/shish_lan/switch.h | Accurate. Forty-eight flags and range checks; no frame/register hardware model or generic factory. |
| Register queue excluded from builds and retaining descriptor linkage | Both source lists; src/core/switch_ctrl.c; public queue header | Accurate. Missing linked successor can spin indefinitely. |
| Host and embedded build choices | CMakeLists.txt, Kconfig.zephyr, zephyr/module.yml, build.sh | Accurate. Host requires the unit dependency. Embedded list has seven protocol/port sources and no test bindings. Wrapper does not build. |
| Nine tests, 1690 assertions, three scenarios, ten steps | tests/unit/main.c, tests/unit/mrp_pdu_test.c, feature hooks/steps, execution receipts | Reproduced. No parser/state/timer/coverage-percentage claim is made. State assertions are correctly described as operation-result proxies. |
| Style migration | Removed base instruction page versus CONTRIBUTING.md:8-16 | All original requirements survive: mandatory braces, tagged enums, no enum typedef, one element per line, uppercase tag prefix. |

The four deferred work areas remain planned without invented issue links.
The licence paragraph matches the assignment's required text.
All eight documentation pages start with the required licence identifier.
