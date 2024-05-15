from apb_iso_pkg import *
@vsc.randobj
class apb_master_driver_item(uvm_sequence_item):

    def __init__(self):
        super().__init__("apb_master_driver_item")
        
        try:
            data_width = int(cocotb.plusargs["APB_ISO_ADDR_WIDTH"])
        except:
            data_width = 32

        try:
            addr_width = int(cocotb.plusargs["APB_ISO_ADDR_WIDTH"])
        except:
            addr_width = 32

        self.addr      = vsc.rand_bit_t(addr_width)
        self.data      = vsc.rand_bit_t(data_width)
        self.direction = vsc.rand_enum_t(apb_direction)
        self.pstrb     = vsc.rand_bit_t(data_width // 8)
        self.pprot0    = vsc.rand_enum_t(apb_pprot0)
        self.pprot1    = vsc.rand_enum_t(apb_pprot1)
        self.pprot2    = vsc.rand_enum_t(apb_pprot2)
        self.num_idle_cycles = vsc.uint32_t()
        self.max_num_idle_cycles = 5

    @vsc.constraint
    def addr_alligned_constr(self):
       self.addr[1:0] == 0
    
    @vsc.constraint
    def pstrb_constr(self):
        with vsc.if_then(self.direction == apb_direction.WRITE):
                self.pstrb > 0
        with vsc.if_then(self.direction == apb_direction.READ):
                self.pstrb == 0

    @vsc.constraint
    def num_idle_cycle_constr(self):
        self.num_idle_cycles in vsc.rangelist(vsc.rng(0,self.max_num_idle_cycles))

    def __eq__(self, other):
        pass

    def __str__(self):
        return self.__class__.__name__
