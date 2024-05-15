from apb_iso_pkg import *

class apb_iso_base_test(uvm_test):
    """
    Base test for the module
    """

    def __init__(self, name, parent):
        super().__init__(name, parent)

    def build_phase(self):
        self.env = apb_iso_env("apb_iso_env", self)
        self.cfg = apb_iso_env_cfg("apb_iso_env_cfg")
        self.apb_memory_random_responce_sequence = apb_memory_random_responce_sequence.create("slave_stimulus")
        self.cfg.build()
        ConfigDB().set(self, "apb_iso_env", "apb_iso_env_cfg", self.cfg)
    
    def start_clock(self, name):
        sig = getattr(cocotb.top, name)
        clock = cocotb.clock.Clock(sig, 42, units="ns")
        cocotb.start_soon(clock.start(start_high=False))
    
    async def apb_slave_responce(self):
        while True:
            await self.apb_memory_random_responce_sequence.start(self.env.apb_slave_agent.apb_slave_sequencer)

    def end_of_elaboration_phase(self):
        try:
            self.set_logging_level_hier(cocotb.plusargs["loglvl"])
        except KeyError:
            self.set_logging_level_hier(INFO)
            
    async def run_phase(self):
        self.raise_objection()
        cocotb.start_soon(self.apb_slave_responce())
        self.start_clock("cocotb_clock")
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, 2)
        await cocotb.triggers.ClockCycles(cocotb.top.cocotb_clock, 10)
        self.drop_objection()

    async def run(self):
        raise NotImplementedError()
