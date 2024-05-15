from apb_iso_pkg import *

class reset_driver(uvm_driver):
    def __init__(self, *args, **kwargs):
        self.num_id = kwargs["num_id"]
        del kwargs["num_id"]
        super().__init__(*args, **kwargs)

    def connect_phase(self):
        pre_index = "rst" + "_vip_"+ "m" + str(self.num_id - 1) + "_"
        self.clk = getattr(cocotb.top, (pre_index + "clk"))
        self.rst = getattr(cocotb.top, (pre_index + "reset"))

    async def run_phase(self):
        active_level = cocotb.binary.BinaryValue(value=self.__cfg.active_level, bigEndian=True, n_bits=1)
        await cocotb.triggers.RisingEdge(self.clk)
        self.rst.value = int(~active_level, 2)
        while True:
            item = await self.seq_item_port.get_next_item()
            if item.item_type  == reset_action.RST_PULSE:
                await cocotb.triggers.ClockCycles(self.clk, 1 + item.clk_cycles_before)
                self.rst.value = int(active_level)
                await cocotb.triggers.ClockCycles(self.clk, item.clk_cycles_duration)
                self.rst.value = int(~active_level, 2)
                await cocotb.triggers.ClockCycles(self.clk, item.clk_cycles_after)
            else:
                raise RuntimeError("Unknown item '{}'" , item.item_type)
            self.seq_item_port.item_done()

    def set_cfg(self, cfg):
        self.__cfg = cfg
