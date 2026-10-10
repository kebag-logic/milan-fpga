# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Planted defects of the SRP adapter's publication writers (#665 lane F-INT).

srp_mutants.py plants them with the rest of its table: each must fail its
named observable, never only a build. Each writer of the publication block
has a publish moved after what promises the value, a wrong field and a
skipped publish.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")

#: reset_interface's closure of every licence on the datapath, then the
#: revocations it reports (the publication block, lane F-INT).
REVOCATIONS_PUBLISHED = ('    publish_licence(i);\n    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {\n'
                         '        if (revoked[k]) {\n            ++m->stops;\n'
                         '            m->config.licence(m->config.ctx,i->index,k,false);\n        }\n    }\n')
DECLARE_SOURCES = 'static bool declare_sources(struct srp_interface *i)\n{'
SEND_COMMITTED = '    m->owed_len = 0;\n    ++m->transmitted;\n    return 0;\n}'

#: What a held-back publish keeps until it is let go: the slope or the set of
#: declared sources declare_sources computed, by the name of its storage.
KEPT = {"slope": ("planted_slope", "(uint32_t)used"), "declared": ("planted_declared", "declared")}


def defects(kind: Callable[..., T]) -> tuple[T, ...]:
    """Every publication defect, built with srp_mutants.Defect."""

    def held_back(name: str, test: str, site: str, publish: str, needle: str, keep: str = "") -> T:
        """The publish at `site` moved after the response: it is held back until
        send_pdu has committed the interface's next MSRP frame, the frame that
        carries what the value promises. A held slope or set of declared sources
        keeps the value it had."""
        late = (f'    if (s->app == s->interface->msrp && planted_held[s->interface->index]) {{\n'
                f'        planted_held[s->interface->index] = false;\n        {publish}\n    }}\n')
        held = f' {KEPT[keep][0]}[i->index] = {KEPT[keep][1]};' if keep else ''
        store = f'static uint32_t {KEPT[keep][0]}[MBX_N_IF];\n' if keep else ''
        return kind(name, test, site, f'    planted_held[i->index] = true;{held}\n', needle,
                    also=((DECLARE_SOURCES, f'static bool planted_held[MBX_N_IF];\n{store}\n{DECLARE_SOURCES}'),
                          (SEND_COMMITTED, SEND_COMMITTED.replace('    return 0;\n', late + '    return 0;\n'))))

    return _licence_domain_slope(kind, held_back) + _declarations(kind, held_back)


