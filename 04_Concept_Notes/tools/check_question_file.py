"""Structural checker for the Day-N question files and notes.

    python3 check_question_file.py Day02_Conceptual_Questions.md [more.md ...]

Checks: every image link exists; the number of '### Qn · TYPE' questions equals the number of
solutions and answer-key rows; the key matches the 'Answer:' line of each solution; the answer
shape fits the question type (MCQ: one letter, MSQ: letters, NAT: a number); <details> blocks balance.
"""
import os
import re
import sys
from collections import Counter


def norm(x):
    """Leading answer token: 'B, C, D' -> 'B,C,D'; '5.33 (range 5.32 to 5.34)' -> '5.33'; '2 A' -> '2'."""
    x = x.strip().replace('\u2212', '-')
    m = re.match(r'[A-D](?:\s*,\s*[A-D])*\b', x)
    if m:
        return re.sub(r'\s+', '', m.group(0))
    m = re.match(r'-?[\d.]+(?:/[\d.]+)?', x)
    return m.group(0) if m else x


def check(path):
    s = open(path, encoding='utf-8').read()
    base = os.path.dirname(os.path.abspath(path))
    problems = []

    for img in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', s):
        if not os.path.exists(os.path.join(base, img)):
            problems.append(f'missing image: {img}')

    qs = re.findall(r'^### Q(\d+) · (MCQ|MSQ|NAT)', s, re.M)
    sols = re.findall(r'<summary><b>Q(\d+) · [^<]*</b></summary>\s*\n\s*\n\*\*Answer: ([^*]+)\*\*', s)
    key = {}
    for a, b, c, d in re.findall(r'^\| (\d+) \| ([^|]+) \| (\d+) \| ([^|]+) \|\s*$', s, re.M):
        key[int(a)] = b.strip()
        key[int(c)] = d.strip()
    for a, b in re.findall(r'^\| (\d+) \| ([^|]+) \|\s*$', s, re.M):      # single-column key tables
        key.setdefault(int(a), b.strip())

    n = len(qs)
    if n == 0:
        problems.append('no questions found')
    if len(sols) != n:
        problems.append(f'{n} questions but {len(sols)} solutions')
    if len(key) != n:
        problems.append(f'{n} questions but {len(key)} answer-key entries')
    if [int(q) for q, _ in qs] != list(range(1, n + 1)):
        problems.append('question numbers are not 1..N in order')

    types = {int(q): t for q, t in qs}
    for q, a in sols:
        q = int(q)
        k = key.get(q)
        if k is None:
            continue
        if norm(a) != norm(k):
            problems.append(f'Q{q}: solution says "{norm(a)}" but key says "{norm(k)}"')
        t = types.get(q)
        a = norm(k)
        if t == 'MCQ' and not re.fullmatch(r'[A-D]', a):
            problems.append(f'Q{q}: MCQ answer shape "{a}"')
        if t == 'MSQ' and not re.fullmatch(r'[A-D](,[A-D])*', a):
            problems.append(f'Q{q}: MSQ answer shape "{a}"')
        if t == 'NAT' and not re.match(r'-?[\d.]+', a):
            problems.append(f'Q{q}: NAT answer shape "{a}"')

    if s.count('<details>') != s.count('</details>'):
        problems.append('unbalanced <details>')

    print(f'{os.path.basename(path)}: {n} questions {dict(Counter(t for _, t in qs))}, '
          f'{len(sols)} solutions, {len(key)} key rows, images ok' if not problems else
          f'{os.path.basename(path)}: PROBLEMS')
    for p in problems:
        print('   -', p)
    return not problems


if __name__ == '__main__':
    ok = all([check(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
