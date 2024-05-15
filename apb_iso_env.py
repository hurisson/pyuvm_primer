from apb_iso_pkg import *
class apb_iso_env (uvm_env):
    """Instantiate components"""
    def build_phase(self):
        
        self.apb_iso_env_cfg = ConfigDB().get(self, "", "apb_iso_env_cfg")
        
        if (self.apb_iso_env_cfg.has_scoreboard):
            self.scoreboard = apb_iso_scoreboard.create("apb_iso_scoreboard", self)
        
        if (self.apb_iso_env_cfg.has_cov):
            self.cov_collector = apb_iso_cov_collector.create("apb_iso_cov_collector", self)

        if (self.apb_iso_env_cfg.has_dut_reset_master_agent):
            self.dut_reset_agent = reset_agent.create("dut_reset_agent", self)
            ConfigDB().set(self, "dut_reset_agent", "cfg", self.apb_iso_env_cfg.dut_reset_agent_cfg)

        if (self.apb_iso_env_cfg.has_slv_reset_master_agent):
            self.slv_reset_agent = reset_agent.create("slv_reset_agent", self)
            ConfigDB().set(self, "slv_reset_agent", "cfg", self.apb_iso_env_cfg.slv_reset_agent_cfg)
            
        if (self.apb_iso_env_cfg.has_mst_reset_master_agent):
            self.mst_reset_agent = reset_agent.create("mst_reset_agent", self)
            ConfigDB().set(self, "mst_reset_agent", "cfg", self.apb_iso_env_cfg.mst_reset_agent_cfg)

        if (self.apb_iso_env_cfg.has_lpi_master_agent):
            self.lpi_master_agent = lpi_master_agent.create("lpi_master_agent", self)
            ConfigDB().set(self, "lpi_master_agent", "cfg", self.apb_iso_env_cfg.lpi_master_agent_cfg)

        if (self.apb_iso_env_cfg.has_master_apb_agent):
            self.apb_master_agent = apb_master_agent.create("apb_master_agent", self)
            ConfigDB().set(self, "apb_master_agent", "cfg", self.apb_iso_env_cfg.apb_master_agent_cfg)

        if (self.apb_iso_env_cfg.has_slave_apb_agent):
            self.apb_slave_agent = apb_slave_agent.create("apb_slave_agent", self)
            ConfigDB().set(self, "apb_slave_agent", "cfg", self.apb_iso_env_cfg.apb_slave_agent_cfg)

    def connect_phase(self):
        if (self.apb_iso_env_cfg.has_scoreboard):

            if (self.apb_iso_env_cfg.has_dut_reset_master_agent):
                self.dut_reset_agent.monitor.ap.connect(self.scoreboard.dut_fifo_reset.analysis_export)

            if (self.apb_iso_env_cfg.has_slv_reset_master_agent):
                self.slv_reset_agent.monitor.ap.connect(self.scoreboard.slv_fifo_reset.analysis_export)

            if (self.apb_iso_env_cfg.has_mst_reset_master_agent):
                self.mst_reset_agent.monitor.ap.connect(self.scoreboard.mst_fifo_reset.analysis_export)

            if (self.apb_iso_env_cfg.has_lpi_master_agent):
                self.lpi_master_agent.monitor.ap.connect(self.scoreboard.lpi_fifo_trans.analysis_export)

            if (self.apb_iso_env_cfg.has_master_apb_agent):
                self.apb_master_agent.monitor.ap.connect(self.scoreboard.mst_fifo_trans.analysis_export)

            if (self.apb_iso_env_cfg.has_slave_apb_agent):
                self.apb_slave_agent.monitor.ap.connect(self.scoreboard.slv_fifo_trans.analysis_export)

        if (self.apb_iso_env_cfg.has_cov):
            if (self.apb_iso_env_cfg.has_dut_reset_master_agent):
                self.dut_reset_agent.monitor.ap.connect(self.cov_collector.analysis_export_dut_rst)

            if (self.apb_iso_env_cfg.has_slv_reset_master_agent):
                self.slv_reset_agent.monitor.ap.connect(self.cov_collector.analysis_export_slave_rst)

            if (self.apb_iso_env_cfg.has_mst_reset_master_agent):
                self.mst_reset_agent.monitor.ap.connect(self.cov_collector.analysis_export_master_rst)

            if (self.apb_iso_env_cfg.has_lpi_master_agent):
                self.lpi_master_agent.monitor.ap.connect(self.cov_collector.analysis_export_lpi)
            
            if (self.apb_iso_env_cfg.has_master_apb_agent):
                self.apb_master_agent.monitor.ap.connect(self.cov_collector.analysis_export_master)

            if (self.apb_iso_env_cfg.has_slave_apb_agent):
                self.apb_slave_agent.monitor.ap.connect(self.cov_collector.analysis_export_slave)
