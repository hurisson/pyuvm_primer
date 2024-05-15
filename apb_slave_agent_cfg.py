from apb_iso_pkg import * 
@vsc.randobj
class apb_slave_agent_cfg(uvm_object):
    def __init__(self, name):
        super().__init__(name)
        self.is_active = 0
        self.has_cov = 0
        self.pready_default = vsc.rand_bit_t()
        self.print_debug_info = 0 #ToDo
