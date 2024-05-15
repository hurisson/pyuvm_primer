
from apb_iso_pkg import *
class reset_monitor_item(uvm_sequence_item):
    """
    Reset monitor item
    """
    def __init__(self, rst_st, time_assert):
        super().__init__("reset_monitor_item")
        self.rst_st = rst_st
        self.time_assert = time_assert

    def randomize(self):
        pass

    def __eq__(self, other):
        pass

    def __str__(self):
        return self.get_full_name()
