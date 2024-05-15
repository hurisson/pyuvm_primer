`timescale 1ns/1ps
module apb_isolator_top_wrapper
#(
    parameter
    AW  = 32, 
    DW  = 32 
)();

    wire             cocotb_clock       ;

    // LPI VIP master[0] wires
    wire             lpi_vip_m0_qreqn     ;
    wire             lpi_vip_m0_qacceptn  ;
    wire             lpi_vip_m0_qdeny     ;
    wire             lpi_vip_m0_qactive   ;
    wire             lpi_vip_m0_qreset    ;
    wire             lpi_vip_m0_qclk      ;

    // APB VIP slave wires
    wire [AW   -1:0] apb_vip_s0_paddr   ; 
    wire [3    -1:0] apb_vip_s0_pprot   ; 
    wire             apb_vip_s0_psel    ; 
    wire             apb_vip_s0_penable ; 
    wire             apb_vip_s0_pwrite  ; 
    wire [DW   -1:0] apb_vip_s0_pwdata  ; 
    wire [DW/8 -1:0] apb_vip_s0_pstrb   ; 
    wire             apb_vip_s0_pready  ; 
    wire [DW   -1:0] apb_vip_s0_prdata  ; 
    wire             apb_vip_s0_pslverr ;
    wire             apb_vip_s0_pclk    ;
    wire             apb_vip_s0_presetn ;

    //APB VIP master wires
    wire [AW   -1:0] apb_vip_m0_paddr   ; 
    wire [3    -1:0] apb_vip_m0_pprot   ; 
    wire             apb_vip_m0_psel    ; 
    wire             apb_vip_m0_penable ; 
    wire             apb_vip_m0_pwrite  ; 
    wire [DW   -1:0] apb_vip_m0_pwdata  ; 
    wire [DW/8 -1:0] apb_vip_m0_pstrb   ; 
    wire             apb_vip_m0_pready  ; 
    wire [DW   -1:0] apb_vip_m0_prdata  ; 
    wire             apb_vip_m0_pslverr ;
    wire             apb_vip_m0_pclk    ;
    wire             apb_vip_m0_presetn ;

    //RST VIP master[0] wires
    wire             rst_vip_m0_clk;
    wire             rst_vip_m0_reset;

    //RST VIP master[1] wires
    wire             rst_vip_m1_clk;
    wire             rst_vip_m1_reset;

    //RST VIP master[2] wires
    wire             rst_vip_m2_clk;
    wire             rst_vip_m2_reset;

    // clk & rst connect to APB-master[0] VIP
    assign apb_vip_m0_pclk = cocotb_clock;
    assign apb_vip_m0_presetn = rst_vip_m2_reset;

    // clk & rst connect to APB-slave[0] VIP
    assign apb_vip_s0_pclk = cocotb_clock;
    assign apb_vip_s0_presetn = rst_vip_m1_reset;

    // clk connect to RST-master[0] VIP
    assign rst_vip_m0_clk = cocotb_clock;

    // clk connect to RST-master[1] VIP
    assign rst_vip_m1_clk = cocotb_clock;

    // clk connect to RST-master[2] VIP
    assign rst_vip_m2_clk = cocotb_clock;

    // clk connect to RST-master[2] VIP
    assign lpi_vip_m0_qreset = ~rst_vip_m0_reset;
    assign lpi_vip_m0_qclk = cocotb_clock;

apb_isolator_top 
#(
    .AW  (AW)   , 
    .DW  (DW) 
)
dut

(
    .pclk_i      (cocotb_clock) , 
    .presetn_i   (rst_vip_m0_reset) , 
    .qreqn_i     (lpi_vip_m0_qreqn),
    .qacceptn_o  (lpi_vip_m0_qacceptn),
    .qdeny_o     (lpi_vip_m0_qdeny), 
    .qactive_o   (lpi_vip_m0_qactive),
    .s_paddr_i   (apb_vip_m0_paddr), 
    .s_pprot_i   (apb_vip_m0_pprot),
    .s_psel_i    (apb_vip_m0_psel),
    .s_penable_i (apb_vip_m0_penable),
    .s_pwrite_i  (apb_vip_m0_pwrite), 
    .s_pwdata_i  (apb_vip_m0_pwdata),
    .s_pstrb_i   (apb_vip_m0_pstrb),
    .s_pready_o  (apb_vip_m0_pready), 
    .s_prdata_o  (apb_vip_m0_prdata), 
    .s_pslverr_o (apb_vip_m0_pslverr), 

    .m_paddr_o   (apb_vip_s0_paddr), 
    .m_pprot_o   (apb_vip_s0_pprot),
    .m_psel_o    (apb_vip_s0_psel), 
    .m_penable_o (apb_vip_s0_penable),
    .m_pwrite_o  (apb_vip_s0_pwrite), 
    .m_pwdata_o  (apb_vip_s0_pwdata), 
    .m_pstrb_o   (apb_vip_s0_pstrb),
    .m_pready_i  (apb_vip_s0_pready),
    .m_prdata_i  (apb_vip_s0_prdata), 
    .m_pslverr_i (apb_vip_s0_pslverr) 
);

endmodule
