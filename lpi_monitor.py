from apb_iso_pkg import *

class lpi_monitor(uvm_component):
    """
    LPI monitor
    """
    def __init__(self, *args, **kwargs):
        self.num_id = kwargs["num_id"]
        del kwargs ["num_id"]
        super().__init__(*args, **kwargs)

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    def connect_phase(self):
        pre_index = "lpi" + "_vip_" + "m" + str(self.num_id - 1) + "_"
        self.qclk = getattr(cocotb.top, (pre_index + "qclk"))
        self.qreset = getattr(cocotb.top, (pre_index + "qreset"))
        self.qreqn = getattr(cocotb.top, (pre_index + "qreqn"))
        self.qacceptn = getattr(cocotb.top, (pre_index + "qacceptn"))
        self.qdeny = getattr(cocotb.top, (pre_index + "qdeny"))
        self.qactive = getattr(cocotb.top, (pre_index + "qactive"))
    
    def set_cfg(self, cfg):
        self.__cfg = cfg

    async def __main_task(self):
        while True:
            await cocotb.triggers.First(cocotb.triggers.Edge(self.qreqn), cocotb.triggers.Edge(self.qacceptn), cocotb.triggers.Edge(self.qdeny), cocotb.triggers.Edge(self.qactive))
            await cocotb.triggers.FallingEdge(self.qclk)
            if (self.qreset.value == 0):
                bus_item = lpi_q_item()
                if (self.qreqn.value):
                    bus_item.state_req = lpi_q_req_e.NO_REQUEST
                else:
                    bus_item.state_req = lpi_q_req_e.REQUEST
                if (self.qacceptn.value == 0 and self.qdeny.value == 0):
                    bus_item.state_resp = lpi_q_resp_e.ACCEPT
                elif (self.qacceptn.value == 1 and self.qdeny.value == 1):
                    bus_item.state_resp = lpi_q_resp_e.DENY
                elif (self.qacceptn.value == 1 and self.qdeny.value == 0):
                    bus_item.state_resp = lpi_q_resp_e.IDLE
                elif (self.qacceptn.value == 0 and self.qdeny.value == 1):
                    self.logger.error(f"Violation of LPI state transitions  - qacceptn = 0 and  qdeny = 1")
                    assert False, "Violation of LPI state transitions"
                if (self.qactive):
                    bus_item.state_active = lpi_q_active_e.ACTIVE
                else:
                    bus_item.state_active = lpi_q_active_e.NOT_ACTIVE
                self.ap.write(bus_item)

    async def __rst_task(self):
        await cocotb.triggers.RisingEdge(self.qreset)
        await cocotb.triggers.FallingEdge(self.qclk)
        bus_item_after_rst = lpi_q_item()
        if (self.qreqn.value):
            bus_item_after_rst.state_req = lpi_q_req_e.NO_REQUEST
        else:
            bus_item_after_rst.state_req = lpi_q_req_e.REQUEST
        if (self.qacceptn.value == 0 and self.qdeny.value == 0):
            bus_item_after_rst.state_resp = lpi_q_resp_e.ACCEPT
        elif (self.qacceptn.value == 1 and self.qdeny.value == 1):
            bus_item_after_rst.state_resp = lpi_q_resp_e.DENY
        elif (self.qacceptn.value == 1 and self.qdeny.value == 0):
            bus_item_after_rst.state_resp = lpi_q_resp_e.IDLE
        elif (self.qacceptn.value == 0 and self.qdeny.value == 1):
            self.logger.error(f"Violation of LPI state transitions  - qacceptn = 0 and  qdeny = 1")
            assert False, "Violation of LPI state transitions"
        if (self.qactive.value):
            bus_item_after_rst.state_active = lpi_q_active_e.ACTIVE
        else:
            bus_item_after_rst.state_active = lpi_q_active_e.NOT_ACTIVE
        self.ap.write(bus_item_after_rst)

    async def run_phase(self):
        while True:
            try: 
                state_x = str(self.qreset.value)
            except ValueError:
                state_x = "x"
            if (state_x != "x"):
                await cocotb.triggers.FallingEdge(self.qreset)
                first_task = cocotb.start_soon(self.__main_task())
                second_task = cocotb.start_soon(self.__rst_task())
                await cocotb.triggers.First(first_task, second_task)
            else:
                await cocotb.triggers.RisingEdge(self.qclk)
