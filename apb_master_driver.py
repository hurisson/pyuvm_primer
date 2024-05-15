from apb_iso_pkg import * 

class apb_master_driver(uvm_driver):

    def __init__(self, *args, **kwargs):
        self.num_id = kwargs["num_id"]
        del kwargs["num_id"]
        super().__init__(*args, **kwargs)

    def connect_phase(self):
        pre_index = "apb" + "_vip_" + "m" + str(self.num_id - 1) + "_"
        self.paddr = getattr(cocotb.top, (pre_index + "paddr"))
        self.psel = getattr(cocotb.top, (pre_index + "psel"))
        self.pprot = getattr(cocotb.top, (pre_index + "pprot"))
        self.penable = getattr(cocotb.top, (pre_index + "penable"))
        self.pwrite = getattr(cocotb.top, (pre_index + "pwrite"))
        self.pwdata = getattr(cocotb.top, (pre_index + "pwdata"))
        self.pstrb = getattr(cocotb.top, (pre_index + "pstrb"))
        self.pready = getattr(cocotb.top, (pre_index + "pready"))
        self.prdata = getattr(cocotb.top, (pre_index + "prdata"))
        self.pslverr = getattr(cocotb.top, (pre_index + "pslverr"))
        self.pclk = getattr(cocotb.top, (pre_index + "pclk"))
        self.presetn = getattr(cocotb.top, (pre_index + "presetn"))

    def __sign_zero_init(self):
        self.penable.value = 0
        self.paddr.value   = 0
        self.psel.value    = 0
        self.pwrite.value  = 0
        self.pwdata.value  = 0
        self.pstrb.value   = 0
        self.pprot.value   = 0
        
    def __init_flag_to_zero(self):
        self.__flag_transaction_started       = 0
        self.__flag_transaction_completed     = 0
    
    async def __main_task(self):
        while True:    
            item = await self.seq_item_port.get_next_item()
            self.__flag_transaction_completed = 0
            self.__flag_transaction_started = 1
            await cocotb.triggers.ClockCycles(self.pclk, 1 + item.num_idle_cycles)
            if item.direction  == apb_direction.WRITE:
                self.pwrite.value = apb_direction.WRITE
                assert item.data is not None
                self.pwdata.value = item.data
                self.pstrb.value = item.pstrb
            elif item.direction  == apb_direction.READ:
                self.pwrite.value = apb_direction.READ
                self.pwdata.value = 0
                self.pstrb.value = 0
            else:
                raise RuntimeError("Unknown direction-field in item '{}'", item.direction)
            assert item.addr   is not None
            assert item.pprot2 is not None
            assert item.pprot1 is not None
            assert item.pprot0 is not None
            assert item.pstrb  is not None
            self.paddr.value = item.addr
            self.pprot.value = int ((str(item.pprot2.value) + str(item.pprot1.value) + str(item.pprot0.value)),2)
            self.psel.value = 1
            await cocotb.triggers.ClockCycles(self.pclk, 1)
            self.penable.value = 1
            await cocotb.triggers.ClockCycles(self.pclk, 1)
            while self.pready.value == 0:
                await cocotb.triggers.ClockCycles(self.pclk, 1)
            self.seq_item_port.item_done()
            self.__flag_transaction_completed = 1
            self.__flag_transaction_started = 0
            self.__sign_zero_init()

    async def __rst_task(self):
        await cocotb.triggers.FallingEdge(self.presetn)
        self.rst_assert = 1
        self.__sign_zero_init()

    async def run_phase(self):
        if (cocotb.SIM_NAME != "Verilator"): #x = 0 Verilator features
            await cocotb.triggers.FallingEdge(self.presetn)
        self.__sign_zero_init()
        while True:
            await cocotb.triggers.RisingEdge(self.presetn)
            self.rst_assert = 0
            self.__flag_transaction_completed = 0
            self.__flag_transaction_started = 0
            main_task = cocotb.start_soon(self.__main_task())
            await cocotb.triggers.First(main_task, cocotb.start_soon(self.__rst_task()))
            main_task.kill()
            if(self.__flag_transaction_completed == 0 and self.__flag_transaction_started == 1 ):
                self.seq_item_port.item_done()
