from apb_iso_pkg import * 
class apb_master_agent(uvm_agent):
    num_id = 0
    def __init__(self, name, parent, *args, **kwargs):
        apb_master_agent.num_id += 1
        self.num_id = apb_master_agent.num_id
        super().__init__(name, parent)

    def build_phase(self):
        self.cfg = ConfigDB().get(self, "", "cfg")
        if (self.cfg.is_active):
            self.apb_master_seqr = uvm_sequencer("apb_master_seqr", self)
            self.driver = apb_master_driver("apb_master_driver", self, num_id = self.num_id)
        self.monitor = apb_monitor("apb_monitor", self, is_master = 1, num_id = self.num_id)
        self.monitor.set_cfg(self.cfg)

    def connect_phase(self):
        if (self.cfg.is_active):
            self.driver.seq_item_port.connect(self.apb_master_seqr.seq_item_export)
