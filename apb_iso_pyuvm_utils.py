from apb_iso_pkg import *

@enum.unique
class lpi_q_req_e(enum.IntEnum):
    REQUEST = 0
    NO_REQUEST = 1

@enum.unique
class lpi_q_resp_e(enum.IntEnum):
    IDLE = 0
    ACCEPT = 1
    DENY = 2

@enum.unique
class lpi_q_active_e(enum.IntEnum):
    NOT_ACTIVE = 0
    ACTIVE = 1

@enum.unique
class lpi_q_state_e(enum.IntEnum):
    Q_RUN = 0
    Q_REQUEST = 1
    Q_STOPPED = 2
    Q_EXIT = 3
    Q_DENIED = 4
    Q_CONTINUE = 5
    ILLEGAL = 6


@enum.unique
class reset_action(enum.IntEnum):
    """Legal ops for the reset driver item"""
    RST_PULSE = 1
    DEASSERT = 2

@enum.unique
class reset_level(enum.IntEnum):
    LOW_LEVEL = 0
    HIGH_LEVEL = 1

@enum.unique
class apb_direction(enum.IntEnum):
    READ = 0
    WRITE = 1

@enum.unique
class apb_pprot0(enum.IntEnum):
    NORMAL = 0
    PRIVILEGED = 1

@enum.unique
class apb_pprot1(enum.IntEnum):
    SECURE = 0
    NON_SECURE = 1

@enum.unique
class apb_state(enum.IntEnum):
    IDLE = 0
    SETUP = 1
    ACCESS = 2
    ABORTED = 3

@enum.unique
class apb_pprot2(enum.IntEnum):
    DATA = 0
    INSTRUCTION = 1

@enum.unique
class rst_state(enum.IntEnum):
    """Legal ops for the reset monitor item"""
    RST_ASSERT = 0
    RST_DEASSERT = 1
