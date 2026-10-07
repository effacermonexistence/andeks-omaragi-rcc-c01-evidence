#!/usr/bin/env python3
"""Refresh publication-only metadata; never import or execute assessed RCC code."""
from __future__ import annotations
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '329b46add38a1770b484bdf90e9db458407a15e1'
REPO = 'effacermonexistence/andeks-omaragi-rcc-c01-evidence'
REGISTER = 'ARTIFACT_REGISTER.csv'
MANIFEST = 'PACKAGE_SHA256SUMS.txt'
PROTECTED = ('evidence', 'provenance/source_acquisition.json',
             'provenance/public_copy_transformations.json', 'scripts/verify_package.py')


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(['git', *args], cwd=ROOT, check=check, capture_output=True)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    if git('diff', '--quiet', BASE, '--', *PROTECTED, check=False).returncode != 0:
        raise RuntimeError('Pre-existing evidence/acquisition/validator changed; stop publication')
    names = sorted(x for x in git('ls-files', '-z').stdout.decode().split('\0') if x)
    if not names or REGISTER not in names or MANIFEST not in names:
        raise RuntimeError('Expected tracked publication tree missing')
    with (ROOT / REGISTER).open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        old = list(reader)
    by_path = {r['package_path']: r for r in old}
    if len(by_path) != len(old):
        raise RuntimeError('Duplicate registry paths')
    if set(by_path) - set(names):
        raise RuntimeError('This revision must not delete existing publication files')
    now = datetime.now(timezone.utc).isoformat()
    used = {r['artifact_id'] for r in old}
    counter = 1
    rows = []
    unchanged_evidence = 0
    for name in names:
        path = ROOT / name
        data = path.read_bytes()
        previous = by_path.get(name)
        if previous and previous['evidence_temporality'] == 'PRE_EXISTING_BEFORE_2026-10-06':
            if digest(data) != previous['public_sha256']:
                raise RuntimeError(f'Historical public bytes changed: {name}')
            rows.append(previous)
            unchanged_evidence += 1
            continue
        base_read = git('show', f'{BASE}:{name}', check=False)
        if previous and base_read.returncode == 0 and base_read.stdout == data and name not in (REGISTER, MANIFEST):
            rows.append(previous)
            continue
        row = dict(previous) if previous else {k: '' for k in fields}
        if not previous:
            while f'R{counter:03d}' in used:
                counter += 1
            row['artifact_id'] = f'R{counter:03d}'
            used.add(row['artifact_id'])
            counter += 1
        row.update({
            'andeks_section': 'INDEX', 'package_path': name,
            'original_repository': REPO, 'original_path': name,
            'pinned_source_commit': 'NOT_APPLICABLE_POST_REQUEST',
            'original_timestamp': now,
            'timestamp_kind': 'publication revision UTC; not historical system execution time',
            'artifact_type': path.suffix.lstrip('.') or 'text',
            'evidence_temporality': 'POST_REQUEST_INDEX_OR_PUBLICATION_MATERIAL',
            'publication_form': 'NEW_INDEX_OR_INTEGRITY_MATERIAL',
            'reason_for_inclusion': 'Request-aligned explanation or publication integrity only; not new RCC behavior.',
            'source_sha256': 'NOT_APPLICABLE_POST_REQUEST',
            'public_sha256': digest(data),
            'source_git_blob_sha1': 'NOT_APPLICABLE_POST_REQUEST',
            'source_bytes': 'NOT_APPLICABLE_POST_REQUEST',
            'public_bytes': str(len(data)),
            'source_selector': f'Publication revision from package commit {BASE}; no historical run implied',
            'last_source_path_commit': 'NOT_APPLICABLE_POST_REQUEST',
        })
        if name == REGISTER:
            row['public_sha256'] = 'SELF_REFERENCE_EXCLUDED'
            row['public_bytes'] = 'SELF_REFERENCE_EXCLUDED'
        if name == MANIFEST:
            row['public_sha256'] = 'MANIFEST_SELF_EXCLUDED'
            row['public_bytes'] = 'SELF_REFERENCE_EXCLUDED'
        rows.append(row)
    with (ROOT / REGISTER).open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    lines = [f'{digest((ROOT / n).read_bytes())}  {n}' for n in names if n != MANIFEST]
    (ROOT / MANIFEST).write_text('\n'.join(lines) + '\n', encoding='utf-8')
    ids = re.findall(r'^\| ([A-FP]\d+) \|', (ROOT / '08_REQUIREMENT_CROSSWALK.md').read_text(), re.M)
    expected = {f'{letter}{i}' for letter, n in {'A':7,'B':7,'C':8,'D':4,'E':6,'F':4,'P':9}.items() for i in range(1,n+1)}
    if len(ids) != 45 or set(ids) != expected:
        raise RuntimeError('Crosswalk does not contain exactly the 45 requested IDs')
    print(json.dumps({'check':'publication_metadata_only', 'status':'PASS', 'files':len(names),
                      'requirements':len(ids), 'unchanged_historical_evidence_rows':unchanged_evidence,
                      'protected_paths_unchanged':True, 'assessed_code_executed':False}, indent=2))


if __name__ == '__main__':
    main()
