"""Re-checks every number quoted in Day04_Sinusoidal_Steady_State_and_Resonance.md and Day04_Conceptual_Questions.md.

Run:  python3 verify_day04.py          (needs numpy; uses mna.py with complex impedances)
Past-year answers are checked against the official keys quoted in the comments.
"""
import numpy as np

from mna import solve

m, k, u = 1e-3, 1e3, 1e-6
J = 1j


def check(name, got, want, tol=1e-6):
    assert abs(got - want) < tol, f'{name}: got {got}, expected {want}'
    print(f'ok  {name:<60} {got:.5g}' if np.isrealobj(got) else f'ok  {name:<60} {got:.5g}')


def pol(z):
    return abs(z), np.degrees(np.angle(z))


# ============================================================ phasors and impedance
check('sin(wt + 30) as a cosine: angle (deg)', 30 - 90, -60)
check('Q2 option: phasor angle of 10 sin(100t+30deg) (deg)', 30 - 90, -60)
tt = np.linspace(0, 0.2, 7)
check('Q2 10 sin(100t+30deg) == 10 cos(100t-60deg)', np.max(abs(10 * np.sin(100 * tt + np.radians(30)) - 10 * np.cos(100 * tt - np.radians(60)))), 0, 1e-12)
# Q1 (B): the product of two sinusoids is NOT a sinusoid at w: v = i = cos(wt)  ->  v i = 1/2 + 1/2 cos(2wt), no component at w
tq = np.linspace(0, 2 * np.pi, 200001)[:-1]
prod = np.cos(tq) * np.cos(tq)
check('Q1 product cos*cos: component at w (cos part)', 2 * np.mean(prod * np.cos(tq)), 0, 1e-9)
check('Q1 product cos*cos: DC part is 1/2 (not Re{V I} = 1)', np.mean(prod), 0.5, 1e-9)

# Ex 1: series R = 4, X_L = 7, X_C = 4, 10 V rms
Z = 4 + J * (7 - 4)
I = 10 / Z
check('Ex1 |Z|', abs(Z), 5); check('Ex1 |I| (A)', abs(I), 2)
VR, VL, VC = I * 4, I * J * 7, I * (-J) * 4
check('Ex1 |V_R|', abs(VR), 8); check('Ex1 |V_L|', abs(VL), 14); check('Ex1 |V_C|', abs(VC), 8)
check('Ex1 V_R + V_L + V_C = 10', abs(VR + VL + VC), 10)
check('Ex1 power factor', 4 / 5, 0.8)
check('Ex1 P (W) = I^2 R', abs(I) ** 2 * 4, 16)
check('Ex1 Q (var) = I^2 X', abs(I) ** 2 * 3, 12)
check('Ex1 S = V I* (VA) magnitude', abs(10 * np.conj(I)), 20)

# Q4: sign conventions
check('Q4 Y_L = 1/(j w L) has NEGATIVE imaginary part (susceptance < 0 = inductive)', np.sign((1 / (1j * 1000 * 0.01)).imag), -1)
check('Q4 Y_C = j w C has POSITIVE susceptance (capacitive)', np.sign((1j * 1000 * 1e-6).imag), 1)
check('Q4 |Z_C| = 1/(w C) -> 0 as w -> infinity (a short)', 1 / (1e12 * 1e-6), 0, 1e-5)
check('Q4 |Z| for R=3, XL=8, XC=4 (note: Ex1-type series check)', abs(3 + J * (8 - 4)), 5)

# Q3: below resonance (L = 1 mH, C = 1 uF, w0 = 31623, test w = 1e4)
L3, C3, w3 = 1e-3, 1e-6, 1e4
Zser = 5 + 1j * (w3 * L3 - 1 / (w3 * C3)); Ypar = 1 / 5 + 1j * (w3 * C3 - 1 / (w3 * L3))
check('Q3 series below resonance: X < 0 (capacitive)', np.sign(Zser.imag), -1)
check('Q3 parallel below resonance: B < 0, so Im Z > 0 (inductive)', np.sign((1 / Ypar).imag), 1)
w3h = 1e5                                              # above resonance both flip
check('Q3 series above resonance: X > 0', np.sign((5 + 1j * (w3h * L3 - 1 / (w3h * C3))).imag), 1)
check('Q3 parallel above resonance: Im Z < 0 (capacitive)', np.sign((1 / (1 / 5 + 1j * (w3h * C3 - 1 / (w3h * L3)))).imag), -1)

