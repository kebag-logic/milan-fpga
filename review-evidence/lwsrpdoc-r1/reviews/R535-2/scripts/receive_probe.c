#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "shish_lan/msrp.h"

static enum mrp_reg_state talker_reg;
static enum mrp_appl_state talker_appl;
static void visit(void *ctx, const struct mrp_attr_status *status)
{
    (void)ctx;
    if (status->attr_type == MSRP_ATTR_TYPE_TALKER_ADV) {
        talker_reg = status->reg;
        talker_appl = status->appl;
    }
}

int main(void)
{
    struct msrp_ctx context = {0};
    struct mrp_app *app = msrp_app_create(1, &context);
    assert(app);
    const unsigned char expected[] = {0x91,0xe0,0xf0,0,0x0e,0x80};
    assert(memcmp(app->ops->group_addr, expected, 6) == 0);
    printf("Observed MSRP address: %02X-%02X-%02X-%02X-%02X-%02X\n",
           app->ops->group_addr[0], app->ops->group_addr[1],app->ops->group_addr[2],
           app->ops->group_addr[3],app->ops->group_addr[4],app->ops->group_addr[5]);
    struct msrp_talker_adv talker = {0};
    talker.stream_id.bytes[7] = 1;
    assert(msrp_declare_talker(app, 0, &talker, true) == 0);
    assert(mrp_attr_visit(app, 0, visit, NULL) == 1);
    assert(talker_reg == MRP_REG_STATE_IN);
    printf("Talker before Listener LeaveAll: Applicant=%s Registrar=%s\n",
           mrp_appl_state_name(talker_appl),mrp_reg_state_name(talker_reg));
    /* Listener message, eight-byte FirstValue, LeaveAll, zero values, two end marks. */
    const unsigned char payload[] = {0,3,8,0,12,0x20,0,0,0,0,0,0,0,0,0,0,0,0,0};
    assert(mrp_rx(app, 0, payload, sizeof(payload)) == 0);
    assert(mrp_attr_visit(app, 0, visit, NULL) == 1);
    printf("Talker after Listener LeaveAll: Applicant=%s Registrar=%s\n",
           mrp_appl_state_name(talker_appl),mrp_reg_state_name(talker_reg));
    assert(talker_reg == MRP_REG_STATE_LV);
    puts("PASS: documented address and cross-type delivery reproduced.");
    /* No further timer operations after destruction. */
    msrp_app_destroy(app);
    return 0;
}
