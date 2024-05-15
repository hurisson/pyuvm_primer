from apb_iso_pkg import *
class apb_slave_driver_item(uvm_sequence_item):
    """
    APB-Slave driver item
    """
    def __init__(self, data = None, error = None, num_wait_cycles = None, direction = None):
        super().__init__("apb_slave_driver_item")
        self.data = data
        self.error = error
        self.direction = direction
        self.num_wait_cycles = num_wait_cycles

    def randomize(self):
        self.randomize_resp()
        self.randomize_data()
        
    def randomize_resp(self):
        slv_err = ""
        slv_err += random.choice(["0", "1"])
        self.error = int(slv_err,2)
    
    def randomize_data(self):
        data = ""
        for i in range(int(cocotb.plusargs["APB_ISO_DATA_WIDTH"])):
            data += random.choice(["0", "1"])
        self.data = int(data, 2)

    def __eq__(self, other):
        pass

    def __str__(self):
        return self.__class__.__name__
