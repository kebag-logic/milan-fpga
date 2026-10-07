<!-- SPDX-License-Identifier: Apache-2.0 -->
| Reversal | Build rc | Check rc | Named failed check |
| --- | --- | --- | --- |
| bounded-header-initialization | n/a | 1 | strict initialized-header compilation |
| changed-listener-indication | 0 | 8 | receive_suite -> changed_registered_listener_notifies_without_duplicate_join  |
| domain-member-order | 0 | 8 | msrp_values_suite -> domain_callback_preserves_existing_member_order  |
| domain-offset | 0 | 8 | msrp_values_suite -> domain_and_vector_offsets_match_wire_fields  |
| hosted-allocation-header | n/a | 1 | hosted header dependency rejection |
| hosted-error-header | n/a | 1 | hosted header dependency rejection |
| independent-domain-byte-order | 0 | 8 | msrp_values_suite -> domain_and_vector_offsets_match_wire_fields  |
| independent-milan-duplicate-leave | 0 | 8 | milan_suite -> listener_leave_in_is_immediate ; milan_suite -> talker_leave_in_is_immediate  |
| independent-premature-commit | 0 | 8 | integration_suite -> registrar_ages_while_a_transmission_is_retained ; transmit_suite -> fresh_ladder_and_refusal_are_transactional ; transmit_suite -> refused_pdu_survives_timers_without_aging_unsent_leaveall  |
| leaveall-all-types | 0 | 8 | integration_suite -> transmitted_leaveall_includes_every_supported_type  |
| leaveall-randomization | 0 | 8 | integration_suite -> leaveall_draws_are_inside_the_required_interval  |
| leaveall-scope | 0 | 8 | integration_suite -> mmrp_leaveall_changes_only_the_message_type_and_port ; integration_suite -> msrp_leaveall_changes_only_the_message_type_and_port  |
| listener-offset | 0 | 8 | msrp_values_suite -> domain_and_vector_offsets_match_wire_fields  |
| listener-redeclaration | 0 | 8 | transmit_suite -> changed_listener_redeclares_from_a_quiet_applicant  |
| local-registration | 0 | 8 | transmit_suite -> fresh_ladder_and_refusal_are_transactional ; transmit_suite -> refused_pdu_survives_timers_without_aging_unsent_leaveall  |
| local-withdrawal-value | 0 | 8 | integration_suite -> local_withdrawal_keeps_the_registered_listener_value  |
| milan-delayed-in-leave | 0 | 8 | milan_suite -> listener_leave_in_is_immediate ; milan_suite -> talker_leave_in_is_immediate  |
| milan-option-scope | 0 | 8 | milan_suite -> disabled_application_option_preserves_ieee_timing ; milan_suite -> mmrp_keeps_ieee_leave_timing ; milan_suite -> msrp_constructor_selects_the_build_profile ; milan_suite -> mvrp_keeps_ieee_leave_timing  |
| milan-profile-selection | 0 | 8 | milan_suite -> msrp_constructor_selects_the_build_profile  |
| milan-restarted-lv-deadline | 0 | 8 | milan_suite -> leave_in_lv_keeps_the_original_deadline  |
| mmrp-address | 0 | 8 | integration_suite -> every_application_uses_its_standard_destination  |
| msrp-address | 0 | 8 | integration_suite -> every_application_uses_its_standard_destination ; msrp_values_suite -> domain_and_vector_offsets_match_wire_fields  |
| mvrp-address | 0 | 8 | integration_suite -> every_application_uses_its_standard_destination  |
| pdu-endmark | 0 | 8 | receive_suite -> truncation_respects_complete_vectors_and_pdu_end  |
| periodic-interval | 0 | 8 | integration_suite -> periodic_is_one_second_independent_of_join_time ; transmit_suite -> receive_redeclare_requests_transmission_without_periodic_wait  |
| periodic-passive | 0 | 8 | integration_suite -> applicant_declaration_recovery_and_withdrawal_follow_the_table  |
| point-to-point-condition | 0 | 8 | integration_suite -> applicant_receive_conditions_follow_link_mode  |
| receive-interest | 0 | 8 | receive_suite -> uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed  |
| receive-opportunity | 0 | 8 | transmit_suite -> receive_redeclare_requests_transmission_without_periodic_wait  |
| received-withdrawal-value | 0 | 8 | milan_suite -> disabled_application_option_preserves_ieee_timing ; milan_suite -> leave_in_lv_keeps_the_original_deadline ; milan_suite -> listener_leave_in_is_immediate ; milan_suite -> msrp_constructor_selects_the_build_profile ; receive_suite -> withdrawal_does_not_replace_the_registered_declaration  |
| reclaim | 0 | 8 | receive_suite -> uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed  |
| refused-storage | 0 | 8 | transmit_suite -> refused_pdu_survives_timers_without_aging_unsent_leaveall  |
| registrar-condition | 0 | 8 | transmit_suite -> fresh_ladder_and_refusal_are_transactional  |
| registrar-during-refusal | 0 | 8 | integration_suite -> registrar_ages_while_a_transmission_is_retained  |
| shared-in-condition | 0 | 8 | integration_suite -> applicant_receive_conditions_follow_link_mode  |
| split-fairness | 0 | 8 | transmit_suite -> a_full_pdu_retries_omitted_attributes_before_repeats  |
| talker-offset | 0 | 8 | msrp_values_suite -> domain_and_vector_offsets_match_wire_fields  |
| talker-replacement | 0 | 8 | receive_suite -> talker_join_replaces_the_other_type_on_the_same_port  |
| timer-unlink | 0 | 8 | timer_suite -> remove_head_middle_tail_and_reinitialize  |
| unknown-stream-message | 0 | 8 | integration_suite -> later_versions_skip_unknown_stream_messages  |
| wire-prevalidation | 0 | 8 | integration_suite -> a_malformed_later_message_has_no_earlier_indications ; receive_suite -> truncation_respects_complete_vectors_and_pdu_end  |
| withdrawal-transition | 0 | 8 | integration_suite -> applicant_declaration_recovery_and_withdrawal_follow_the_table  |
