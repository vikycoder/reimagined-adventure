"""Builds the Networks past-year-question map (2019-2026) used in Day06_Networks_Revision.md.

    python3 build_pyq_map.py            prints the markdown tables

Sources: the PYQ tables of the Day 1-5 notes (question, type, official answer, concept) and the official answer keys in
02_Previous_Year_Papers (marks).  The 2019 and 2021 keys are scanned images; their marks follow the 55-question layout
(Q1-Q25 one mark, Q26-Q55 two marks), which reproduces the 2020 key exactly.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.abspath(os.path.join(HERE, '..'))
PAPERS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '02_Previous_Year_Papers'))

DAYS = {
    1: ('Day01_Circuit_Analysis_Fundamentals.md', 'Circuit analysis', 12),
    2: ('Day02_Network_Theorems.md', 'Network theorems', 9),
    3: ('Day03_Transient_Analysis.md', 'Transients', 8),
    4: ('Day04_Sinusoidal_Steady_State_and_Resonance.md', 'AC steady state and resonance', 8),
    5: ('Day05_Two_Port_Networks.md', 'Two-port networks', 7),
}


def read_rows():
    rows = {}
    for d, (fn, _, _) in DAYS.items():
        s = open(os.path.join(NOTES, fn), encoding='utf-8').read()
        seg = s[s.index('Past-year questions'):]
        table = seg[:seg.index('\n### ')]
        for line in table.splitlines():
            m = re.match(r'^\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$', line)
            if not m or m.group(1) == 'Question':
                continue
            qs = re.findall(r'(\d{4}) Q(\d+) \((MCQ|NAT|MSQ)\)', m.group(1))
            ans, concept = m.group(2), m.group(3)
            if 'solved on Day' in concept:          # cross-reference rows: the question is counted where it was solved
                continue
            parts = [x.strip() for x in ans.split(', ')] if len(qs) > 1 else [ans]
            for (y, q, t), a in zip(qs, parts):
                rows[(int(y), int(q))] = dict(day=d, type=t, ans=a, concept=concept)
    return rows


def key_marks(year):
    out = {}
    txt = subprocess.run(['pdftotext', '-layout', os.path.join(PAPERS, str(year), f'GATE{year}_EC_AnswerKey.pdf'), '-'],
                         capture_output=True, text=True).stdout
    for line in txt.splitlines():
        t = line.split()
        if len(t) >= 6 and t[0].isdigit() and t[-1].isdigit():
            out[int(t[0])] = int(t[-1])
    return out


def build():
    rows = read_rows()
    km = {y: key_marks(y) for y in (2020, 2022, 2023, 2024, 2025, 2026)}
    for (y, q), r in rows.items():
        r['marks'] = km[y][q] if y in km else (1 if q <= 25 else 2)
    return rows


def markdown(rows):
    out = []
    years = sorted({y for y, _ in rows})
    out.append('| Year | Networks questions (number, marks) | Questions | Marks |')
    out.append('|---|---|---|---|')
    for y in years:
        qs = sorted((q, r['marks']) for (yy, q), r in rows.items() if yy == y)
        out.append(f'| {y} | ' + ', '.join(f'Q{q} ({m})' for q, m in qs) + f' | {len(qs)} | {sum(m for _, m in qs)} |')
    out.append(f'| **Total** | | **{len(rows)}** | **{sum(r["marks"] for r in rows.values())}** |')
    out.append('')
    tot = sum(r['marks'] for r in rows.values())
    out.append('| Topic (day) | Questions | Marks | Share of the marks |')
    out.append('|---|---|---|---|')
    for d, (_, name, _) in DAYS.items():
        rs = [r for r in rows.values() if r['day'] == d]
        mk = sum(r['marks'] for r in rs)
        out.append(f'| {name} (Day {d}) | {len(rs)} | {mk} | {100 * mk / tot:.0f} % |')
    out.append('')
    for d, (fn, name, sec) in DAYS.items():
        out.append(f'### Day {d}: {name}')
        out.append('')
        out.append('| Question | Marks | Official answer | Concept it tests | Solved in |')
        out.append('|---|---|---|---|---|')
        for (y, q), r in sorted(rows.items()):
            if r['day'] != d:
                continue
            out.append(f'| {y} Q{q} ({r["type"]}) | {r["marks"]} | {r["ans"]} | {r["concept"]} | [Day {d} §{sec}]({fn}) |')
        out.append('')
    return '\n'.join(out)


if __name__ == '__main__':
    rows = build()
    sys.stdout.write(markdown(rows) + '\n')
    nat = sum(r['type'] == 'NAT' for r in rows.values())
    sys.stderr.write(f'{len(rows)} questions, {sum(r["marks"] for r in rows.values())} marks, NAT {nat}, MCQ {len(rows) - nat}\n')
