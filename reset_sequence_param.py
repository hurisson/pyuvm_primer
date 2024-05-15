
from apb_iso_pkg import *
class reset_sequence_param(uvm_sequence):
    def __init__(self, name, item_type, clk_cycles_before, clk_cycles_duration, clk_cycles_after):
        super().__init__(name)
        self.item_type = item_type
        self.clk_cycles_after = clk_cycles_after
        self.clk_cycles_before = clk_cycles_before
        self.clk_cycles_duration = clk_cycles_duration
        
    async def body(self):
        item = reset_driver_item(self.item_type, self.clk_cycles_before, self.clk_cycles_duration, self.clk_cycles_after)
        await self.start_item(item)
        await self.finish_item(item)