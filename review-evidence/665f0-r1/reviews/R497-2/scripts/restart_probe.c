/* Review probe: public ADP API, no implementation edits. */
#define main repository_test_main
#include "test_adp.c"
#undef main

int main(void)
{
    struct adp a;
    /* Positive control: a deferred shutdown without restart is delivered. */
    fresh(&a, true);
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    fk.room = false;
    adp_set_enable(&a, false);
    fk.room = true;
    adp_poll(&a);
    check("control: deferred shutdown sends DEPARTING index 1", wire_is(ADP_MSG_ENTITY_DEPARTING, 1));

    fresh(&a, true);
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    printf("initial available: type=%u index=%u sends=%u\n", fk.last[15], wire_index(), fk.sends);
    fk.room = false;
    adp_set_enable(&a, false);
    printf("shutdown blocked: pending=%u saved_index=%u state=%u\n", a.pending, a.pending_index, a.state);
    check("shutdown owes DEPARTING", a.pending == ADP_PENDING_DEPARTING);
    adp_set_enable(&a, true);
    adp_timer_expired(&a);
    printf("restart expiry while blocked: pending=%u saved_index=%u state=%u\n", a.pending, a.pending_index, a.state);
    check("restart expiry preserves the owed DEPARTING", a.pending == ADP_PENDING_DEPARTING);
    fk.room = true;
    adp_poll(&a);
    printf("first successful send after recovery: type=%u index=%u sends=%u\n", fk.last[15], wire_index(), fk.sends);
    check("DEPARTING with the shutdown index precedes the restarted AVAILABLE", wire_is(ADP_MSG_ENTITY_DEPARTING, 1));

    /* Integration: a full ring, driver, event loop and real model timer. */
    boot();
    mbx_model_set_link(&model, 0, true);
    settle();
    to_waiting();
    check("integration setup: WAITING with current index 1", adp0()->state == ADP_STATE_WAITING && adp0()->available_index == 1);
    mbx_model_tx_pause(&model, true);
    uint8_t filler[ADP_FRAME_BYTES];
    adp_build(adp0(), ADP_MSG_ENTITY_AVAILABLE, 0x55, filler);
    while (mbx_tx_send(MBX_CH_ADP, 0, filler, sizeof filler) == MBX_STATUS_OK) {}
    adp_mbx_set_enable(&app.adp, false);
    check("integration: full ring leaves DEPARTING owed", adp0()->pending == ADP_PENDING_DEPARTING);
    adp_mbx_set_enable(&app.adp, true);
    uint32_t deadline = mbx_model_tmr_op(&model, model.tmr_ops - 1)->deadline_ms;
    mbx_model_advance_ms(&model, deadline - model.now_ms + 1);
    ctrl_loop_service(&app.loop);
    printf("model restart expiry: pending=%u saved_index=%u\n", adp0()->pending, adp0()->pending_index);
    mbx_model_tx_pause(&model, false);
    uint32_t drained = model.tx_sent;
    ctrl_loop_service(&app.loop);
    const struct mbx_model_tx *tx = mbx_model_tx_frame(&model, drained);
    printf("model first new frame after recovery: type=%u index=%u\n", tx ? tx->bytes[15] : 255, tx ? wire_be32(tx->bytes + 50) : 0);
    check("integration: pending DEPARTING index 1 survives restart and timer expiry", tx && tx->bytes[15] == ADP_MSG_ENTITY_DEPARTING && wire_be32(tx->bytes + 50) == 1);
    return check_report("restart while DEPARTING is owed");
}
