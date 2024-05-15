from apb_iso_pkg import *

class apb_iso_env_cfg (uvm_object):
    def __init__(self, name):
        super().__init__(name)
        self.has_scoreboard          = 1
        self.has_master_apb_agent    = 1
        self.has_slave_apb_agent     = 1
        self.has_lpi_master_agent    = 1
        self.has_reset_master_agent  = 1
        self.has_dut_reset_master_agent = 1
        self.has_slv_reset_master_agent = 1
        self.has_mst_reset_master_agent = 1
        self.is_active = 1
        try:
            self.has_cov = int(cocotb.plusargs["has_cov"])
        except KeyError:
            self.has_cov = 0

    def build(self):
        if (self.has_dut_reset_master_agent):
            self.build_dut_reset_agent_cfg()

        if (self.has_slv_reset_master_agent):
            self.build_slv_reset_agent_cfg()

        if (self.has_mst_reset_master_agent):
            self.build_mst_reset_agent_cfg()

        if (self.has_lpi_master_agent):
            self.build_lpi_master_agent_cfg()

        if (self.has_master_apb_agent):
            self.build_master_apb_agent_cfg()

        if (self.has_slave_apb_agent):
            self.build_slave_apb_agent_cfg()

    def build_dut_reset_agent_cfg(self):
        self.dut_reset_agent_cfg = reset_agent_cfg("dut_reset_agent_cfg")
        self.dut_reset_agent_cfg.active_level = reset_level.LOW_LEVEL
        self.dut_reset_agent_cfg.is_active = self.is_active

    def build_slv_reset_agent_cfg(self):
        self.slv_reset_agent_cfg = reset_agent_cfg("slv_reset_agent_cfg")
        self.slv_reset_agent_cfg.active_level  = reset_level.LOW_LEVEL
        self.slv_reset_agent_cfg.is_active  = self.is_active

    def build_mst_reset_agent_cfg(self):
        self.mst_reset_agent_cfg = reset_agent_cfg("mst_reset_agent_cfg")
        self.mst_reset_agent_cfg.active_level = reset_level.LOW_LEVEL
        self.mst_reset_agent_cfg.is_active = self.is_active

    def build_lpi_master_agent_cfg(self):
        self.lpi_master_agent_cfg = lpi_master_agent_cfg("lpi_master_agent_cfg")
        self.lpi_master_agent_cfg.is_active = self.is_active
        self.lpi_master_agent_cfg.randomize()
        with self.lpi_master_agent_cfg.randomize_with() as it:
            it.qreqn_state_during_rst == 0

    def build_master_apb_agent_cfg(self):
        self.apb_master_agent_cfg = apb_master_agent_cfg("apb_master_agent_cfg")
        self.apb_master_agent_cfg.is_active = self.is_active
        self.apb_master_agent_cfg.fix_pready_timeout = 10

    def build_slave_apb_agent_cfg(self):
        self.apb_slave_agent_cfg = apb_slave_agent_cfg("apb_slave_agent_cfg")
        self.apb_slave_agent_cfg.is_active = self.is_active
        self.apb_slave_agent_cfg.randomize()
