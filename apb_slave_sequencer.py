from apb_iso_pkg import *

class apb_slave_sequencer(uvm_sequencer):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.apb_slave_memory = dict()
        self.ready = CocotbEvent()
        self.pslverr = 0
        self.num_wait_cycles = 0
        
    def build_phase(self):
        super().build_phase()
        self.mon_trans_port_get = uvm_blocking_get_port("mon_trans_port_get", self)


    async def run_phase(self):
        while True:
            get_item = await self.mon_trans_port_get.get()
            mask_wr_data = ""
            wr_data = get_item.data
            self.build_item = apb_slave_driver_item()
            if self.pslverr == 0:
                if (get_item.direction == apb_direction.WRITE):
                    if get_item.address in self.apb_slave_memory:
                        mem_data = str(bin(self.apb_slave_memory[get_item.address]))
                        mem_data = mem_data.replace("0b","")
                    else:
                        self.build_item.randomize()
                        mem_data = str(bin(self.build_item.data))
                        mem_data = mem_data.replace("0b","")
                    for i in range((int(get_item.pstrb).bit_length())):
                        if (get_item.pstrb >> i) & 1:
                            mask_wr_data = "11111111" + mask_wr_data
                            if (i == 0):
                                mem_data = mem_data[:-8*(i+1)] + "00000000"
                            else:
                                mem_data = mem_data[:-8*(i+1)] + "00000000" + mem_data[-8*i:]
                        else:
                            mask_wr_data = "00000000" + mask_wr_data
                    wr_data = (wr_data & int(mask_wr_data, 2)) | int(mem_data, 2)
                    self.apb_slave_memory[get_item.address] = wr_data
                else:
                    if  get_item.address in self.apb_slave_memory:
                        self.build_item.data  = self.apb_slave_memory[get_item.address]
                    else:
                        self.build_item.randomize()
                        self.apb_slave_memory[get_item.address] = self.build_item.data
            self.build_item.error = self.pslverr
            self.build_item.num_wait_cycles  = self.num_wait_cycles
            self.build_item.direction = get_item.direction
            self.ready.set()
            self.ready.clear()
            next_item = await self.seq_q.get()
            self.logger.debug(f"Sequence item  {next_item} started")
            await self.seq_item_export.put_req(next_item)
               
    async def get_ready(self):
        await self.ready.wait()

    def final_phase(self):
        file_name = (str(self.get_full_name()) + "_mem.txt")
        with open(file_name,'w') as out:
            for addr, data in self.apb_slave_memory.items():
                out.write('MEM_ADDR |                 {}| DATA |                {}|\n'.format(addr, hex(data)))
        out.close()
