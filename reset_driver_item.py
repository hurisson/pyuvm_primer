from apb_iso_pkg import *
class reset_driver_item(uvm_sequence_item):
    def __init__(self, item_type, clk_cycles_before = 0, clk_cycles_duration = 0, clk_cycles_after = 0):
        super().__init__("reset_driver_item")
        self.item_type = item_type
        self.clk_cycles_after = clk_cycles_after
        self.clk_cycles_before = clk_cycles_before
        self.clk_cycles_duration = clk_cycles_duration

    def randomize(self):
        pass

    def __eq__(self, other):
        pass

    def __str__(self):
        return self.__class__.__name__
