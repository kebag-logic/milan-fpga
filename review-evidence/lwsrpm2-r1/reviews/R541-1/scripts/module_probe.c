/* SPDX-License-Identifier: Apache-2.0 */
#include "shish_lan/switch.h"
static int connect_port(struct shlan_switch *sw) { (void)sw; return 0; }
static void disconnect_port(struct shlan_switch *sw) { (void)sw; }
static int set_port(struct shlan_switch *sw, uint8_t p) { (void)sw; (void)p; return 0; }
int main(void) {
    const struct shlan_switch_ops ops = {connect_port, disconnect_port, set_port, set_port};
    struct shlan_switch sw = {&ops, 0};
    int result = shlan_connect(&sw);
    result |= shlan_port_enable(&sw, 0);
    result |= shlan_port_disable(&sw, 0);
    shlan_disconnect(&sw);
    return result;
}
