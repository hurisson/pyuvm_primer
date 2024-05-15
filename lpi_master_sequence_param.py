from apb_iso_pkg import *
class lpi_master_sequence_param(uvm_sequence):
    def __init__(self, name, pre_delay_clk, post_delay_clk, state_req):
        super().__init__(name)
        self.pre_delay_clk = pre_delay_clk
        self.post_delay_clk = post_delay_clk
        self.state_req = state_req
    async def body(self):
        item = lpi_q_item(state_req = self.state_req, pre_delay_clk = self.pre_delay_clk, post_delay_clk = self.post_delay_clk)
        await self.start_item(item)
        await self.finish_item(item)
