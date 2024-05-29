# Translations
 - [Russian](README.ru.md)
 - [English](README.md)

# Example of using PyUVM for digital design verification


  The tested digital RTL design is an isolator (LPI q-channel based) for the AMBA APB3 protocol bus (rtl/apb_isolator_top.sv).

  **The composition of the PyUVM verification environment:**

    -apb_iso_base_test - basic test
        -apb_iso_env_cfg - environment configuration
        -apb_iso_env - environment
            -dut_reset_agent - agent for the DUT process
                -uvm_sequencer
                -reset_driver
                -reset_monitor
            -slv_reset_agent - agent for resetting the slave APB3
                -uvm_sequencer
                -reset_driver
                -reset_monitor
            -mst_reset_agent - agent for resetting master APB3
                -uvm_sequencer
                -reset_driver
                -reset_monitor
            -lpi_master_agent - LPI_Q channel interface management agent
                -uvm_sequencer
                -lpi_master_driver
                -lpi_monitor
            -apb_master_agent - APB3 Master bus management agent
                -uvm_sequencer
                -apb_master_driver
                -apb_monitor
            -apb_slave_agent - APB3 slave bus management agent
                -apb_slave_sequencer - non-standard sequencer, memory support is implemented
                -apb_slave_driver
                -uvm_tlm_fifo
                -apb_monitor
            -apb_iso_scoreboard - golden model
            -apb_iso_cov_collector - functional coverage collector (using cocotb-coverage)

  **Verification environment scheme on PyUVM:**
  ![image](https://github.com/hurisson/pyuvm_primer/assets/61613953/28a63384-993e-4527-86e8-48837aa27078)

  Each agent of the verification environment is assigned its own signals in the RTL wrapper (rtl/apb_isolator_top_wrapper.sv). This allows you to instantiate many identical agents in an environment. The names of the signals comparable to them are indexed by the serial number of the agent creation.


  **Used frameworks in the environment:**
  
  | Framework  | Link  |
  | ------------- | ------------- |
  | cocotb  | https://github.com/cocotb/cocotb  |
  | PyUVM  | https://github.com/pyuvm/pyuvm |
  | pyvsc (constraint, randomize)  | https://github.com/fvutils/pyvsc |
  | cocotb_coverage (functional coverage)  | https://cocotb-coverage.readthedocs.io/en/latest/ |
  | debugpy (Python debugger in  vscode) |https://github.com/microsoft/debugpy |

**Documentation of the standarts:**
  | Standart  | Link  |
  | ------------- | ------------- |
  | APB3  | https://web.eecs.umich.edu/~prabal/teaching/eecs373-f12/readings/ARM_AMBA3_APB.pdf  |
  | LPI q-channel  |  https://developer.arm.com/documentation/ihi0068/latest/|


**Start testing:**

  ```bash
  [user@pc /../pyuvm_primer]$ make 
  ```

Available Makefile Options:

  |  Option  | Description  |
  | ------------- | ------------- |
  | SIM  | Default - icarus. Support Synopsys, Cadence. With Verilator don't work in this env, because X-state checking.  |
  | TEST_NAME  | Default  - apb_iso_all_random_reset_test. Available variant - apb_iso_server_test  |
  | PLUSARGS | +APB_ISO_ADDR_WIDTH=32 (APB address width) +APB_ISO_DATA_WIDTH=32 (APB data width) +num_pkts=1000 (iterations in  apb_iso_all_random_reset_test) +has_cov=0 (coverage enable) +loglvl=DEBUG(log level) +pydebug=0 (python debug enable ) |
  | WAVES | Default  - 1. Support dump timing diagrams in vcd format |
  | COCOTB_HDL_TIMEUNIT | Default 1ns|
  | COCOTB_HDL_TIMEPRECISION | Default  1ps|


**Using client-server testing:**

  ![image](https://github.com/hurisson/pyuvm_primer/assets/61613953/fe3a494f-29d3-42c8-8697-d0e3ef2f2732)

In the test apb_iso_server_test.py the server is instantiated in run_phase. The server is waiting for the client to connect (apb_uart_client.py ) and commands from him. Simple commands such as starting a coroutine reset, random transaction on the master bus, and completing the simulation are implemented.


  ![2024-05-2413-32-26-ezgif com-video-to-gif-converter](https://github.com/hurisson/pyuvm_primer/assets/61613953/2ac04e2b-83e9-463f-8928-9b20b272e524)