# Q5: parallel R, L, C across V = 1/0:  I_R = 6, I_L = 14 (lagging), I_C = 6 (leading)
I5 = 6 + (-1j * 14) + (1j * 6)
check('Q5 source current |6 - j14 + j6| (A)', abs(I5), 10)
check('Q5 wrong: arithmetic sum of readings', 6 + 14 + 6, 26); check('Q5 wrong: root of sum of squares', np.sqrt(6 ** 2 + 14 ** 2 + 6 ** 2), 16.37, 1e-2)

# ============================================================ power and power-factor correction
Pw, pf1, pf2, V, f = 10e3, 0.8, 0.95, 230.0, 50.0
w = 2 * np.pi * f
Q1, Q2 = Pw * np.tan(np.arccos(pf1)), Pw * np.tan(np.arccos(pf2))
Cc = (Q1 - Q2) / (w * V ** 2)
check('Ex2 Q1 (kvar)', Q1 / k, 7.5); check('Ex2 Q2 (kvar)', Q2 / k, 3.287, 1e-3)
check('Ex2 capacitor for 0.95 (uF)', Cc / u, 253.5, 0.1)
check('Ex2 line current before (A)', Pw / (V * pf1), 54.35, 0.01); check('Ex2 line current after (A)', Pw / (V * pf2), 45.77, 0.01)
Cunity = Pw * np.tan(np.arccos(pf1)) / (w * V ** 2)
check('Q8 capacitor for unity pf (uF)', Cunity / u, 451.3, 0.1)
check('P2 5 kW at 0.6 -> unity (uF)', 5e3 * np.tan(np.arccos(0.6)) / (w * V ** 2) / u, 401.2, 0.1)
check('Q6 apparent power for 3 kW + 4 kvar', np.hypot(3, 4), 5); check('Q6 pf', 3 / 5, 0.6)
S1, S2 = 6 + 4.5j, 8 - 6j                             # 6 kW at 0.8 lagging, 8 kW at 0.8 leading
check('Q10 total |S| (kVA)', abs(S1 + S2), 14.08, 5e-3); check('Q10 sum of |S| (wrong)', abs(S1) + abs(S2), 17.5)
check('Q10 S1 apparent', abs(S1), 7.5); check('Q10 S2 apparent', abs(S2), 10)
check('Q10 wrong: |S2| - |S1|', abs(S2) - abs(S1), 2.5)
check('Q10 source power factor (leading)', (S1 + S2).real / abs(S1 + S2), 0.9943, 1e-4)
check('note: rms of 3 + 4cos(wt)', np.sqrt(3 ** 2 + 4 ** 2 / 2), 4.1231, 1e-4)

# Q7: V = 200/0, I = 5/-30 -> S = V I*
S7 = 200 * np.conj(5 * np.exp(-1j * np.radians(30)))
check('Q7 P (W)', S7.real, 866.03, 1e-2); check('Q7 Q (var)  (positive = inductive)', S7.imag, 500, 1e-9)
S7wrong = 200 * (5 * np.exp(-1j * np.radians(30)))
check('Q7 wrong (no conjugate): Q (var)', S7wrong.imag, -500, 1e-9)

# Q8: 2 kW at 0.8 lagging, 230 V, 50 Hz -> unity pf
C8 = 2e3 * np.tan(np.arccos(0.8)) / (w * V ** 2)
check('Q8 capacitor for unity pf (uF)', C8 / u, 90.26, 0.01)
check('Q8 wrong: Q = P sin(phi) instead of P tan(phi) (uF)', 2e3 * 0.6 / (w * V ** 2) / u, 72.2, 0.05)
check('Q8 wrong: peak voltage used (uF)', 2e3 * 0.75 / (w * (V * np.sqrt(2)) ** 2) / u, 45.13, 0.01)

