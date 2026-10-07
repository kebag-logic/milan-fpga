/* SPDX-License-Identifier: Apache-2.0 */
/* Probe: a consumer of the switch interface linked only against the
 * embedded module source list from the root build definition. */
#include "shish_lan/switch.h"
static int connect_op(struct shlan_switch *sw) { (void)sw; return 0; }
static void disconnect_op(struct shlan_switch *sw) { (void)sw; }
static int port_op(struct shlan_switch *sw, uint8_t port) { (void)sw; (void)port; return 0; }
int main(void)
{
    static const struct shlan_switch_ops ops = {
        .connect = connect_op, .disconnect = disconnect_op,
        .port_enable = port_op, .port_disable = port_op,
    };
    struct shlan_switch sw = {.ops = &ops};
    int r = shlan_connect(&sw) | shlan_port_enable(&sw, 0) | shlan_port_disable(&sw, 0);
    shlan_disconnect(&sw);
    return r;
}
