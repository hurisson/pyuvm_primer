from apb_iso_pkg import *
class apb_master_random_sequence(uvm_sequence):

    def __init__(self, name):
        super().__init__(name)

    async def body(self):
        item = apb_master_driver_item()
        item.randomize()
        await self.start_item(item)
        await self.finish_item(item)