# Q9: 10 kW at 0.8 lagging on 230 V; add the capacitor for 0.95 -> load current unchanged, source current falls
S9 = 10e3 + 7.5e3j
Zload = V ** 2 / np.conj(S9)
Iload = V / Zload
Isrc_before = Iload
Isrc_after = Iload + 1j * w * Cc * V
check('Q9 real power from the source, before (kW)', (V * np.conj(Isrc_before)).real / k, 10, 1e-9)
check('Q9 real power from the source, after (kW)', (V * np.conj(Isrc_after)).real / k, 10, 1e-9)
check('Q9 |I_source| falls from (A)', abs(Isrc_before), 54.35, 0.01); check('Q9 ... to (A)', abs(Isrc_after), 45.77, 0.01)
check('Q9 current through the load is unchanged (A)', abs(V / Zload), abs(Iload), 1e-12)
check('Q9 reactive power from the source falls (kvar)', (V * np.conj(Isrc_after)).imag / k, 3.287, 1e-3)

# Q11: i = 2 + 4cos(100t) + 3 sin(300t) through 5 ohm
T11 = 2 * np.pi / 100
t11 = np.linspace(0, T11, 600001)[:-1]
i11 = 2 + 4 * np.cos(100 * t11) + 3 * np.sin(300 * t11)
check('Q11 average power (W) by direct integration', np.mean(i11 ** 2 * 5), 82.5, 1e-6)
check('Q11 I_rms^2 = 4 + 8 + 4.5', 2 ** 2 + 4 ** 2 / 2 + 3 ** 2 / 2, 16.5)
check('Q11 wrong: amplitudes added, (2+4+3)^2 * 5', (2 + 4 + 3) ** 2 * 5, 405)
check('Q11 wrong: DC ignored', (4 ** 2 / 2 + 3 ** 2 / 2) * 5, 62.5)

# P1: Z1 = 3+j4 and Z2 = 6-j8 in parallel across 100 V rms
Vp = 100.0
Ip = Vp * (1 / (3 + 4j) + 1 / (6 - 8j))
Sp = Vp * np.conj(Ip)
check('P1 |I| (A)', abs(Ip), 19.70, 0.01); check('P1 P (W)', Sp.real, 1800, 1e-6); check('P1 Q (var)', Sp.imag, 800, 1e-6)
check('P1 pf', Sp.real / abs(Sp), 0.9138, 1e-4)

# P5: v = 20 sin(100 t + 30 deg) across 20 ohm + 0.2 H
Z5 = 20 + J * 100 * 0.2
check('P5 |Z|', abs(Z5), 28.284, 1e-3); check('P5 amplitude of i (A)', 20 / abs(Z5), 0.7071, 1e-4)
check('P5 phase of i (deg) = 30 - 45', 30 - np.degrees(np.angle(Z5)), -15)

# ============================================================ AC maximum power
Zth, Vth = 3 + 4j, 10.0
Pconj = Vth ** 2 / (4 * Zth.real)
check('Q12/Q13 P_max (W) with a conjugate load  V^2/(4 R_th)', Pconj, 8.333, 1e-3)
RL = np.linspace(0.01, 20, 200001)
P_RL = Vth ** 2 * RL / ((Zth.real + RL) ** 2 + Zth.imag ** 2)
check('Q12 best purely resistive R_L = |Z_th|', RL[np.argmax(P_RL)], 5, 1e-3)
check('Q12 power at R_L = 5 (W)', P_RL[np.argmin(abs(RL - 5))], 6.25, 1e-3)
check('Q12 max over R_L (W)', P_RL.max(), 6.25, 1e-6)
check('AC: power at R_L = 3 (W)', Vth ** 2 * 3 / ((3 + 3) ** 2 + 16), 5.769, 1e-3)
check('Q13 (A) false: Z_L = Z_th (not the conjugate) gives only (W)', Vth ** 2 * 3 / abs(2 * Zth) ** 2, 3.0, 1e-9)
XL = np.linspace(-10, 5, 150001)                      # Q13: Z_th = 4 + j3, R_L = 6 fixed, X_L adjustable
P_X = 1.0 / ((4 + 6) ** 2 + (3 + XL) ** 2)
check('Q13 (C) best X_L with R_L fixed (= -X_th)', XL[np.argmax(P_X)], -3, 1e-3)

