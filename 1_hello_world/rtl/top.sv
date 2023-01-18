module top (
    input clk_i,
    input rstn_i,
    output logic led
);

always @(posedge clk_i) begin
    if (!rstn_i)
        led <= 0;
    else
        led <= 1;     
end

endmodule
