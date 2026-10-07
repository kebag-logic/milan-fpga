# SPDX-License-Identifier: Apache-2.0
"""Probe exported wrappers against a deliberately distinct vtable and real adapter.
Usage: python3 binding_probe.py PATH_TO_LIBSHLAN
"""
import ctypes as c
import sys

class Switch(c.Structure):
    pass
Pointer = c.POINTER(Switch)
Connect = c.CFUNCTYPE(c.c_int, Pointer)
Disconnect = c.CFUNCTYPE(None, Pointer)
Port = c.CFUNCTYPE(c.c_int, Pointer, c.c_uint8)
class Ops(c.Structure):
    _fields_ = [("connect", Connect), ("disconnect", Disconnect),
                ("port_enable", Port), ("port_disable", Port)]
Switch._fields_ = [("ops", c.POINTER(Ops)), ("priv", c.c_void_p)]
events = []
def on_connect(pointer):
    events.append(("connect", c.addressof(pointer.contents)))
    return -12345
def on_disconnect(pointer):
    events.append(("disconnect", c.addressof(pointer.contents)))
def on_enable(pointer, port):
    events.append(("enable", c.addressof(pointer.contents), port))
    return 1000 + port
def on_disable(pointer, port):
    events.append(("disable", c.addressof(pointer.contents), port))
    return -1000 - port
ops = Ops(Connect(on_connect), Disconnect(on_disconnect), Port(on_enable), Port(on_disable))
switch = Switch(c.pointer(ops), None)
pointer = c.pointer(switch)
address = c.addressof(switch)
lib = c.CDLL(sys.argv[1])
for name, restype, argtypes in [
    ("connect", c.c_int, [Pointer]), ("disconnect", None, [Pointer]),
    ("port_enable", c.c_int, [Pointer, c.c_uint8]), ("port_disable", c.c_int, [Pointer, c.c_uint8])]:
    function = getattr(lib, "shlan_test_" + name)
    function.restype = restype
    function.argtypes = argtypes
assert lib.shlan_test_connect(pointer) == -12345
assert events.pop() == ("connect", address)
for port in range(256):
    assert lib.shlan_test_port_enable(pointer, port) == 1000 + port
    assert events.pop() == ("enable", address, port)
    assert lib.shlan_test_port_disable(pointer, port) == -1000 - port
    assert events.pop() == ("disable", address, port)
assert lib.shlan_test_disconnect(pointer) is None
assert events.pop() == ("disconnect", address)
assert events == []
print("PASS: four wrappers dispatch the correct vtable member and preserve pointer and return value.")
print("PASS: both port wrappers preserve every uint8_t value (0 through 255).")
lib.shlan_sim_adapter_create.restype = Pointer
lib.shlan_sim_adapter_create.argtypes = []
lib.shlan_sim_adapter_destroy.restype = None
lib.shlan_sim_adapter_destroy.argtypes = [Pointer]
for iteration in range(100):
    switch = lib.shlan_sim_adapter_create()
    assert switch
    assert lib.shlan_test_connect(switch) == 0
    for port in (0, 47, 48, 255):
        expected = 0 if port < 48 else -1
        assert lib.shlan_test_port_enable(switch, port) == expected
        assert lib.shlan_test_port_disable(switch, port) == expected
    lib.shlan_test_disconnect(switch)
    lib.shlan_sim_adapter_destroy(switch)
print("PASS: 100 real-adapter create/connect/port-boundary/disconnect/destroy cycles.")
