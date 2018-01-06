addpath('..');
x = 1:1:10;
m=0.1;k=0.01;
y = -k ./ (x.^2);
n = length(y);
y = y';
cvx_setup
cvx_begin
variable F(n)
minimize norm(-F+y,2)
cvx_end