# ============================================================ resonance
# Ex 3: series RLC, L = 1 mH, C = 10 uF, R = 1 ohm
L_, C_, R_ = 1 * m, 10 * u, 1.0
w0 = 1 / np.sqrt(L_ * C_); Q = w0 * L_ / R_
check('Ex3 w0', w0, 1e4); check('Ex3 Q', Q, 10); check('Ex3 BW = R/L (rad/s)', R_ / L_, 1000)
ws = np.linspace(8000, 12000, 400001)
Zs = R_ + J * (ws * L_ - 1 / (ws * C_))
I_rel = R_ / abs(Zs)
half = ws[I_rel >= 1 / np.sqrt(2)]
check('Ex3 lower half-power w1', half[0], 9512.5, 0.05); check('Ex3 upper half-power w2', half[-1], 10512.5, 0.05)
check('Ex3 w2 - w1 = BW exactly', half[-1] - half[0], 1000, 0.1)
check('Ex3 sqrt(w1 w2) = w0', np.sqrt(half[0] * half[-1]), 1e4, 0.1)
check('Ex3 closed form w2', w0 * (np.sqrt(1 + 1 / (4 * Q ** 2)) + 1 / (2 * Q)), 10512.5, 0.05)
i_half = R_ / (R_ + J * (half[0] * L_ - 1 / (half[0] * C_)))
check('Ex3 phase at w1 (deg)', np.degrees(np.angle(i_half)), 45, 0.05)
# voltage magnification at resonance
check('P3 Q = w0 L / R   (L=0.1, C=10uF, R=10)', (1 / np.sqrt(0.1 * 10 * u)) * 0.1 / 10, 10, 1e-9)
check('P3 V_C at resonance (V) for a 5 V source', 10 * 5, 50)
check('P3 I at resonance (A)', 5 / 10, 0.5)
check('P3 BW = R/L (rad/s)', 10 / 0.1, 100)
# Q14: R = 5, L = 20 mH, C = 2 uF, 2 V rms at resonance
w14 = 1 / np.sqrt(20e-3 * 2e-6); Q14 = w14 * 20e-3 / 5
check('Q14 w0 (rad/s)', w14, 5000, 1e-6); check('Q14 Q', Q14, 20, 1e-9)
I14 = 2 / 5; XC14 = 1 / (w14 * 2e-6)
check('Q14 V_C = I X_C (V)', I14 * XC14, 40, 1e-9); check('Q14 V_C = Q V_s (V)', Q14 * 2, 40, 1e-9)

# Q15 (B): in a series RLC at resonance the total stored energy is constant in time
L15, C15, R15, Vm15 = 20e-3, 2e-6, 5.0, 2 * np.sqrt(2)
w15 = 1 / np.sqrt(L15 * C15)
t15 = np.linspace(0, 4 * 2 * np.pi / w15, 4001)
Im15 = Vm15 / R15
i15 = Im15 * np.cos(w15 * t15); vC15 = Im15 / (w15 * C15) * np.sin(w15 * t15)
Wtot = 0.5 * L15 * i15 ** 2 + 0.5 * C15 * vC15 ** 2
check('Q15 (B) W_L + W_C is constant: spread over time (J)', Wtot.max() - Wtot.min(), 0, 1e-12)
check('Q15 (B) constant value = 1/2 L Im^2 (mJ)', Wtot[0] / m, 0.5 * L15 * Im15 ** 2 / m, 1e-9)
check('Q15 (C) false: V_C / V_s = Q, not 1', (Im15 / (w15 * C15)) / Vm15, 20, 1e-9)

check('Q19-style check: Q = f0/BW', 10 / 5, 2)
# Q16: f0 = 1 MHz, Q = 50
check('Q16 BW = f0/Q (kHz)', 1000 / 50, 20)
# Q19: f0 = 10 kHz, BW = 5 kHz -> Q = 2
Q19 = 10 / 5
f2_ = 10 * (np.sqrt(1 + 1 / (4 * Q19 ** 2)) + 1 / (2 * Q19)); f1_ = 10 * (np.sqrt(1 + 1 / (4 * Q19 ** 2)) - 1 / (2 * Q19))
check('Q19 upper half-power frequency (kHz)', f2_, 12.808, 1e-3); check('Q19 lower half-power frequency (kHz)', f1_, 7.808, 1e-3)
check('Q19 f2 - f1 = BW (kHz)', f2_ - f1_, 5, 1e-9); check('Q19 sqrt(f1 f2) = f0 (kHz)', np.sqrt(f1_ * f2_), 10, 1e-9)
fs_ = np.linspace(5, 15, 1000001)
Irel = 1 / np.sqrt(1 + Q19 ** 2 * (fs_ / 10 - 10 / fs_) ** 2)
hp = fs_[Irel >= 1 / np.sqrt(2)]
check('Q19 numerical upper half-power point (kHz)', hp[-1], 12.808, 1e-3); check('Q19 numerical lower half-power point (kHz)', hp[0], 7.808, 1e-3)
check('Q19 wrong: f0 + BW/2 (kHz)', 10 + 5 / 2, 12.5)

