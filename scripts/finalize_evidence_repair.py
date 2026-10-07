#!/usr/bin/env python3
"""Reproduce unchanged components, preserve old evidence, and register new classes."""
from __future__ import annotations
import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b61e2159a7c10a7ce3a604f4c972a671cc9025f6'
REPO = 'effacermonexistence/andeks-omaragi-rcc-c01-evidence'
REGISTER = 'ARTIFACT_REGISTER.csv'
MANIFEST = 'PACKAGE_SHA256SUMS.txt'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    now = datetime.now(timezone.utc).isoformat()
    # Correct OUR new analysis reader to use the actual stored patch schema.
    # The historical patched artifact has final_source, not a patched gate flag.
    analysis = ROOT / 'scripts/reproduce_bounded_adoption.py'
    text = analysis.read_text()
    old = "accepted = row[prefix+'adoption_gate_accepts']"
    new = "accepted = row['adoption_gate_accepts'] if not prefix else row['patched_final_source'] != row['fallback_source']"
    if old in text:
        text = text.replace(old, new)
        text = text.replace("'non_adopted_rows':len(checked)", "'selected_preservation_rows':len(checked), 'selection_rule':('adoption_gate_accepts == false' if not prefix else 'patched_final_source == fallback_source; no patched gate flag is inferred')")
        analysis.write_text(text)
    assert new in analysis.read_text(), 'Unexpected analysis revision'
    subprocess.run([sys.executable, str(analysis)], cwd=ROOT, check=True)

    base_names = git('ls-tree', '-r', '--name-only', BASE).decode().splitlines()
    protected = [n for n in base_names if n.startswith('evidence/') or n in ('provenance/source_acquisition.json', 'provenance/public_copy_transformations.json', 'scripts/verify_package.py')]
    for name in protected:
        assert (ROOT/name).read_bytes() == git('show', f'{BASE}:{name}'), f'Existing protected bytes changed: {name}'
    recovered = []
    for name, selector in (
        ('evidence/source_recovery/bbeh_adoption_core_20260630.py.excerpt.txt', 'L3497 through end; base_default_adoption and evaluate_revas_route'),
        ('evidence/source_recovery/bbeh_types_verifier_20260630.py.excerpt.txt', 'L18-L128; declarations and ExecutorVerifier'),
    ):
        data = (ROOT/name).read_bytes()
        recovered.append({'package_path':name, 'original_repository':'effacermonexistence/omar-benchmark-replay-live-source', 'original_path':'benchmark_executors/bbeh_executor_backed_routing.py', 'source_commit':'b38e6757673173df19216877368e020eb4b51fc5', 'source_git_blob_sha1':'2eb56b207971ac569865d256633c4b2d62f6ef23', 'original_timestamp':'2026-06-30T23:41:59Z', 'timestamp_kind':'source commit time, not independent execution attestation', 'source_selector':selector, 'full_source_sha256':'NOT_COMPUTED; Git blob identity retained', 'public_sha256':digest(data), 'public_bytes':len(data), 'publication_form':'POST_REQUEST_VERBATIM_EXCERPT_OF_PRE_EXISTING_SOURCE'})
    (ROOT/'provenance/source_recovery_20261007.json').write_text(json.dumps({'record_created_at':now, 'classification':'POST_REQUEST_SOURCE_RECOVERY_METADATA', 'prior_acquisition_record_unchanged':True, 'recovered':recovered}, indent=2)+'\n')
    old_rows = list(csv.DictReader((ROOT/REGISTER).open(newline='')))
    fields = list(old_rows[0])
    previous = {r['package_path']:r for r in old_rows}
    names = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts)
    assert set(previous).issubset(names), 'Existing package file deleted'
    used = {r['artifact_id'] for r in old_rows}
    sequence = 1
    rows = []
    source_lookup = {r['package_path']:r for r in recovered}
    unchanged_evidence = 0
    for name in names:
        data = (ROOT/name).read_bytes()
        prior = previous.get(name)
        if prior and prior['evidence_temporality'] == 'PRE_EXISTING_BEFORE_2026-10-06':
            assert digest(data) == prior['public_sha256'], name
            rows.append(prior)
            unchanged_evidence += 1
            continue
        row = dict(prior) if prior else {k:'' for k in fields}
        if not prior:
            while f'S{sequence:03d}' in used:
                sequence += 1
            row['artifact_id'] = f'S{sequence:03d}'
            used.add(row['artifact_id'])
            sequence += 1
        row.update({'andeks_section':'INDEX', 'package_path':name, 'original_repository':REPO, 'original_path':name, 'pinned_source_commit':'NOT_APPLICABLE_POST_REQUEST', 'original_timestamp':now, 'timestamp_kind':'current publication/reproduction record time, not historical execution', 'artifact_type':Path(name).suffix.lstrip('.') or 'text', 'evidence_temporality':'POST_REQUEST_INDEX_OR_PUBLICATION_MATERIAL', 'publication_form':'NEW_INDEX_OR_INTEGRITY_MATERIAL', 'reason_for_inclusion':'Source-linked request response and evidence classification; not an independent finding.', 'source_sha256':'NOT_APPLICABLE_POST_REQUEST', 'public_sha256':digest(data), 'source_git_blob_sha1':'NOT_APPLICABLE_POST_REQUEST', 'source_bytes':'NOT_APPLICABLE_POST_REQUEST', 'public_bytes':str(len(data)), 'source_selector':'', 'last_source_path_commit':'NOT_APPLICABLE_POST_REQUEST'})
        if name in source_lookup:
            source = source_lookup[name]
            row.update({'andeks_section':'A;D;E;F', 'original_repository':source['original_repository'], 'original_path':source['original_path'], 'pinned_source_commit':source['source_commit'], 'original_timestamp':source['original_timestamp'], 'timestamp_kind':source['timestamp_kind'], 'evidence_temporality':'PRE_EXISTING_BEFORE_2026-10-06', 'publication_form':source['publication_form'], 'source_sha256':'NOT_COMPUTED_FULL_SOURCE_GIT_BLOB_RETAINED', 'source_git_blob_sha1':source['source_git_blob_sha1'], 'source_bytes':'NOT_REPORTED', 'source_selector':source['source_selector'], 'last_source_path_commit':source['source_commit'], 'reason_for_inclusion':'Recovered committed June component source; exact selected declaration equivalence is checked separately. Not the entire initial freeze file.'})
        elif name.startswith('reproduction/'):
            record = json.loads(data)
            row.update({'andeks_section':'A;B;C;D;E;F;P8;P9', 'original_timestamp':record['created_at'], 'evidence_temporality':record['classification'], 'publication_form':'NEW_POST_REQUEST_RECORD', 'reason_for_inclusion':('New controlled execution of unchanged original components; not historical or full-product execution.' if name.endswith('unchanged_component_cases.json') else 'New analysis of preserved source/stored data, not a new benchmark or historical run.')})
        if name == REGISTER:
            row['public_sha256'] = row['public_bytes'] = 'SELF_REFERENCE_EXCLUDED'
        elif name == MANIFEST:
            row['public_sha256'] = 'MANIFEST_SELF_EXCLUDED'
            row['public_bytes'] = 'SELF_REFERENCE_EXCLUDED'
        rows.append(row)
    with (ROOT/REGISTER).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    (ROOT/MANIFEST).write_text('\n'.join(f'{digest((ROOT/n).read_bytes())}  {n}' for n in names if n != MANIFEST)+'\n')
    ids = re.findall(r'^\| ([A-FP]\d+) \|', (ROOT/'08_REQUIREMENT_CROSSWALK.md').read_text(), re.M)
    expected = {f'{letter}{i}' for letter,n in {'A':7,'B':7,'C':8,'D':4,'E':6,'F':4,'P':9}.items() for i in range(1,n+1)}
    assert len(ids) == 45 and set(ids) == expected
    subprocess.run([sys.executable, 'scripts/verify_package.py'], cwd=ROOT, check=True)
    print(json.dumps({'status':'PASS', 'files':len(names), 'requirements':len(ids), 'original_evidence_artifacts_preserved':unchanged_evidence, 'recovered_source_excerpts':len(recovered), 'new_component_execution_separately_labeled':True, 'original_assessed_sources_changed':False, 'benchmark_rerun':False, 'provider_calls':0}, indent=2))


if __name__ == '__main__':
    main()
