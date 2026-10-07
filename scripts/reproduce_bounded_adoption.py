#!/usr/bin/env python3
"""New, dated evidence checks of unchanged source components and stored records.

No model API, no benchmark rerun, no source modification or monkey-patching.
The controlled component inputs below are NEW test inputs, not historical logs.
The boolean analysis executes extracted expressions, not a simulated full product.
"""
from __future__ import annotations
import ast
import hashlib
import itertools
import json
import os
import re
import sys
import types
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reproduction'
OLD = ROOT / 'evidence/source_recovery/bbeh_adoption_core_20260630.py.excerpt.txt'
TYPES = ROOT / 'evidence/source_recovery/bbeh_types_verifier_20260630.py.excerpt.txt'
CURRENT = ROOT / 'evidence/path_identity/bbeh_executor_backed_routing.py.excerpt.txt'
RUNNER = ROOT / 'evidence/upstream_influence/run_bbeh500_full_gold_blind.py'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def marked(path: Path) -> str:
    return path.read_text().split('--- BEGIN VERBATIM SOURCE ---\n', 1)[1].split('--- END VERBATIM SOURCE ---', 1)[0]


def nodes(text: str) -> dict[str, ast.AST]:
    return {node.name: node for node in ast.parse(text).body if isinstance(node, (ast.ClassDef, ast.FunctionDef))}


def canonical(node: ast.AST) -> str:
    return ast.dump(node, annotate_fields=True, include_attributes=False)


def dump(name: str, data: Any) -> None:
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=True) + '\n')


