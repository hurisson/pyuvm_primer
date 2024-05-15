from  apb_iso_pkg import *
class apb_memory_random_responce_sequence(uvm_sequence):

    def __init__(self, name):
        super().__init__(name)

    async def body(self):
        self.sequencer.pslverr = random.randint(0, 1)
        self.sequencer.num_wait_cycles = random.randint(0, 5)
        await self.sequencer.get_ready()
        item = self.sequencer.build_item
        await self.start_item(item)
        await self.finish_item(item)
