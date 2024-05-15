from apb_iso_pkg import *
@vsc.randobj
class lpi_q_item(uvm_sequence_item):
    """
    LPI-Master driver item
    """
    def __init__(self, pre_delay_clk = 0, post_delay_clk = 0, state_req = None, state_resp = None, state_active = None):
        super().__init__("lpi_q_item")
        self.pre_delay_clk = pre_delay_clk
        self.post_delay_clk = post_delay_clk
        self.state_req = state_req
        self.state_resp = state_resp
        self.state_active = state_active

    def randomize(self):
        self.__randomize_req()

    def __randomize_req(self):
        self.state_req = random.choice(list(state_req))

    def __eq__(self, other):
        pass

    def __str__(self):
        return self.__class__.__name__

    def get_lpi_state(self):
        if (self.state_req == lpi_q_req_e.NO_REQUEST and  self.state_resp == lpi_q_resp_e.IDLE):
            return lpi_q_state_e.Q_RUN.name
        elif (self.state_req == lpi_q_req_e.REQUEST and self.state_resp == lpi_q_resp_e.IDLE):
            return lpi_q_state_e.Q_REQUEST.name
        elif (self.state_req == lpi_q_req_e.REQUEST and self.state_resp == lpi_q_resp_e.ACCEPT):
            return lpi_q_state_e.Q_STOPPED.name
        elif (self.state_req == lpi_q_req_e.NO_REQUEST and self.state_resp == lpi_q_resp_e.ACCEPT):
            return lpi_q_state_e.Q_EXIT.name
        elif (self.state_req == lpi_q_req_e.REQUEST and self.state_resp == lpi_q_resp_e.DENY):
            return lpi_q_state_e.Q_DENIED.name
        elif (self.state_req == lpi_q_req_e.NO_REQUEST and self.state_resp == lpi_q_resp_e.DENY):
            return lpi_q_state_e.Q_CONTINUE.name
        else:
            return lpi_q_state_e.ILLEGAL.name
