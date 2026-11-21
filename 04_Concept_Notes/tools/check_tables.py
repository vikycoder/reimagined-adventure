"""Lint markdown tables: no row may have more cells than the header (GitHub pads short rows and drops extra cells).

GitHub-flavoured markdown splits a table row at every unescaped `|`, even inside a `code span`, so a cell such as
`|x|` silently breaks the table (extra cells are dropped).  Escape pipes in table cells as `\\|`.

Run:  python3 check_tables.py FILE.md [FILE2.md ...]     (exit status 1 if any table is inconsistent)
Also checks that every ![](image) link points to an existing file (relative to the markdown file).
"""
import pathlib
import re
import sys


def split_cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'):
        s = s[:-1]
    cells, cur, i = [], '', 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s) and s[i + 1] == '|':
            cur += '\\|'
            i += 2
            continue
        if c == '|':
            cells.append(cur)
            cur = ''
        else:
            cur += c
        i += 1
    cells.append(cur)
    return cells


def check(path):
    problems = []
    lines = path.read_text(encoding='utf-8').splitlines()
    in_fence = False
    block = []                                   # (line number, text) of the current table
    def flush():
        if len(block) >= 2:
            header = split_cells(block[0][1])
            sep = split_cells(block[1][1])
            if not all(re.fullmatch(r'\s*:?-{1,}:?\s*', c) for c in sep):
                problems.append(f'{path}:{block[1][0]}: second row of a table is not a separator row')
            n = len(header)
            if len(sep) != n:
                problems.append(f'{path}:{block[1][0]}: separator has {len(sep)} cells, header has {n}')
            for ln, text in block[2:]:
                m = len(split_cells(text))
                if m > n:                                # fewer cells are padded by GitHub; extra cells are silently dropped
                    problems.append(f'{path}:{ln}: row has {m} cells, header has {n}: {text.strip()[:90]}')
        block.clear()
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith('```'):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.lstrip().startswith('|'):
            block.append((i, line))
        else:
            flush()
    flush()
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', line):
            target = (path.parent / m.group(1)).resolve()
            if not target.exists():
                problems.append(f'{path}:{i}: missing image {m.group(1)}')
    return problems


if __name__ == '__main__':
    bad = []
    for arg in sys.argv[1:]:
        bad += check(pathlib.Path(arg))
    for b in bad:
        print(b)
    print(f'{len(sys.argv) - 1} file(s) checked, {len(bad)} problem(s)')
    sys.exit(1 if bad else 0)
