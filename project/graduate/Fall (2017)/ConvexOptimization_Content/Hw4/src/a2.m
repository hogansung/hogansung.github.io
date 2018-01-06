function a2()
% (b)
randn('seed', 1); 
T = 96;
t = (1:T)'; 
p = exp(-cos((t-15)*2*pi/T)+0.01*randn(T,1)); 
u = 2*exp(-0.6*cos((t+40)*pi/T) -0.7*cos(t*4*pi/T)+0.01*randn(T,1));

[optv, c, q] = optimize(T, p, u, 3, 3, 35);
disp(optv);

hold on
plot(t, u);
plot(t, p);
plot(t, c);
plot(t, q);
hold off

legend('ut', 'pt', 'ct', 'qt');


% (c)
Q = (1:35)';

cd3_v = zeros(size(Q));
for i = 1:size(Q,1)
    [optv, ~, ~] = optimize(T, p, u, 3, 3, Q(i));
    cd3_v(i) = optv;
end

cd1_v = zeros(size(Q));
for i = 1:size(Q,1)
    [optv, ~, ~] = optimize(T, p, u, 1, 1, Q(i));
    cd1_v(i) = optv;
end

hold on
plot(Q, cd3_v);
plot(Q, cd1_v);
hold off

legend('C = D = 3', 'C = D = 1')
end

function [cvx_optval, q, c] = optimize(T, p, u, C, D, Q)
    cvx_begin quiet
        variable q(T);
        variable c(T);
        minimize (p' * (u + c));

        q(1) == q(T) + c(T);
        for i = 1:(T-1)
            q(i+1) == q(i) + c(i);
        end

        for i = 1:T
            c(i) <= C;
            c(i) >= -D;
            q(i) >= 0;
            q(i) <= Q;
        end
    cvx_end
end