def _licence_domain_slope(Defect: Callable[..., T], held_back: Callable[..., T]) -> tuple[T, ...]:
    """Round 2 (#665, comment 6088423771): LICENCE, SR_DOMAIN, IDLE_SLOPE and the poll's terms."""
    return (
        # lane F-INT: the publication block (#665, comment 6088423771). The licence
        # published after its report, skipped and on the wrong bit, and after the
        # revocations of a reset; destroy's closure skipped; the Domain and the
        # slope skipped, wrong, or held back until the first MSRP frame carrying
        # them has left; the bounds' publication terms understated.
        Defect('pub-licence-after-the-report','PubLicenceIsSetAndClearedBeforeEachChangeIsReported',
               '                publish_licence(i);\n                m->config.licence(m->config.ctx,n,s,active);',
               '                m->config.licence(m->config.ctx,n,s,active);\n                publish_licence(i);',
               "PUB LICENCE holds source 0's bit before the licence is reported"),
        Defect('pub-licence-skipped','PubLicenceIsSetAndClearedBeforeEachChangeIsReported',
               '                publish_licence(i);\n                m->config.licence(m->config.ctx,n,s,active);',
               '                m->config.licence(m->config.ctx,n,s,active);',
               "PUB LICENCE holds source 0's bit before the licence is reported"),
        Defect('pub-licence-wrong-bit','PubLicenceIsSetAndClearedBeforeEachChangeIsReported',
               'active |= (i->active[k] ? 1u : 0u) << k;', 'active |= (i->active[k] ? 1u : 0u) << (k + 1u);',
               "PUB LICENCE holds source 0's bit before the licence is reported"),
        Defect('pub-licence-after-the-revocations','PubLicenceIsSetAndClearedBeforeEachChangeIsReported',
               REVOCATIONS_PUBLISHED,
               REVOCATIONS_PUBLISHED.removeprefix('    publish_licence(i);\n') + '    publish_licence(i);\n',
               'PUB a link loss clears LICENCE before the revocation is reported'),
        Defect('pub-licence-kept-at-destroy','PubLicenceIsSetAndClearedBeforeEachChangeIsReported',
               '        (void)mbx_pub_licence(n,0u);\n', '',
               'PUB destroy clears LICENCE before any revocation is reported'),
        Defect('pub-domain-adoption-skipped','PubDomainPrecedesEveryDeclarationThatCarriesIt',
               '    (void)mbx_pub_domain(i->index,true,i->domain.priority,i->domain.vid);\n', '',
               'PUB an MRPDU carrying the adopted Domain or its VID left after SR_DOMAIN published it'),
        Defect('pub-domain-priority-for-vid','PubDomainPrecedesEveryDeclarationThatCarriesIt',
               '(void)mbx_pub_domain(i->index,true,i->domain.priority,i->domain.vid);',
               '(void)mbx_pub_domain(i->index,true,(uint8_t)i->domain.vid,i->domain.priority);',
               'PUB an MRPDU carrying the adopted Domain or its VID left after SR_DOMAIN published it'),
        Defect('pub-domain-default-skipped','PubDomainPrecedesEveryDeclarationThatCarriesIt',
               '    (void)mbx_pub_domain(i->index,false,i->domain.priority,i->domain.vid);\n', '',
               'PUB after a link restart, the default Domain is published before it is declared again'),
        Defect('pub-domain-default-marked-adopted','PubDomainPrecedesEveryDeclarationThatCarriesIt',
               '(void)mbx_pub_domain(i->index,false,i->domain.priority,i->domain.vid);',
               '(void)mbx_pub_domain(i->index,true,i->domain.priority,i->domain.vid);',
               'PUB the default Domain {priority 3, VID 2}, not adopted, from startup'),
        Defect('pub-slope-skipped','PubIdleSlopeIsPublishedBeforeTheDeclarationsItAdmits',
               '    (void)mbx_pub_idle_slope(i->index,(uint32_t)used);\n', '',
               'PUB every MRPDU of the restarted interface left with IDLE_SLOPE published again'),
        Defect('pub-slope-halved','PubIdleSlopeIsPublishedBeforeTheDeclarationsItAdmits',
               '(void)mbx_pub_idle_slope(i->index,(uint32_t)used);',
               '(void)mbx_pub_idle_slope(i->index,(uint32_t)(used / 2u));',
               'PUB IDLE_SLOPE is the admitted bandwidth from startup'),
        held_back('pub-domain-adoption-after-the-declarations','PubDomainPrecedesEveryDeclarationThatCarriesIt',
                  '    (void)mbx_pub_domain(i->index,true,i->domain.priority,i->domain.vid);\n',
                  '(void)mbx_pub_domain(s->interface->index,true,s->interface->domain.priority,'
                  's->interface->domain.vid);',
                  'PUB an MRPDU carrying the adopted Domain or its VID left after SR_DOMAIN published it'),
        held_back('pub-domain-default-after-the-declarations','PubDomainPrecedesEveryDeclarationThatCarriesIt',
                  '    (void)mbx_pub_domain(i->index,false,i->domain.priority,i->domain.vid);\n',
                  '(void)mbx_pub_domain(s->interface->index,false,s->interface->domain.priority,'
                  's->interface->domain.vid);',
                  'PUB after a link restart, the default Domain is published before it is declared again'),
        held_back('pub-slope-after-the-declarations','PubIdleSlopeIsPublishedBeforeTheDeclarationsItAdmits',
                  '    (void)mbx_pub_idle_slope(i->index,(uint32_t)used);\n',
                  '(void)mbx_pub_idle_slope(s->interface->index,planted_slope[s->interface->index]);',
                  'PUB every MRPDU of the restarted interface left with IDLE_SLOPE published again', keep='slope'),
        Defect('pub-term-poll-understated','PollPublicationTermIsMeasuredThroughRealCallbacks',
               '#define SRP_MBX_PUB_POLL_MAX (SRP_MBX_PUB_RESET + 3u + 2u * MBX_N_PUB_SOURCES)',
               '#define SRP_MBX_PUB_POLL_MAX (SRP_MBX_PUB_RESET + 3u)',
               "the poll's publication term funds a reset, an adoption and two changes per source",
               path='srp/srp_bounds.h', suite='srp_app.cpp'),
        Defect('pub-term-reset-understated','PollPublicationTermIsMeasuredThroughRealCallbacks',
               '#define SRP_MBX_PUB_RESET 5u', '#define SRP_MBX_PUB_RESET 4u',
               'a reset publishes LICENCE and TALKER_DECL, then SR_DOMAIN, IDLE_SLOPE and TALKER_DECL, once each',
               path='srp/srp_bounds.h', suite='srp_app.cpp'),
    )


