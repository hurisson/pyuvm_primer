from apb_iso_pkg import * 

class lpi_master_agent(uvm_agent):
    num_id = 0
    def __init__(self, name, parent, *args, **kwargs):
        lpi_master_agent.num_id +=1
        self.num_id = lpi_master_agent.num_id
        super().__init__(name, parent)

    def build_phase(self):
        super().build_phase()
        self.cfg = ConfigDB().get(self, "", "cfg")
        if (self.cfg.is_active):
            self.sequencer = uvm_sequencer("lpi_master_seqr", self)
            self.driver = lpi_master_driver("lpi_master_driver", self, num_id = self.num_id)
            self.driver.set_cfg(self.cfg)
        self.monitor = lpi_monitor("lpi_monitor", self, num_id = self.num_id)
        self.monitor.set_cfg(self.cfg)

    def connect_phase(self):
        if (self.cfg.is_active):
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export)
