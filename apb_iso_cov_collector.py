from apb_iso_pkg import *


class apb_iso_cov_collector(uvm_component):

    class uvm_AnalysisImp(uvm_analysis_export):
        def __init__(self, name, parent, write_fn):
            super().__init__(name, parent)
            self.write_fn = write_fn

        def write(self, tt):
            self.write_fn(tt)

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.analysis_export_master = self.uvm_AnalysisImp("analysis_export_master",
                                                    self,
                                                    self.write_master_cov)

        self.analysis_export_slave = self.uvm_AnalysisImp("analysis_export_slave",
                                            self,
                                            self.write_slave_cov)

        self.analysis_export_lpi = self.uvm_AnalysisImp("analysis_export_lpi",
                                            self,
                                            self.write_lpi_cov)

        self.analysis_export_dut_rst = self.uvm_AnalysisImp("analysis_export_dut_rst",
                                            self,
                                            self.write_dut_rst_cov)

        self.analysis_export_master_rst = self.uvm_AnalysisImp("analysis_export_master_rst",
                                            self,
                                            self.write_master_rst_cov)

        self.analysis_export_slave_rst = self.uvm_AnalysisImp("analysis_export_slave_rst",
                                            self,
                                            self.write_slave_rst_cov)
        
        self.ready = CocotbEvent()

    
    def write_master_cov(self, master_item):
        self.sample_mst_trn(self.lpi_state, master_item.direction, master_item.pslverr_enable,
        int(master_item.pstrb), master_item.pprot0, master_item.pprot1, master_item.pprot2)

    def write_slave_cov(self, slave_item):
        self.sample_slv_trn(self.lpi_state, slave_item.direction, slave_item.pslverr_enable,
        int(slave_item.pstrb), slave_item.pprot0, slave_item.pprot1, slave_item.pprot2)

    def write_lpi_cov(self, lpi_item):
        self.lpi_state = lpi_item.get_lpi_state()

    def write_dut_rst_cov(self, dut_rst_item):
        self.sample_rst_dut(dut_rst_item.rst_st.name)
        if dut_rst_item.rst_st == rst_state.RST_ASSERT:
            self.get_dut_rst = 1
            self.ready.set()
            self.ready.clear()

    def write_master_rst_cov(self, master_rst_item):
        self.sample_rst_mst(master_rst_item.rst_st.name)
        if master_rst_item.rst_st == rst_state.RST_ASSERT:
            self.get_master_rst = 1
            self.ready.set()
            self.ready.clear()

    def write_slave_rst_cov(self, slave_rst_item):
        self.sample_rst_slv(slave_rst_item.rst_st.name)
        if slave_rst_item.rst_st == rst_state.RST_ASSERT:
            self.get_slave_rst = 1
            self.ready.set()
            self.ready.clear()

    async def run_phase(self):
        self.lpi_state = lpi_q_state_e.Q_STOPPED
        while True:
            await self.ready.wait()
            await cocotb.triggers.Timer(1.0, "ns")
            if (self.get_master_rst == 1 and self.get_slave_rst == 1 and self.get_dut_rst == 1):
                get_all_reset = 1
                self.general_rst_on_all_components_cg_sample(get_all_reset, self.lpi_state)
                self.get_master_rst = 0
                self.get_slave_rst = 0
                self.get_dut_rst = 0

    def final_phase(self):
        coverage_db.report_coverage(self.logger.info, bins=True)
        coverage_db.export_to_xml(filename="coverage.xml")
        coverage_db.export_to_yaml(filename="coverage.yml")

    @CoverPoint("apb_iso_top.apb_master.lpi_state.qstate_cp",
        xf = lambda x, y, z, a, b, c, d : x,
        bins = [lpi_q_state_e.Q_RUN.name, lpi_q_state_e.Q_REQUEST.name, lpi_q_state_e.Q_STOPPED.name, lpi_q_state_e.Q_EXIT.name])
    @CoverPoint("apb_iso_top.apb_master.direction", 
        xf = lambda x, y, z, a, b, c, d : y,
        bins = [0, 1],
        bins_labels = ["READ", "WRITE"])
    @CoverPoint("apb_iso_top.apb_master.responce", 
        xf = lambda x, y, z, a, b, c, d : z,
        bins = [0, 1],
        bins_labels = ["OKAY", "ERROR"])
    @CoverPoint("apb_iso_top.apb_master.pstrb",
        xf = lambda x, y, z, a, b, c, d :a,
        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    @CoverPoint("apb_iso_top.apb_master.pprot0", 
        xf = lambda x, y, z, a, b, c, d :b,
        bins = [apb_pprot0.NORMAL.name, apb_pprot0.PRIVILEGED.name])
    @CoverPoint("apb_iso_top.apb_master.pprot1", 
        xf = lambda x, y, z, a, b, c, d :c,
        bins = [apb_pprot1.SECURE.name, apb_pprot1.NON_SECURE.name])
    @CoverPoint("apb_iso_top.apb_master.pprot2", 
        xf = lambda x, y, z, a, b, c, d :d,
        bins = [apb_pprot2.DATA.name, apb_pprot2.INSTRUCTION.name])         
    @CoverCross("apb_iso_top.apb_master.qstate_cp_X_status_tr_cp",
        items = ["apb_iso_top.apb_master.lpi_state.qstate_cp", "apb_iso_top.apb_master.direction"])
    def sample_mst_trn(self, x, y, z, a, b, c, d):
        pass

    @CoverPoint("apb_iso_top.apb_slave.lpi_state.qstate_cp",
        xf = lambda x, y, z, a, b, c, d : x,
        bins = [lpi_q_state_e.Q_RUN.name, lpi_q_state_e.Q_REQUEST.name, lpi_q_state_e.Q_STOPPED.name, lpi_q_state_e.Q_EXIT.name])
    @CoverPoint("apb_iso_top.apb_slave.direction", 
        xf = lambda x, y, z, a, b, c, d : y,
        bins = [0, 1],
        bins_labels = ["READ", "WRITE"])
    @CoverPoint("apb_iso_top.apb_slave.responce", 
        xf = lambda x, y, z, a, b, c, d : z,
        bins = [0, 1],
        bins_labels = ["OKAY", "ERROR"])
    @CoverPoint("apb_iso_top.apb_slave.pstrb",
        xf = lambda x, y, z, a, b, c, d :a,
        bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    @CoverPoint("apb_iso_top.apb_slave.pprot0", 
        xf = lambda x, y, z, a, b, c, d :b,
        bins = [apb_pprot0.NORMAL.name, apb_pprot0.PRIVILEGED.name])
    @CoverPoint("apb_iso_top.apb_slave.pprot1", 
        xf = lambda x, y, z, a, b, c, d :c,
        bins = [apb_pprot1.SECURE.name, apb_pprot1.NON_SECURE.name])
    @CoverPoint("apb_iso_top.apb_slave.pprot2", 
        xf = lambda x, y, z, a, b, c, d :d,
        bins = [apb_pprot2.DATA.name, apb_pprot2.INSTRUCTION.name])         
    @CoverCross("apb_iso_top.apb_slave.qstate_cp_X_status_tr_cp",
        items = ["apb_iso_top.apb_slave.lpi_state.qstate_cp", "apb_iso_top.apb_master.direction"])
    def sample_slv_trn(self, x, y, z, a, b, c, d):
        pass

    @CoverPoint("apb_iso_top.reset_dut", bins = [rst_state.RST_ASSERT.name, rst_state.RST_DEASSERT.name])
    def sample_rst_dut(self, a):
        pass

    @CoverPoint("apb_iso_top.reset_mst", bins = [rst_state.RST_ASSERT.name, rst_state.RST_DEASSERT.name])
    def sample_rst_mst(self, a):
        pass

    @CoverPoint("apb_iso_top.reset_slv", bins = [rst_state.RST_ASSERT.name, rst_state.RST_DEASSERT.name])
    def sample_rst_slv(self, a):
        pass

    @CoverPoint("apb_iso_top.covercross.get_all_reset",
        xf = lambda x, y: x,
        bins = [1],
        bins_labels  = ["ALL_RESET"]
    )
    @CoverPoint("apb_iso_top.covercross.lpi_state",
        xf = lambda x, y: y,
        bins = [lpi_q_state_e.Q_RUN.name, lpi_q_state_e.Q_REQUEST.name, lpi_q_state_e.Q_STOPPED.name, lpi_q_state_e.Q_EXIT.name]
    )

    @CoverCross(
        name = "apb_iso_top.covercross.get_all_reset_lpi_state",
        items = ["apb_iso_top.covercross.get_all_reset", "apb_iso_top.covercross.lpi_state"]
    )
    def general_rst_on_all_components_cg_sample (self, get_all_reset, lpi_state):
        pass
