from apb_iso_pkg import *
class apb_slave_driver(uvm_driver):
    """
       Seqr <---> Driver
    Monitor <--^
    """
    def __init__(self, *args, **kwargs):
        self.num_id = kwargs["num_id"]
        del kwargs["num_id"]
        super().__init__(*args, **kwargs)

    def connect_phase(self):
        pre_index = "apb" + "_vip_" + "s" + str(self.num_id - 1) + "_"
        self.pready = getattr(cocotb.top, (pre_index + "pready"))
        self.prdata = getattr(cocotb.top, (pre_index + "prdata"))
        self.pslverr = getattr(cocotb.top, (pre_index + "pslverr"))
        self.presetn = getattr(cocotb.top, (pre_index + "presetn"))
        self.pclk    = getattr(cocotb.top, (pre_index + "pclk"))

    def zero_init(self):
        self.pready.value = 0
        self.prdata.value  = 0
        self.pslverr.value = 0

    def set_cfg(self, cfg):
        self.__cfg = cfg

    def __sign_default_init(self):
        self.pready.value = self.__cfg.pready_default
        self.prdata.value  = 0
        self.pslverr.value = 0

    def __sign_reset_init(self):
        self.pready.value = 0
        self.prdata.value  = 0
        self.pslverr.value = 0
        

    def __init_flag_to_zero(self):
        self.__flag_transaction_started       = 0 #private
        self.__flag_transaction_completed     = 0 #private
    

    async def __main_task(self):
        while True:
            item = await self.seq_item_port.get_next_item() #ToDo
            self.__flag_transaction_started = 1
            self.__flag_transaction_completed = 0
            if (item.num_wait_cycles > 0):
                self.pready.value = 0
            for i in range(item.num_wait_cycles):
                await cocotb.triggers.RisingEdge(self.pclk)
            self.pready.value = 1
            if item.direction  == apb_direction.WRITE:
                self.prdata.value = 0
            elif item.error == 1:
                self.prdata.value = 0
            else:
                self.prdata.value = item.data
            self.pslverr.value = item.error
            await cocotb.triggers.RisingEdge(self.pclk)
            self.__sign_default_init()
            self.seq_item_port.item_done()
            self.__flag_transaction_completed = 1
            self.__flag_transaction_started = 0


    async def __rst_task(self):
        await cocotb.triggers.FallingEdge(self.presetn)
        self.rst_assert = 1
        self.__sign_reset_init()

    async def run_phase(self):
        if (cocotb.SIM_NAME != "Verilator"): #x = 0 Verilator features
            await cocotb.triggers.FallingEdge(self.presetn)
        self.__sign_reset_init()
        self.__init_flag_to_zero()
        while True:
            await cocotb.triggers.RisingEdge(self.presetn)
            self.__sign_default_init()
            self.__init_flag_to_zero()
            self.rst_assert = 0
            t1 = cocotb.start_soon(self.__main_task())
            await cocotb.triggers.First(t1, cocotb.start_soon(self.__rst_task()))
            t1.kill()
            if(self.__flag_transaction_completed == 0 and self.__flag_transaction_started == 1):
                self.seq_item_port.item_done()
