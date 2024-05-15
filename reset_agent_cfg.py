from apb_iso_pkg import *
class reset_agent_cfg (uvm_object):
    def __init__(self, name):
        super().__init__(name)
        self.active_level = 0
        self.is_active = 0
