from apb_iso_pkg import *

@test()
class apb_iso_server_test(apb_iso_base_test):

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
        while (cocotb.top.rst_vip_m0_reset.value == 0 or cocotb.top.rst_vip_m1_reset.value == 0):
            await cocotb.triggers.First(cocotb.triggers.Edge(cocotb.top.rst_vip_m0_reset), cocotb.triggers.Edge(cocotb.top.rst_vip_m1_reset))
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
        self.raise_objection()
        cocotb.start_soon(self.apb_slave_responce())
        self.start_clock("cocotb_clock")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 15259))
        server.listen(1)
        conn, _ = server.accept()
        conn.send("APB_ISO_SERVER IS CONNECTED".encode("utf-8"))
        conn.setblocking(False)
        while True:
            try:
                hdr = conn.recv(1024)
            except:
                await cocotb.triggers.RisingEdge(cocotb.top.cocotb_clock)
                continue
            if (hdr.decode("utf-8") == "RESET ALL"):
                await cocotb.start_soon(self.all_reset())
                conn.send("System reset".encode("utf-8"))
            elif (hdr.decode("utf-8") == "APB TRANS"):
                await cocotb.start_soon(apb_master_random_sequence("apb_master_stimulus").start(self.env.apb_master_agent.apb_master_seqr))
                conn.send("APB-tran complete".encode("utf-8"))
            elif (hdr.decode("utf-8") == "FINISH"):
                break
            hdr = ""
            await cocotb.triggers.RisingEdge(cocotb.top.cocotb_clock)

        self.drop_objection()
