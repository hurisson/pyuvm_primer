from apb_iso_pkg import *
class apb_monitor_item(uvm_sequence_item):
    """
    APB-common monitor item
    """

    def __init__(self, direction = None, data = None, address = None, pprot0 = None, pprot1 = None, pprot2 = None, pslverr_enable = None, pstrb = None, curr_state = None, begin_time = None, end_time = None):
        super().__init__("apb_monitor_item")
        self.direction = direction
        self.data = data
        self.address = address
        self.pslverr_enable = pslverr_enable
        self.pstrb = pstrb
        self.pprot0 = pprot0
        self.pprot1 = pprot1
        self.pprot2 = pprot2
        self.curr_state = curr_state
        self.begin_time = begin_time
        self.end_time = end_time

    def __eq__(self, other):
        return (self.direction == other.direction and
                self.data == other.data and
                self.address == other.address and
                self.pslverr_enable == other.pslverr_enable and
                self.pstrb == other.pstrb and
                self.pprot0 == other.pprot0 and
                self.pprot1 == other.pprot1 and
                self.pprot2 == other.pprot2 and
                self.curr_state == other.curr_state)

    def __str__(self):
        return ((f"\nName: {self.get_full_name()} \
                \nADDR: {self.address} \
                \nDATA: {hex(self.data)} \
                \nDIRECTION: {apb_direction(self.direction).name} \
                \nSLV_ERR: {self.pslverr_enable} \
                \nPSTRB: {self.pstrb} \
                \nPPROT_0: {self.pprot0} \
                \nPPROT_1: {self.pprot1} \
                \nPPROT_2: {self.pprot2} \
                \nSTATE: {self.curr_state} \
                \nBEGIN_TIME: {self.begin_time} \
                \nEND_TINE: {self.end_time}"))