def _declarations(Defect: Callable[..., T], held_back: Callable[..., T]) -> tuple[T, ...]:
    """Round 3 (#665, comment 6092086337): TALKER_DECL."""
    return (
        # round 3 (#665, comment 6092086337): TALKER_DECL, set before the
        # declarations it describes leave and withdrawn before their participants
        # are destroyed. Set: skipped, on the wrong register or bit, held back
        # until the first MSRP frame has left. Withdrawn: skipped at a reset and at
        # destroy, and moved after the reset's new declarations.
        Defect('pub-declared-skipped','PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst',
               '    (void)mbx_pub_talker_decl(i->index,declared);\n', '    (void)declared;\n',
               'PUB TALKER_DECL holds every declared source from startup'),
        Defect('pub-declared-in-the-licence','PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst',
               '(void)mbx_pub_talker_decl(i->index,declared);', '(void)mbx_pub_licence(i->index,declared);',
               'PUB TALKER_DECL holds every declared source from startup'),
        Defect('pub-declared-wrong-bit','PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst',
               '        declared |= 1u << n;', '        declared |= 1u << (n + 1u);',
               'PUB TALKER_DECL holds every declared source from startup'),
        held_back('pub-declared-after-the-declarations','PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst',
                  '    (void)mbx_pub_talker_decl(i->index,declared);\n',
                  '(void)mbx_pub_talker_decl(s->interface->index,planted_declared[s->interface->index]);',
                  'PUB every MRPDU carrying a Talker declaration left with TALKER_DECL published again', keep='declared'),
        Defect('pub-declared-kept-at-reset','PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst',
               '    withdraw_declared(i->index);\n', '',
               'PUB a link restart withdraws TALKER_DECL before the new participants declare'),
        Defect('pub-declared-withdrawn-after-the-new-declarations',
               'PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst',
               '    withdraw_declared(i->index);\n', '',
               'PUB a link restart withdraws TALKER_DECL before the new participants declare',
               also=(('    if (!open_interface(i)) {\n        ++m->refused;\n    }\n}\n\nstatic void on_event(',
                      '    if (!open_interface(i)) {\n        ++m->refused;\n    }\n    withdraw_declared(i->index);\n}'
                      '\n\nstatic void on_event('),)),
        Defect('pub-declared-kept-at-destroy','PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst',
               '        withdraw_declared(n);\n', '',
               'PUB destroy withdraws every declaration from the datapath'),
    )