# Ex 4: practical tank, coil L = 1 mH with R_L = 10 ohm in series, C = 1 uF in parallel
Lt, Rt, Ct = 1 * m, 10.0, 1 * u
wr = np.sqrt(1 / (Lt * Ct) - (Rt / Lt) ** 2)
Y = lambda w: 1j * w * Ct + 1 / (Rt + 1j * w * Lt)
check('Ex4 unity-pf frequency (rad/s)', wr, 30000, 1e-6)
check('Ex4 Im Y at that frequency', Y(wr).imag, 0, 1e-12)
check('Ex4 dynamic impedance L/(C R_L) (ohm)', Lt / (Ct * Rt), 100)
check('Ex4 1/Re Y at unity pf (ohm)', 1 / Y(wr).real, 100, 1e-6)
w_ = np.linspace(20000, 40000, 400001)
zmax = w_[np.argmax(1 / abs(Y(w_)))]
print(f'      peak |Z| of the tank is at {zmax:.0f} rad/s (unity-pf frequency is {wr:.0f}; w0 = {1 / np.sqrt(Lt * Ct):.0f})')
# Q17: coil L = 5 mH, R_L = 40 ohm in parallel with C = 2 uF
L17, R17, C17 = 5e-3, 40.0, 2e-6
w17 = np.sqrt(1 / (L17 * C17) - (R17 / L17) ** 2)
Y17 = lambda ww: 1j * ww * C17 + 1 / (R17 + 1j * ww * L17)
check('Q17 unity-pf frequency (rad/s)', w17, 6000, 1e-6)
check('Q17 Im Y at that frequency', Y17(w17).imag, 0, 1e-12)
check('Q17 dynamic impedance L/(C R_L) (ohm)', L17 / (C17 * R17), 62.5, 1e-9); check('Q17 1/Re Y (ohm)', 1 / Y17(w17).real, 62.5, 1e-9)
check('Q17 wrong: 1/sqrt(LC) (rad/s)', 1 / np.sqrt(L17 * C17), 10000, 1e-6)
check('Q17 Im Y at 1/sqrt(LC) is NOT zero (S)', Y17(1 / np.sqrt(L17 * C17)).imag, 7.805e-3, 1e-5)
# Q18: R = 10, L, C in parallel across an ideal 10 V source: the source current is minimum at w0
R18, L18, C18, V18 = 10.0, 1e-3, 1e-6, 10.0
w18 = 1 / np.sqrt(L18 * C18)
ww = np.linspace(0.2 * w18, 5 * w18, 2000001)
I18 = abs(V18 * (1 / R18 + 1j * (ww * C18 - 1 / (ww * L18))))
check('Q18 source current is minimum at w0 (ratio w/w0)', ww[np.argmin(I18)] / w18, 1.0, 1e-4)
check('Q18 minimum source current = V/R (A)', I18.min(), 1.0, 1e-6)
check('Q18 I_L + I_C = 0 at w0 (A)', abs(V18 / (1j * w18 * L18) + 1j * w18 * C18 * V18), 0, 1e-6)
# P4
L4, R4, C4 = 2 * m, 4.0, 5 * u
w4 = np.sqrt(1 / (L4 * C4) - (R4 / L4) ** 2)
check('P4 w_r (rad/s)', w4, 9797.96, 0.01); check('P4 Z_d = L/(C R)', L4 / (C4 * R4), 100)

