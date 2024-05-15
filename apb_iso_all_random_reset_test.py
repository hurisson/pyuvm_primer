from apb_iso_pkg import *


@test()
class apb_iso_all_random_reset_test(apb_iso_base_test):

    async def all_reset(self):
        rst_task_dut = cocotb.start_soon(reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 20, clk_cycles_after = 20).start(self.env.dut_reset_agent.reset_seqr))
        rst_task_mst = cocotb.start_soon(reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 20, clk_cycles_after = 20).start(self.env.mst_reset_agent.reset_seqr))
        rst_task_slv = cocotb.start_soon(reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 20, clk_cycles_after = 20).start(self.env.slv_reset_agent.reset_seqr))
        await cocotb.triggers.Combine(rst_task_dut, rst_task_mst, rst_task_slv)

    async def reset_action(self):
        while True:
            await self.reset_seq.start(self.env.mst_reset_agent.reset_seqr)

    async def apb_mst_trn_task(self, min_delay_trn, max_delay_trn):
        while True:    
            wdt_delay = random.randint(min_delay_trn, max_delay_trn)
            await cocotb.triggers.Timer(wdt_delay, "ns")
            await cocotb.start_soon(apb_master_random_sequence("apb_master_stimulus").start(self.env.apb_master_agent.apb_master_seqr))

    async def lpi_trn_task_after_reset(self):
        await cocotb.triggers.Combine(cocotb.triggers.RisingEdge(cocotb.top.rst_vip_m0_reset), cocotb.triggers.RisingEdge(cocotb.top.rst_vip_m1_reset))
        await cocotb.start_soon(lpi_master_sequence_param("lpi_param_stim", state_req = lpi_q_req_e.NO_REQUEST, pre_delay_clk = 0, post_delay_clk = 20).start(self.env.lpi_master_agent.sequencer))

    async def rst_apb_slv_mst_in_iso_state_task(self, min_delay_trn, max_delay_trn):
        wdt_delay = random.randint(min_delay_trn, max_delay_trn)
        await cocotb.triggers.Timer(wdt_delay, "ns")
        await cocotb.start_soon(lpi_master_sequence_param("lpi_param_stim", state_req = lpi_q_req_e.REQUEST, pre_delay_clk = 0, post_delay_clk = 0).start(self.env.lpi_master_agent.sequencer))
        while (cocotb.top.lpi_vip_m0_qacceptn.value == 1):
            await cocotb.triggers.FallingEdge(cocotb.top.lpi_vip_m0_qacceptn)
        await cocotb.start_soon(reset_sequence_param("rst_param_stim_slv", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 50, clk_cycles_after = 20).start(self.env.slv_reset_agent.reset_seqr))
        await cocotb.start_soon(lpi_master_sequence_param("lpi_param_stim", state_req = lpi_q_req_e.NO_REQUEST, pre_delay_clk = 0, post_delay_clk = 40).start(self.env.lpi_master_agent.sequencer))
        await cocotb.start_soon(lpi_master_sequence_param("lpi_param_stim", state_req = lpi_q_req_e.REQUEST, pre_delay_clk = 0, post_delay_clk = 0).start(self.env.lpi_master_agent.sequencer))
        while (cocotb.top.lpi_vip_m0_qacceptn.value == 1):
            await cocotb.triggers.FallingEdge(cocotb.top.lpi_vip_m0_qacceptn)
        await cocotb.start_soon(reset_sequence_param("rst_param_stim_mst", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = 40, clk_cycles_after = 30).start(self.env.mst_reset_agent.reset_seqr))

    async def run_phase(self):
        # Break into debugger for user control
        # breakpoint()  # or debugpy.breakpoint() on 3.6 and below
        try:
            is_debug = int(cocotb.plusargs["pydebug"])
        except KeyError:
            is_debug = 0
        
        if (is_debug):
            listen_host, listen_port = debugpy.listen(("localhost", 5679))
            debugpy.wait_for_client()
                   
        self.raise_objection()
        cocotb.start_soon(self.apb_slave_responce())
        self.start_clock("cocotb_clock")

        max_duration_rst = 30
        min_duration_rst = 20
        min_delay_trn = 0
        max_delay_trn = 2000

        try:
            num_pkts = int(cocotb.plusargs["num_pkts"])
        except KeyError:
            num_pkts = 1

        for i in range(num_pkts):
            self.logger.info("System cold-reset init")
            await cocotb.start_soon(self.all_reset())
            self.logger.info("System hot-reset init")
            duration_reset_slv = random.randint(min_duration_rst, max_duration_rst)
            duration_reset_mst = random.randint(min_duration_rst, max_duration_rst)
            duration_reset_dut = random.randint(min_duration_rst, max_duration_rst)
            rst_task_dut = cocotb.start_soon(reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = duration_reset_dut, clk_cycles_after = 0).start(self.env.dut_reset_agent.reset_seqr))
            rst_task_mst = cocotb.start_soon(reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = duration_reset_mst, clk_cycles_after = 0).start(self.env.mst_reset_agent.reset_seqr))
            rst_task_slv = cocotb.start_soon(reset_sequence_param("rst_param_stim", item_type = reset_action.RST_PULSE, clk_cycles_before = 0, clk_cycles_duration = duration_reset_slv, clk_cycles_after = 0).start(self.env.slv_reset_agent.reset_seqr))
            await cocotb.triggers.First(rst_task_dut, rst_task_mst, rst_task_slv)
            await cocotb.triggers.First(cocotb.start_soon(self.apb_mst_trn_task(min_delay_trn, max_delay_trn)), cocotb.start_soon(self.lpi_trn_task_after_reset()))
            await cocotb.triggers.Timer(max_delay_trn, "ns")
            #Separate reset for Slave and Master
            await cocotb.start_soon(self.all_reset())
            await cocotb.start_soon(lpi_master_sequence_param("lpi_param_stim", state_req = lpi_q_req_e.NO_REQUEST, pre_delay_clk = 0, post_delay_clk = 20).start(self.env.lpi_master_agent.sequencer))
            await cocotb.triggers.First(cocotb.start_soon(self.apb_mst_trn_task(min_delay_trn, max_delay_trn / 4)), cocotb.start_soon(self.rst_apb_slv_mst_in_iso_state_task(min_delay_trn + 1, max_delay_trn * 2)))
            await cocotb.triggers.Timer(max_delay_trn, "ns")
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, 10)
        self.drop_objection()
        
    def final_phase(self):
        uvm_factory().print(1)