def main() -> None:
    OUT.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    source = CURRENT.read_text()
    type_text = source.split('--- VERBATIM ORIGINAL LINES 18-142 ---\n', 1)[1].split('\n\nclass BaseExecutor:', 1)[0]
    core_text = source[source.index('def base_default_adoption('):]
    current_nodes = {**nodes(type_text), **nodes(core_text)}
    june_type_text, june_core_text = marked(TYPES), marked(OLD)
    june_nodes = {**nodes(june_type_text), **nodes(june_core_text)}
    selected = ['ExecutorInput', 'ExecutorOutput', 'VerifierOutput', 'RouteDecision', 'AdoptionDecision', 'RevasRouteRecord', 'normalize_answer', 'ExecutorVerifier', 'base_default_adoption', 'evaluate_revas_route']
    comparison = {}
    for name in selected:
        left, right = june_nodes[name], current_nodes[name]
        equal = canonical(left) == canonical(right)
        comparison[name] = {'ast_equal': equal, 'june_ast_sha256': sha(canonical(left).encode()), 'current_ast_sha256': sha(canonical(right).encode())}
        if not equal:
            raise AssertionError(f'Core source mismatch: {name}')
    dump('source_equivalence.json', {
        'created_at': now, 'classification': 'POST_REQUEST_SOURCE_ANALYSIS',
        'historical_commit': 'b38e6757673173df19216877368e020eb4b51fc5',
        'current_source_pin': '8976dc12c2d398dd59e4e193c41fa36749dee996',
        'comparison': comparison,
        'input_public_sha256': {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in (OLD, TYPES, CURRENT)},
        'whole_initial_freeze_source_hash_matched': False,
        'boundary': 'Semantic AST equality of listed declarations only; not identity of solver bodies, family policies, entire module, or initial pre-run freeze file.'
    })

    # Compile original component declarations. Bodies, defaults and predicates
    # are unchanged; imports/environment are supplied by this separate runner.
    module = types.ModuleType('_c01_unchanged_original_component')
    module.__dict__.update({'dataclass': dataclass, 'field': field, 'Optional': Optional, 'Any': Any, 're': re})
    sys.modules[module.__name__] = module
    compile_names = ['ExecutorOutput', 'VerifierOutput', 'AdoptionDecision', 'normalize_answer', 'ExecutorVerifier', 'base_default_adoption']
    tree = ast.Module(body=[current_nodes[name] for name in compile_names], type_ignores=[])
    exec(compile(tree, str(CURRENT), 'exec'), module.__dict__)
    cases = [
        ('positive', True, '(B)', 0.99, ['candidate trace'], None, None, True, True),
        ('failed_parse_nonempty', False, '(B)', 0.99, ['ambiguous'], None, 'ambiguous parse', False, False),
        ('failed_verifier_confidence', True, '(B)', 0.50, ['trace'], None, None, False, False),
        ('failed_adoption_confidence', True, '(B)', 0.80, ['trace'], None, None, True, False),
        ('empty_candidate', True, '', 0.99, ['trace'], None, None, False, False),
        ('missing_trace', True, '(B)', 0.99, [], None, None, False, False),
        ('executor_error', True, '(B)', 0.99, ['trace'], 'controlled error input', None, False, False),
    ]
    records = []
    for name, parsed, answer, confidence, trace, error, abstain, expected_verifier, expected_adoption in cases:
        baseline = '(A)'
        candidate = module.ExecutorOutput('boolean expressions', 'controlled_component_input_not_solver_execution', parsed, answer, confidence, trace, error, abstain)
        verifier = module.ExecutorVerifier().verify(candidate)
        adoption = module.base_default_adoption(baseline, candidate, verifier)
        assert verifier.verified is expected_verifier, name
        assert adoption.override_accepted is expected_adoption, name
        assert adoption.final_answer == ('(B)' if expected_adoption else baseline), name
        payload = {'attempt_id': 'component-reproduction-' + name, 'candidate': asdict(candidate), 'route_identity': 'ExecutorVerifier.verify -> base_default_adoption', 'baseline_before': baseline, 'verifier': asdict(verifier), 'adoption': asdict(adoption), 'state_after': adoption.final_answer}
        payload['record_sha256'] = sha(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode())
        records.append(payload)
    dump('unchanged_component_cases.json', {
        'created_at': now, 'workflow_revision': os.getenv('GITHUB_SHA'), 'workflow_run_id': os.getenv('GITHUB_RUN_ID'),
        'classification': 'NEW_POST_REQUEST_EXECUTION_OF_UNCHANGED_EXISTING_COMPONENTS',
        'input_classification': 'NEW_CONTROLLED_TEST_INPUTS_NOT_HISTORICAL_OR_PRODUCTION_RECORDS',
        'source_components': compile_names, 'source_pin': '8976dc12c2d398dd59e4e193c41fa36749dee996',
        'mechanism_modified': False, 'full_module_or_route_executed': False,
        'provider_calls': 0, 'new_benchmark_run': False, 'cases': records,
        'boundary': 'Reproduction begins at existing ExecutorOutput -> verifier -> adoption component. Does not establish solver accuracy, all caller behavior, non-finite inputs, crash recovery, or authenticated persistence.'
    })

    # Exhaustive finite boolean analysis of the ORIGINAL outer selection
    # expressions. This is a source-derived truth table, not 64 product runs.
    outer = current_nodes['evaluate_revas_route']
    assignments = {}
    for node in outer.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments.setdefault(target.id, []).append(node)
    gate = assignments['revas_supported'][0].value
    assert isinstance(gate, ast.Call) and isinstance(gate.func, ast.Name) and gate.func.id == 'all'
    flags = [node.id for node in gate.args[0].elts]
    assert len(flags) == 6
    assert len(assignments['final_answer']) == len(assignments['final_source']) == 1
    rows = []
    for values in itertools.product((False, True), repeat=len(flags)):
        env = dict(zip(flags, values))
        env.update({'all': all, 'base_answer': 'BASE', 'fallback_source': 'base1_answer', 'adoption': types.SimpleNamespace(final_answer='CANDIDATE', final_source='executor_override_accepted')})
        for key in ('revas_supported', 'final_answer', 'final_source'):
            env[key] = eval(compile(ast.Expression(assignments[key][0].value), str(CURRENT), 'eval'), env)
        preserved = env['final_answer'] == 'BASE'
        assert preserved == (not all(values))
        assert env['final_source'] == ('executor_override_accepted' if all(values) else 'base1_answer')
        rows.append({'conditions': dict(zip(flags, values)), 'supported': env['revas_supported'], 'final_answer': env['final_answer'], 'final_source': env['final_source']})
    return_nodes = [n for n in ast.walk(outer) if isinstance(n, ast.Return)]
    assert len(return_nodes) == 1 and isinstance(return_nodes[0].value, ast.Call)
    keywords = {k.arg: ast.unparse(k.value) for k in return_nodes[0].value.keywords}
    assert keywords['final_answer'] == 'final_answer' and keywords['final_source'] == 'final_source'
    runner_tree = ast.parse(RUNNER.read_text())
    main_node = next(n for n in runner_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    finals = [n for n in ast.walk(main_node) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'final_answer' for t in n.targets)]
    assert len(finals) == 1 and ast.unparse(finals[0].value) == 'revas.final_answer'
    gold_calls = [n for n in ast.walk(main_node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'gold']
    assert gold_calls and all(finals[0].lineno < n.lineno for n in gold_calls)
    row_dicts = [n for n in ast.walk(main_node) if isinstance(n, ast.Dict) and any(isinstance(k, ast.Constant) and k.value == 'revas_final_answer_locked_before_scoring' for k in n.keys if k is not None)]
    assert len(row_dicts) == 1
    answer_expr = next(v for k,v in zip(row_dicts[0].keys, row_dicts[0].values) if isinstance(k, ast.Constant) and k.value == 'revas_final_answer_locked_before_scoring')
    assert ast.unparse(answer_expr) == 'final_answer'
    dump('bounded_control_flow.json', {
        'created_at': now, 'classification': 'POST_REQUEST_STATIC_SOURCE_AND_FINITE_BOOLEAN_ANALYSIS',
        'outer_gate_fields': flags, 'truth_table_cases': len(rows), 'failed_conjunctions_preserving_baseline': sum(not r['supported'] for r in rows),
        'outer_return_count': len(return_nodes), 'final_answer_assignment_count': len(assignments['final_answer']),
        'return_fields': {k: keywords[k] for k in ('final_answer','final_source')},
        'runner_final_assignment_line': finals[0].lineno,
        'runner_first_gold_access_line': min(n.lineno for n in gold_calls),
        'runner_record_answer_expression': ast.unparse(answer_expr), 'truth_table': rows,
        'scope': 'Bounded returned per-row value and its shown historical recorder; not all deployments, arbitrary code mutation, storage authorization, or all external writers.'
    })

    history = ROOT / 'evidence/negative_case/bbeh_history'
    raw = [json.loads(line) for line in (history/'bbeh500_full_gold_blind_run_outputs.jsonl').read_text().splitlines() if line.strip()]
    patch = json.loads((history/'bbeh500_after_word_sorting_floor_patch_offline_replay.json').read_text())
    corpus_results = []
    for label, source_rows, prefix in [('original', raw, ''), ('patched_offline', patch['rows'], 'patched_')]:
        checked, violations = [], []
        for row in source_rows:
            accepted = row[prefix+'adoption_gate_accepts']
            final = row['patched_final_answer' if prefix else 'revas_final_answer_locked_before_scoring']
            baseline = row['base_answer_locked_before_scoring']
            if not accepted:
                checked.append(row['row_id'])
                if final != baseline:
                    violations.append(row['row_id'])
        assert not violations, (label, violations)
        corpus_results.append({'source': label, 'rows':len(source_rows), 'non_adopted_rows':len(checked), 'baseline_preservation_violations':violations, 'non_adopted_row_ids':checked})
    counts = {'base':sum(r['patched_base_correct'] for r in patch['rows']), 'patched_final':sum(r['patched_final_correct'] for r in patch['rows']), 'accepted_C':sum(r['patched_accepted_C'] for r in patch['rows']), 'accepted_B':sum(r['patched_accepted_B'] for r in patch['rows'])}
    assert counts == {'base':91, 'patched_final':268, 'accepted_C':177, 'accepted_B':0}
    dump('whole_corpus_preservation.json', {
        'created_at':now, 'classification':'POST_REQUEST_ANALYSIS_OF_PRE_EXISTING_RECORDS',
        'corpora':corpus_results, 'final_patched_counts':counts,
        'nonempty_rejected_rows_in_initial_corpus':sum(r['executor_answer_locked_before_scoring'] not in (None,'') and not r['adoption_gate_accepts'] for r in raw),
        'new_runtime_execution':False, 'scope':'Stored output relationships only; unchanged-component reproduction is separate. Failed admission preservation is not equivalent to every accepted answer being correct.'
    })
    print(json.dumps({'status':'PASS', 'equivalent_declarations':len(selected), 'component_cases':len(records), 'component_positive_cases':sum(r['adoption']['override_accepted'] for r in records), 'component_nonpromotion_cases':sum(not r['adoption']['override_accepted'] for r in records), 'outer_boolean_cases':len(rows), 'corpora':[{k:v for k,v in c.items() if k != 'non_adopted_row_ids'} for c in corpus_results], 'final_patched_counts':counts, 'provider_calls':0, 'mechanism_modified':False}, indent=2))


if __name__ == '__main__':
    main()
