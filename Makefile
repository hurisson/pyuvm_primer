CWD=$(shell pwd)
SIM ?= icarus #Verilator don't supported  
TEST_NAME ?= apb_iso_all_random_reset_test
VERILOG_SOURCES =$(CWD)/rtl/apb_isolator_top_wrapper.sv \
				 $(CWD)/rtl/apb_isolator_top.sv	 
MODULE := $(TEST_NAME)
TOPLEVEL = apb_isolator_top_wrapper
PLUSARGS ?=+APB_ISO_ADDR_WIDTH=32 +APB_ISO_DATA_WIDTH=32 +num_pkts=5 +has_cov=0 +loglvl=DEBUG +pydebug=0
WAVES ?= 1
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps
include $(shell cocotb-config --makefiles)/Makefile.sim