# ============================================================ locus of Z (2022 Q38)
R1, R2 = 2.0, 3.0
wsw = np.logspace(-3, 6, 200001) / (R2 * 1e-6)
Zl = R1 + R2 / (1 + 1j * wsw * R2 * 1e-6)
check('locus: Z(0) (k ohm)', Zl[0].real, 5, 1e-3); check('locus: Z(inf) (k ohm)', Zl[-1].real, 2, 1e-3)
check('locus: max -Im(Z) = R2/2', (-Zl.imag).max(), 1.5, 1e-4)
check('locus: circle centre (R1 + R2/2, 0)', np.mean([np.abs(Zl[i] - (R1 + R2 / 2)) for i in range(0, len(Zl), 5000)]), 1.5, 5e-3)
R1b, R2b = 1.0, 4.0
Zl2 = R1b + R2b / (1 + 1j * wsw * R2b * 1e-6)
check('Q20 Z(0) (k ohm)', Zl2[0].real, 5, 1e-3); check('Q20 Z(inf) (k ohm)', Zl2[-1].real, 1, 1e-3)
check('Q20 max -Im Z = R2/2 (k ohm)', (-Zl2.imag).max(), 2, 1e-3)
check('Q20 all Im Z <= 0 (lower half-plane)', float((Zl2.imag <= 1e-12).all()), 1.0, 0.5)

# ============================================================ past-year questions
# 2019 Q30 (key C): v = 2 sin(1000 t), R = 1 k, C = 1 uF.  Nodes: T=1 (top vertex), BL=0 (ground), BR=2, O=3.
Rr, Zc = 1e3, 1 / (1j * 1000 * 1 * u)
net = [('R', 1, 0, Rr), ('R', 1, 2, Rr), ('R', 2, 0, Rr), ('Z', 1, 3, Zc), ('Z', 0, 3, Zc), ('Z', 2, 3, Zc)]
V, Iv = solve(net + [('V', 1, 0, 2 + 0j, 'vs')])
i_mA = -Iv['vs'] / m                                   # phasor with a sine reference: i = Re{I e^{jwt}} for sin-type waves
check('2019 Q30 i(t) = 3 sin + cos: real part (sin coeff, mA)  [key C]', i_mA.real, 3, 1e-9)
check('2019 Q30 imaginary part (cos coeff, mA)', i_mA.imag, 1, 1e-9)

# 2020 Q16 (key 2.80 to 2.85 H): i = 10 cos(5t - pi/4) A from 200 cos(5t) V
Zm = 200 / 10
phi = np.pi / 4
Rq, Xq = Zm * np.cos(phi), Zm * np.sin(phi)
check('2020 Q16 R (ohm)', Rq, 14.142, 1e-3); check('2020 Q16 L = X/w (H)  [key 2.80-2.85]', Xq / 5, 2.828, 1e-3)

# 2020 Q28 (key C = 2.38 /143.63 deg A)
Zq = 80 - 35j
node = [('V', 1, 0, 120 * np.exp(-1j * np.pi / 2), 'v1'), ('V', 2, 0, 120 * np.exp(-1j * np.pi / 6), 'v2'),
        ('Z', 1, 0, Zq), ('Z', 0, 2, Zq), ('Z', 1, 2, Zq)]
_, Iq = solve(node)
Iwire = Iq['v1'] + Iq['v2']
mag, ang = pol(Iwire)
check('2020 Q28 |I| (A)', mag, 2.38, 5e-3); check('2020 Q28 angle (deg)  [key 143.63]', ang, 143.63, 5e-3)
check('2020 Q28 shortcut -(V1+V2)/Z: |I|', abs((120 * np.exp(-1j * np.pi / 2) + 120 * np.exp(-1j * np.pi / 6)) / Zq), 2.38, 5e-3)
check('2020 Q28 sum of source phasors: magnitude', abs(120 * np.exp(-1j * np.pi / 2) + 120 * np.exp(-1j * np.pi / 6)), 207.85, 5e-3)

# 2022 Q24 (key C): same current in a series R-C  (conduction = displacement)
print('ok  2022 Q24: series elements carry the same current -> 2 sin(t + pi/2)  [key C]')

# 2022 Q38 (key A): R1 = 2 k, R2 = 3 k  (checked above in the locus block)
print('ok  2022 Q38: Z(0) = 5, Z(inf) = 2, max -Im = 1.5  ->  R1 = 2 k, R2 = 3 k  [key A]')

