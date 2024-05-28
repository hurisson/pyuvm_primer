# Example of using PyUVM for digital design verification / Пример использования  PyUVM для верификации цифрового дизайна:
EN:

  The tested digital RTL design is an isolator for the AMBA APB3 protocol bus (rtl/apb_isolator_top.sv).

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


  **Verification environment scheme on PyUVM:**
  ![image](https://github.com/hurisson/pyuvm_primer/assets/61613953/28a63384-993e-4527-86e8-48837aa27078)
RU:
  Тестируемый цифровой дизайн RTL - изолятор для шины протокола семейства AMBA APB3 (rtl/apb_isolator_top.sv).  
  
  **Состав верификационного окружения PyUVM:**  
  
        -apb_iso_base_test - базовый тест 
            -apb_iso_env_cfg - конфигурация окружения 
            -apb_iso_env - окружение 
                -dut_reset_agent  - агент для сроса DUT
                    -uvm_sequencer
                    -reset_driver
                    -reset_monitor
                -slv_reset_agent  - агент для сброса slave APB3 
                    -uvm_sequencer
                    -reset_driver
                    -reset_monitor
                -mst_reset_agent - агент для сброса master APB3
                    -uvm_sequencer
                    -reset_driver
                    -reset_monitor
                -lpi_master_agent - агент управления интерфейсом LPI_Q channel
                    -uvm_sequencer
                    -lpi_master_driver
                    -lpi_monitor
                -apb_master_agent - агент управления шиной мастера APB3
                    -uvm_sequencer
                    -apb_master_driver
                    -apb_monitor 
                -apb_slave_agent - агент управления шиной слейва APB3
                    -apb_slave_sequencer - нестандартный секвенсор, реализована поддержка памяти
                    -apb_slave_driver
                    -uvm_tlm_fifo
                    -apb_monitor  

  **Схема верификационного окружения PyUVM:** 
  ![image](https://github.com/hurisson/pyuvm_primer/assets/61613953/28a63384-993e-4527-86e8-48837aa27078)
