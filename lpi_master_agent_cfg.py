from apb_iso_pkg import *

@vsc.randobj
class lpi_master_agent_cfg (uvm_object):
    def __init__(self, name):
        super().__init__(name)
        self.is_active = 0
        self.print_debug_info = 0 #ToDo
        self.qreqn_state_during_rst = vsc.rand_bit_t()