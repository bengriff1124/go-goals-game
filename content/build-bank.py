#!/usr/bin/env python3
"""Packs the 17 goal files into one bank the game fetches at runtime.

The answer payload (correct index, explanations, action) is XOR-scrambled and
base64'd. That is a SPEED BUMP, not security: anyone who reads the game's source
can reverse it in a minute. It only stops a student idly opening the JSON in a
browser tab and reading 'correctIndex' off the screen. Real secrecy needs the
answers held server-side and checked over the network.
"""
import json, base64, pathlib, sys

KEY = b'go-goals-2030'
HERE = pathlib.Path(__file__).parent

def scramble(text: str) -> str:
    raw = text.encode('utf-8')
    out = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(raw))
    return base64.b64encode(out).decode('ascii')

bank = {'v': 1, 'goals': {}, 'sources': {}}
total = 0
for g in range(1, 18):
    f = HERE / f'goal-{g:02d}.json'
    data = json.loads(f.read_text(encoding='utf-8'))
    for key, meta in data.get('sources', {}).items():
        bank['sources'][key] = meta
    items = []
    for q in data['questions']:
        answer = {
            'c': q['correctIndex'],
            'w': q['whyCorrect'],
            'x': q['whyWrong'],
            'a': q['action'],
            's': q['src'],
        }
        items.append({
            'i': q['id'],
            'p': q['prompt'],
            'o': q['options'],
            'k': scramble(json.dumps(answer, ensure_ascii=False, separators=(',', ':'))),
        })
    bank['goals'][str(g)] = items
    total += len(items)

out = HERE / 'bank.json'
out.write_text(json.dumps(bank, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(f'wrote {out} — {total} questions, {len(bank["sources"])} sources, {out.stat().st_size/1024:.0f} KB')
