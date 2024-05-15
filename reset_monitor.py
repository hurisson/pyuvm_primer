from apb_iso_pkg import *

class reset_monitor(uvm_component):
    """
    Reset monitor
    """

    def __init__(self, *args, **kwargs):
        self.num_id = kwargs["num_id"]
        del kwargs["num_id"]
        super().__init__(*args, **kwargs)

    def connect_phase(self):
        pre_index = "rst" + "_vip_"+ "m" + str(self.num_id - 1) + "_"
        self.clk = getattr(cocotb.top, (pre_index + "clk"))
        self.rst = getattr(cocotb.top, (pre_index + "reset"))

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        await cocotb.triggers.Edge(self.rst)
        while True:
            await cocotb.triggers.Edge(self.rst)
            if self.rst.value:
                rst_st = rst_state.RST_ASSERT
            else:
                rst_st = rst_state.RST_DEASSERT
            time_assert = cocotb.utils.get_sim_time(units='ns')
            self.ap.write(reset_monitor_item(rst_st, time_assert))
