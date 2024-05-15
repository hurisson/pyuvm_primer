`timescale 1ns/1ps
module apb_isolator_top
#(
    parameter
    AW   = 20 ,
    DW   = 32   
)
(

    input  wire             pclk_i      ,
    input  wire             presetn_i   , 

    input  wire             qreqn_i     ,
    output wire             qacceptn_o  , 
    output wire             qdeny_o     , 
    output wire             qactive_o   , 

    input  wire [AW   -1:0] s_paddr_i   , 
    input  wire [3    -1:0] s_pprot_i   , 
    input  wire             s_psel_i    , 
    input  wire             s_penable_i , 
    input  wire             s_pwrite_i  , 
    input  wire [DW   -1:0] s_pwdata_i  , 
    input  wire [DW/8 -1:0] s_pstrb_i   , 
    output wire             s_pready_o  , 
    output wire [DW   -1:0] s_prdata_o  , 
    output wire             s_pslverr_o , 

    output wire [AW   -1:0] m_paddr_o   , 
    output wire [3    -1:0] m_pprot_o   , 
    output wire             m_psel_o    , 
    output wire             m_penable_o , 
    output wire             m_pwrite_o  , 
    output wire [DW   -1:0] m_pwdata_o  , 
    output wire [DW/8 -1:0] m_pstrb_o   , 
    input  wire             m_pready_i  , 
    input  wire [DW   -1:0] m_prdata_i  , 
    input  wire             m_pslverr_i   

);

wire presetn_l ; 
wire qreqn_l   ; 
reg  qactive_l ; 
reg  iso_l     ;

assign qacceptn_o  = iso_l ? {    {1'b0}}  : 1'b1        ;
assign qdeny_o     =                         1'b0        ;
assign qactive_o   =                         qactive_l   ;
assign m_paddr_o   = iso_l ? {AW  {1'b0}}  : s_paddr_i   ;
assign m_pprot_o   = iso_l ? {3   {1'b0}}  : s_pprot_i   ;
assign m_psel_o    = iso_l ? {    {1'b0}}  : s_psel_i    ;
assign m_penable_o = iso_l ? {    {1'b0}}  : s_penable_i ;
assign m_pwrite_o  = iso_l ? {    {1'b0}}  : s_pwrite_i  ;
assign m_pwdata_o  = iso_l ? {DW  {1'b0}}  : s_pwdata_i  ;
assign m_pstrb_o   = iso_l ? {DW/8{1'b0}}  : s_pstrb_i   ;
assign s_pready_o  = iso_l ? {    {1'b1}}  : m_pready_i  ;
assign s_prdata_o  = iso_l ? {DW  {1'b0}}  : m_prdata_i  ;
assign s_pslverr_o = iso_l ? {    {1'b1}}  : m_pslverr_i ;

always @(posedge pclk_i or negedge presetn_l)
begin
    if (~presetn_l) qactive_l <= 1'b0     ;
    else            qactive_l <= s_psel_i ;
end
always @(posedge pclk_i or negedge presetn_l)
begin
    if (~presetn_l) iso_l <= 1'b1 ;
    else
    begin
        if (qreqn_l == iso_l)
        begin
            if (~s_psel_i || (s_penable_i && s_pready_o)) iso_l <= ~iso_l ;
        end
    end
end

assign presetn_l = presetn_i;
assign qreqn_l = qreqn_i;

endmodule
