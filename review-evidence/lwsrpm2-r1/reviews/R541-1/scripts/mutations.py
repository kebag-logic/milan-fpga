# SPDX-License-Identifier: Apache-2.0
"""Replay the published reversals plus independent faults in a disposable tree."""
import argparse, pathlib, sys
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);p.add_argument('--prefix',type=pathlib.Path,required=True)
a=p.parse_args();path=a.source/'tests/check_reversals.py'
ns={'__file__':str(path),'__name__':'review_mutations'}
code=path.read_text().replace('build_command = ["cmake", "--build", str(build), "--parallel", "2"]','build_command = ["make", "-C", str(build), "-j16"]')
exec(compile(code,str(path),'exec'),ns)
ns['CASES'] += [
 ('independent-domain-byte-order',ns['MSRP'],'be16_put(buf + 2, d->vid);','buf[2] = (uint8_t)d->vid; buf[3] = (uint8_t)(d->vid >> 8);','unit'),
 ('independent-milan-duplicate-leave',ns['MAD'],'ai->reg == MRP_REG_STATE_IN) {\n        e = &milan_leave;','ai->reg != MRP_REG_STATE_LV) {\n        e = &milan_leave;','unit'),
 ('independent-premature-commit',ns['MAD'],'if (r != 0) {\n        return r;','if (false && r != 0) {\n        return r;','unit')]
ns['REQUIRED_FAILURES'].update({
 'independent-domain-byte-order':['domain_and_vector_offsets_match_wire_fields'],
 'independent-milan-duplicate-leave':['talker_leave_in_is_immediate','listener_leave_in_is_immediate'],
 'independent-premature-commit':['fresh_ladder_and_refusal_are_transactional'],
 'leaveall-scope':['msrp_leaveall_changes_only_the_message_type_and_port','mmrp_leaveall_changes_only_the_message_type_and_port'],
 'wire-prevalidation':['a_malformed_later_message_has_no_earlier_indications'],
 'split-fairness':['a_full_pdu_retries_omitted_attributes_before_repeats'],
 'refused-storage':['refused_pdu_survives_timers_without_aging_unsent_leaveall']})
sys.argv=[str(path),'--work-dir',str(a.packet/'scratch/mutations'),'--prefix',str(a.prefix)]
sys.exit(ns['main']())
