from apb_iso_pkg import *

class apb_monitor(uvm_component):
    """
    APB master-interface monitor
    """
    def __init__(self, *args, **kwargs):
        self.is_master = kwargs["is_master"]
        self.num_id = kwargs["num_id"]
        del kwargs ["is_master"]
        del kwargs ["num_id"]
        super().__init__(*args, **kwargs)

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        if not self.is_master:
            self.mon_trans_port_put  = uvm_blocking_put_port("mon_trans_port_put", self)

    def connect_phase(self):
        if self.is_master:
            pre_index = "apb" + "_vip_" + "m" + str(self.num_id - 1) + "_"
        else:
            pre_index = "apb" + "_vip_" + "s" + str(self.num_id - 1) + "_"
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

    def set_cfg(self, cfg):
        self.__cfg = cfg
        
    async def run_phase(self):
        if not self.is_master:
            fix_pready_timeout = 500000
        else:
            fix_pready_timeout = self.__cfg.fix_pready_timeout
        send_trans = 0
        if (cocotb.SIM_NAME != "Verilator"): #x = 0 Verilator features
            await cocotb.triggers.RisingEdge(self.presetn)
            await cocotb.triggers.RisingEdge(self.presetn)
        else: 
            await cocotb.triggers.RisingEdge(self.presetn)
        tr = apb_monitor_item()
        tr.curr_state = apb_state.IDLE.name
        wdt_timeout = 0
        while True:
            await cocotb.triggers.First(cocotb.triggers.RisingEdge(self.pclk), cocotb.triggers.FallingEdge(self.presetn))
            if (self.presetn.value == 0):
                if (tr.curr_state == apb_state.SETUP.name or tr.curr_state == apb_state.ACCESS.name):
                    tr.curr_state = apb_state.ABORTED.name
                    tr.end_time = cocotb.utils.get_sim_time(units='ns')
                    if (send_trans == 0 ):
                        self.ap.write(apb_monitor_item(tr.direction, tr.data, tr.address, tr.pprot0, tr.pprot1, tr.pprot2, tr.pslverr_enable, tr.pstrb, tr.curr_state, tr.begin_time, tr.end_time))
                    send_trans = 1
                    tr.curr_state = apb_state.IDLE.name
                else:
                    tr.curr_state = apb_state.IDLE.name
                    send_trans = 0
            elif (self.psel.value == 0 and self.penable.value == 0):
                if (tr.curr_state == apb_state.ACCESS.name):
                    tr.curr_state = apb_state.IDLE.name
                    send_trans = 0
                elif (tr.curr_state == apb_state.IDLE.name):
                    pass
                else:
                    self.logger.error(f"Violation of APB state transitions in {tr.curr_state.name}")
                    assert False, "Violation of state transitions in SETUP-state"
            elif (self.psel.value == 1  and self.penable.value == 0):
                if (tr.curr_state == apb_state.IDLE.name or tr.curr_state == apb_state.ACCESS.name ):
                    tr.curr_state = apb_state.SETUP.name
                else:
                    self.logger.error(f"Violation of APB state transitions")
                    assert False, "Violation of state transitions in SETUP-state"
                send_trans = 0
                tr.begin_time = cocotb.utils.get_sim_time(units='ns')
                tr.address = hex(self.paddr.value)
                tr.direction = self.pwrite.value
                tr.data = self.pwdata.value
                tr.pstrb = self.pstrb.value
                if tr.direction == apb_direction.READ.name:
                    assert self.pwdata.value == 0, "PWDATA must be zero for READ-transaction"
                    assert self.pstrb.value == 0, "PSTRB must be zero for READ-transaction"
                tr.pprot0 = apb_pprot0(self.pprot.value & 0b001).name
                tr.pprot1 = apb_pprot1((self.pprot.value & 0b010) >> 1).name
                tr.pprot2 = apb_pprot2((self.pprot.value & 0b100) >> 2).name
                if not self.is_master:
                    if (self.__cfg.is_active):
                        await self.mon_trans_port_put.put(apb_monitor_item(tr.direction, tr.data, tr.address, tr.pprot0, tr.pprot1, tr.pprot2, tr.pslverr_enable, tr.pstrb, tr.curr_state, tr.begin_time, tr.end_time))
            elif (self.psel.value == 1 and self.penable.value == 1):
                if tr.curr_state == apb_state.SETUP.name:
                    tr.curr_state = apb_state.ACCESS.name
                    assert tr.address == hex(self.paddr.value), "PADDR change value in SETUP_to_ACCESS cycle"
                    if (tr.direction == apb_direction.WRITE.name):
                        assert tr.data == self.pwdata.value, "PWDATA change value in SETUP_to_ACCESS cycle"
                    assert tr.direction == self.pwrite.value,"PWRITE change value in SETUP_to_ACCESS cycle"
                    assert tr.pprot0 == apb_pprot0(self.pprot.value & 0b001).name, "PPROT0 change value in SETUP_to_ACCESS cycle"
                    assert tr.pprot1 == apb_pprot1((self.pprot.value & 0b010) >> 1).name, "PPROT1 change value in SETUP_to_ACCESS cycle"
                    assert tr.pprot2 == apb_pprot2((self.pprot.value & 0b100) >> 2).name, "PPROT2 change value in SETUP_to_ACCESS cycle"
                    assert tr.pstrb == self.pstrb.value, "PPROT2 change value in SETUP_to_ACCESS cycle"
                    if self.pready.value:
                        tr.end_time = cocotb.utils.get_sim_time(units='ns')
                        if (tr.direction == apb_direction.READ.name):
                            tr.data = self.prdata.value
                        tr.pslverr_enable = self.pslverr.value
                        send_trans = 1
                        self.ap.write(apb_monitor_item(tr.direction, tr.data, tr.address, tr.pprot0, tr.pprot1, tr.pprot2, tr.pslverr_enable, tr.pstrb, tr.curr_state, tr.begin_time, tr.end_time))
                        wdt_timeout = 0
                elif tr.curr_state == apb_state.ACCESS.name:
                    if (wdt_timeout  < fix_pready_timeout):
                        if self.pready.value:
                            wdt_timeout = 0
                            tr.end_time = cocotb.utils.get_sim_time(units='ns')
                            if (tr.direction == apb_direction.READ):
                                tr.data = self.prdata.value
                            tr.pslverr_enable = self.pslverr.value
                            send_trans = 1
                            self.ap.write(apb_monitor_item(tr.direction, tr.data, tr.address, tr.pprot0, tr.pprot1, tr.pprot2, tr.pslverr_enable, tr.pstrb, tr.curr_state, tr.begin_time, tr.end_time))
                        else:
                            wdt_timeout += 1
                    else:
                        self.logger.error(f"TIMEOUT of PREADY, timeout set {fix_pready_timeout} clock cycles")
                        assert False, "TIMEOUT of PREADY in APB-bus"
                else:
                    self.logger.error(tr.curr_state)
                    self.logger.error(f"Violation of APB state transitions")
                    assert False, "Violation of state transitions in SETUP-state"
