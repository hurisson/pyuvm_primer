import cocotb
import pyuvm
import random

from cocotb.triggers import Timer
from pyuvm import *


@pyuvm.test()

class send_hello_world_in_any_time (uvm_test):

    async def run_phase(self):
        self.raise_objection()
        alarm  = random.randrange(1000,100000,1)
        self.logger.info("Message will be started after %d  ns",  alarm)
        await Timer(alarm,'ns')
        self.logger.info('Hello World')
        self.drop_objection()

uvm_root().run_test('send_hello_world_in_any_time')        

    