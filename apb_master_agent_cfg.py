from apb_iso_pkg import * 
class apb_master_agent_cfg(uvm_object):
    def __init__(self, name):
        super().__init__(name)
        self.is_active = 0
        self.has_cov = 0
        self.fix_pready_timeout = 10
        self.print_debug_info = 0 #ToDo