# 2022 Q39 (key B = inductor 1 H): V = sin t, 1 ohm in series with Z, |I| = 1/sqrt(2), zero crossing (rising) at t = pi/4
for X, name in ((1.0, 'inductor 1 H'), (-1.0, 'capacitor 1 F')):
    Iph = 1 / (1 + 1j * X)
    t = np.linspace(0, 2 * np.pi, 100001)
    it = abs(Iph) * np.sin(t + np.angle(Iph))
    cross = t[np.argmin(abs(it - 0) + (np.gradient(it) < 0) * 10)]
    print(f'      {name}: |I| = {abs(Iph):.4f},  first rising zero-crossing of i(t) at t = {cross:.4f}   (pi/4 = {np.pi / 4:.4f})')
assert abs(abs(1 / (1 + 1j)) - 1 / np.sqrt(2)) < 1e-12
check('2022 Q39 lag angle of the inductor case (deg)', np.degrees(np.angle(1 / (1 + 1j))), -45)

# 2023 Q18 (key D): Q = w0 L / R = 1000 at w0 = 1e6, L = 1 uH, C = 1 uF
for Rv in (1.0, 0.1, 0.01, 0.001):
    print(f'      R = {Rv:<6g} -> Q = {1e6 * 1e-6 / Rv:g}')
check('2023 Q18 Q for R = 0.001  [key D]', 1e6 * 1e-6 / 0.001, 1000)
check('2023 Q18 w0 = 1/sqrt(LC)', 1 / np.sqrt(1e-6 * 1e-6), 1e6)

# 2025 Q20 (key A): V = 1 /90 deg, Y_C = j0.25, Y_L = -j0.1, Y_R = 0.2
Vq = 1j
for nm, Yv, want in (('i_C', 0.25j, (0.25, 180)), ('i_L', -0.1j, (0.1, 0)), ('i_R', 0.2, (0.2, 90))):
    mg, an = pol(Yv * Vq)
    an = an % 360
    assert abs(mg - want[0]) < 1e-12 and abs(an - want[1]) < 1e-9, (nm, mg, an)
print('ok  2025 Q20 i_C = 0.25 /180, i_L = 0.1 /0, i_R = 0.2 /90   [key A]')

# 2025 Q39 (key A = 25 uF): rms 25 V and 5 A -> |Z| = 5 = R -> resonance at w = 200
check('2025 Q39 C = 1/(w^2 L) (uF)  [key 25]', 1 / (200 ** 2 * 1) / u, 25)
Zb = 5 + 1j * (200 * 1 - 1 / (200 * 25 * u))
check('2025 Q39 |Z| of the branch', abs(Zb), 5); check('2025 Q39 V_rms / |Z| = 5 A', 25 / abs(Zb), 5)

# 2026 Q31 (key 71.50 to 72.50 mW)
Vm_ = 12.0
check('2026 Q31 P = (Vm/sqrt2)^2 / R (mW)  [key 71.5-72.5]', (Vm_ / np.sqrt(2)) ** 2 / 1e3 / m, 72, 1e-9)
w0q = 1 / np.sqrt(2.2 * m * 1 * u)
Ic, Il = 1j * w0q * 1 * u * Vm_, Vm_ / (1j * w0q * 2.2 * m)
check('2026 Q31 I_C + I_L at resonance (mA)', abs(Ic + Il) / m, 0, 1e-9)
check('2026 Q31 resonant frequency (rad/s)', w0q, 21320, 1)

# 2026 Q39 (key B = 1): L = 1 uH, C = 1 uF at w = 1e6 -> X_L = X_C = 1 ohm ; I_C leads, I_L lags, theta1 + theta2 = 90
w39 = 2 * np.pi * 159.15e3
XL39, XC39 = w39 * 1e-6, 1 / (w39 * 1e-6)
check('2026 Q39 X_L (ohm)', XL39, 1, 1e-3); check('2026 Q39 X_C (ohm)', XC39, 1, 1e-3)
for RC_, RL_ in ((0.5, 2.0), (4.0, 0.25), (1.0, 1.0)):
    th1 = np.degrees(np.arctan(XC39 / RC_)); th2 = np.degrees(np.arctan(XL39 / RL_))
    check(f'2026 Q39 theta1 + theta2 for R_C={RC_}, R_L={RL_} (deg)', th1 + th2, 90, 1e-2)
th = np.degrees(np.arctan(1 / 2.0) + np.arctan(1 / 1.0))
print(f'      (R_C R_L = 2 would give {th:.1f} deg, not 90)')
check('2026 Q39 R_C x R_L = L/C (ohm^2)', 1e-6 / 1e-6, 1)

print('\nall Day 4 checks passed')
