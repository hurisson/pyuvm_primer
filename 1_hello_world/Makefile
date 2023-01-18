CWD=$(shell pwd)
SIM ?= icarus
VERILOG_SOURCES =$(CWD)/rtl/top.sv
MODULE := testbench
TOPLEVEL = top
COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ns
include $(shell cocotb-config --makefiles)/Makefile.sim
