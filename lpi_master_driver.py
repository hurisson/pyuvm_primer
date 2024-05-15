from apb_iso_pkg import *

class lpi_master_driver(uvm_driver):

    def __init__(self, *args, **kwargs):
        self.num_id = kwargs["num_id"]
        del kwargs["num_id"]
        self.__flag_transaction_completed = 0
        self.__flag_transaction_started = 0
        super().__init__(*args, **kwargs)

    def connect_phase (self):
        pre_index = "lpi" + "_vip_" + "m" + str(self.num_id - 1) + "_"
        self.qreqn = getattr(cocotb.top, (pre_index + "qreqn"))
        self.qclk = getattr(cocotb.top, (pre_index + "qclk"))
        self.qreset = getattr(cocotb.top, (pre_index + "qreset"))

    def __init_flag_to_zero(self):
        self.__flag_transaction_started       = 0 #private
        self.__flag_transaction_completed     = 0 #private

    def set_cfg(self, cfg):
        self.__cfg = cfg

    async def __main_task(self):
        while True:    
            item = await self.seq_item_port.get_next_item() #ToDo
            self.__flag_transaction_started = 1
            await cocotb.triggers.ClockCycles(self.qclk, 1 + item.pre_delay_clk)
            if item.state_req  == lpi_q_req_e.REQUEST:
                self.qreqn.value = 0
            elif item.state_req  == lpi_q_req_e.NO_REQUEST:
                self.qreqn.value = 1
            else:
                raise RuntimeError("Unknown switch case-statement: '{}'" , item.state_req)
            await cocotb.triggers.ClockCycles(self.qclk, item.post_delay_clk)
            self.seq_item_port.item_done()
            self.__flag_transaction_completed = 1
            self.__init_flag_to_zero()

    async def __rst_task(self):
        await cocotb.triggers.RisingEdge(self.qreset)
        self.qreqn.value = self.__cfg.qreqn_state_during_rst

    async def run_phase(self):
        await cocotb.triggers.RisingEdge(self.qreset)
        self.qreqn.value = 0
        await cocotb.triggers.FallingEdge(self.qreset)
        while True:
            first_task = cocotb.start_soon(self.__main_task())
            second_task = cocotb.start_soon(self.__rst_task())
            await cocotb.triggers.First(first_task, second_task)
            if(self.__flag_transaction_started == 1 and ~self.__flag_transaction_completed == 1):
                seq_item_port.item_done()
            self.__init_flag_to_zero()
