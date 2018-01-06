function a1()

% (a)
cvx_begin quiet
    variables x1 x2;
    dual variables y1 y2 y3;
    minimize 0.5 * x1^2 + 1.5 * x2^2 + 0.5 * (x1 - x2)^2 - x1;
    subject to
        y1: x1 + 2 * x2 <= -2;
        y2: x1 - 4 * x2 <= -3;
        y3: 5 * x1 + 76 * x2 <= 1;
cvx_end
opt = cvx_optval;



% (b)
u1 = -2;
u2 = -3;
d = [0, -0.1, 0.1];
for i = 1:3
    for j = 1:3
        cvx_begin quiet
            variables x1 x2;
            minimize 0.5 * x1^2 + 1.5 * x2^2 + 0.5 * (x1 - x2)^2 - x1;
            subject to
                x1 + 2 * x2 <= u1 + d(i);
                x1 - 4 * x2 <= u2 + d(j);
                5 * x1 + 76 * x2 <= 1;
        cvx_end
        pp = opt - y1 * d(i) - y2 * d(j);
        pe = cvx_optval;
        fprintf('d1=%+f d2=%+f, pp=%+f, pe=%+f\n', d(i), d(j), pp, pe);
    end
end

end