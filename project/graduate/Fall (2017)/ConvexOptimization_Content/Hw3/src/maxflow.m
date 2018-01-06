cvx_begin
    variable vsa(1);
    variable vsc(1);
    variable vab(1);
    variable vad(1);
    variable vcd(1);
    variable vcf(1);
    variable vbe(1);
    variable vde(1);
    variable vdf(1);
    variable vfe(1);
    variable vet(1);
    variable vft(1);
    
    maximize (vsa + vsc);
    subject to
        0 <= vsa <= 6;
        0 <= vsc <= 7;
        0 <= vab <= 5;
        0 <= vad <= 4;
        0 <= vcd <= 1;
        0 <= vcf <= 5;
        0 <= vbe <= 7;
        0 <= vde <= 3;
        0 <= vdf <= 3;
        0 <= vfe <= 2;
        0 <= vet <= 9;
        0 <= vft <= 4;
        vsa <= vab + vad; % a
        vab == vbe; % b
        vsc == vcd + vcf; % c
        vad + vcd == vde + vdf; % d
        vbe + vde + vfe == vet; % e
        vcf + vdf == vfe + vft; % f
cvx_end