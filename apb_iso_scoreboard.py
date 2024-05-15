from apb_iso_pkg import *
class apb_iso_scoreboard (uvm_component):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.passed = None
        self.apb_slv_trn = None

    def build_phase(self):
        self.dut_fifo_reset = uvm_tlm_analysis_fifo("dut_fifo_reset", self)
        self.slv_fifo_reset = uvm_tlm_analysis_fifo("slv_fifo_reset", self)
        self.mst_fifo_reset = uvm_tlm_analysis_fifo("mst_fifo_reset", self)
        self.mst_fifo_trans = uvm_tlm_analysis_fifo("mst_fifo_trans", self)
        self.slv_fifo_trans = uvm_tlm_analysis_fifo("slv_fifo_trans", self)
        self.lpi_fifo_trans = uvm_tlm_analysis_fifo("lpi_fifo_trans", self)

    async def get_lpi_trn(self):
        while True:
            self.lpi_trn  = await self.lpi_fifo_trans.get()
            
    async def get_apb_slv_trn(self):
        while True:
            self.apb_slv_trn  = await self.slv_fifo_trans.get()
            self.logger.debug(f"Get apb-slv trans{self.apb_slv_trn}")
            self.got_slv_trn_flag = 1

    async def get_rst_dut_trn(self):
        while True:
            self.rst_dut_trn  = await self.dut_fifo_reset.get()
    
    async def get_rst_slv_trn(self):
        while True:
            self.rst_slv_trn  = await self.slv_fifo_reset.get()

    async def check_trn(self, mst_trn, slv_trn):
        if (self.lpi_trn.state_resp == lpi_q_resp_e.IDLE):
            if (self.got_slv_trn_flag == 0 and self.rst_slv_trn.rst_st != rst_state.RST_ASSERT):
                self.logger.error(f"Slave transaction was skipped")
                raise RuntimeError(f"{self.get_full_name()} : Slave transaction was skipped")
            self.got_slv_trn_flag = 0
            if (slv_trn.curr_state != apb_state.ABORTED.name):
                if (mst_trn != slv_trn):
                    self.logger.error(f"slave and master transactions are different")
                    raise RuntimeError(f"{self.get_full_name()} : slave and master transactions are different")
        elif (self.lpi_trn.state_resp == lpi_q_resp_e.ACCEPT and mst_trn.curr_state != apb_state.ABORTED.name):
            if (self.got_slv_trn_flag == 1):
                self.logger.error(f"Extra slave transaction was received")
                raise RuntimeError(f"Extra slave transaction was received")
            if (mst_trn.pslverr_enable != 1):
                self.logger.error(f"The interface was not isolated")
                raise RuntimeError(f"The interface was not isolated")

    async def run_phase (self):
        self.got_slv_trn_flag = 0
        t1 = cocotb.start_soon(self.get_apb_slv_trn())
        t2 = cocotb.start_soon(self.get_lpi_trn())
        t3 = cocotb.start_soon(self.get_rst_dut_trn())
        t4 = cocotb.start_soon(self.get_rst_slv_trn())
        cocotb.triggers.Combine(t1, t2, t3, t4)
        while True:
            self.apb_mst_trn = await self.mst_fifo_trans.get()
            self.logger.debug(f"Get apb-mst trans{self.apb_mst_trn}")
            await cocotb.triggers.Timer(1.0, "ns")
            await self.check_trn(self.apb_mst_trn, self.apb_slv_trn)
