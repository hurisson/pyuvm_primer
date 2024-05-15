from apb_iso_pkg import * 
class apb_slave_agent(uvm_agent):
    num_id = 0
    def __init__(self, name, parent, *args, **kwargs):
        apb_slave_agent.num_id += 1
        self.num_id = apb_slave_agent.num_id
        super().__init__(name, parent)

    def build_phase(self):
        self.cfg = ConfigDB().get(self, "", "cfg")
        if (self.cfg.is_active):
            self.apb_slave_sequencer = apb_slave_sequencer("apb_slave_sequencer", self)
            self.driver = apb_slave_driver("apb_slave_driver", self, num_id = self.num_id)
            self.driver.set_cfg(self.cfg)
            self.fifo = uvm_tlm_fifo("fifo", self)
        self.monitor = apb_monitor("apb_monitor", self, is_master = 0, num_id = self.num_id)
        self.monitor.set_cfg(self.cfg)
        
    def connect_phase(self):
        if (self.cfg.is_active):
            self.driver.seq_item_port.connect(self.apb_slave_sequencer.seq_item_export)
            self.apb_slave_sequencer.mon_trans_port_get.connect(self.fifo.get_export)
            self.monitor.mon_trans_port_put.connect(self.fifo.put_export)
