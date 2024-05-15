from apb_iso_pkg import *

class reset_agent(uvm_agent):
    num_id = 0
    def __init__(self, name, parent, *args, **kwargs):
        reset_agent.num_id += 1
        self.num_id = reset_agent.num_id
        super().__init__(name, parent)


    def build_phase(self):
        self.cfg = ConfigDB().get(self, "", "cfg")
        if (self.cfg.is_active):
            self.reset_seqr = uvm_sequencer.create("reset_seqr", self)
            self.driver = reset_driver("reset_driver", self, num_id = self.num_id)
            self.driver.set_cfg(self.cfg)
        self.monitor = reset_monitor("reset_monitor", self, num_id = self.num_id)

    def connect_phase(self):
        if (self.cfg.is_active):
            self.driver.seq_item_port.connect(self.reset_seqr.seq_item_export)
