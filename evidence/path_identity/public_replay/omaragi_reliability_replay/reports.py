"""JSON, Markdown, and HTML report export for OmarAGI Reliability BYOK Replay."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _metric(label: str, value: Any, tone: str = "") -> str:
    return (
        f'<article class="metric {tone}"><span>{_esc(label)}</span>'
        f'<strong>{_esc(value)}</strong></article>'
    )


def _humanize(value: Any) -> str:
    return str(value).replace("_", " ").strip().title()


def _verifier_display(verifier: dict[str, Any]) -> tuple[str, str]:
    if verifier["status"] == "not_run":
        return "Not run", "neutral"
    if verifier["passed"]:
        return "Passed", "good"
    return "Rejected", "warning"


def _scorer_display(scorer: dict[str, Any]) -> tuple[str, str]:
    passed = bool(scorer["final"]["passed"])
    return ("Final passed", "good") if passed else ("Final failed", "warning")


def _event_display(event: dict[str, Any]) -> tuple[str, str, str, str]:
    stage = str(event["stage"])
    stage_labels = {
        "route": "Router",
        "execute": "Executor",
        "runtime_verify": "Runtime Verifier",
        "adoption_gate": "Adoption Gate",
        "decision_lock": "Decision Lock",
        "post_lock_score": "Post-lock Scorer",
        "artifact_score": "Artifact Score",
        "log": "Scored Artifact Log",
    }
    title = stage_labels.get(stage, _humanize(stage))

    if stage == "route":
        status = "Allowed" if event.get("allowed") else "Denied"
        tone = "good" if event.get("allowed") else "protected"
        detail = str(event.get("reason") or "Router result recorded")
    elif stage == "execute":
        executed = event.get("status") == "executed"
        status = "Executed" if executed else "Skipped"
        tone = "neutral" if executed else "protected"
        detail = (
            f"{event.get('reason') or 'Executor result recorded'} · "
            f"{_humanize(event.get('mode') or 'unknown mode')} · no live generation"
        )
    elif stage == "runtime_verify":
        status, tone = _verifier_display(event)
        method = _humanize(event.get("method") or "unspecified")
        detail = (
            f"{method} · {event.get('reason') or 'No verifier rationale recorded'} · "
            "post-lock target unavailable"
        )
    elif stage == "adoption_gate":
        adopted = event.get("decision") == "candidate_adopted"
        status = "Adopted" if adopted else "Baseline preserved"
        tone = "good" if adopted else "protected"
        source = _humanize(event.get("source") or "unknown source")
        detail = f"{event.get('reason') or 'Gate result recorded'} · Final source: {source}"
    elif stage == "decision_lock":
        status = "Locked"
        tone = "good"
        detail = (
            f"{event.get('reason') or 'Decision locked'} · "
            f"SHA-256 {str(event.get('decision_sha256') or '')[:12]}…"
        )
    elif stage == "post_lock_score":
        status, tone = _scorer_display(event)
        detail = (
            f"{event.get('reason') or 'Post-lock score recorded'} · "
            f"lock verified={str(bool(event.get('lock_verified'))).lower()}"
        )
    elif stage == "artifact_score":
        score = int(event.get("score", 0))
        status = f"{score}/100"
        tone = "good" if score >= 90 else "warning" if score < 70 else "neutral"
        detail = (
            f"{event.get('reason') or 'Artifact score recorded'} · "
            "public demonstration score, not a benchmark metric"
        )
    else:
        status = "Recorded"
        tone = "neutral"
        detail = f"Ordered decision path captured for {event.get('case_id') or 'this case'}"
    return title, status, tone, detail


def _case_card(case: dict[str, Any], *, expanded: bool = False) -> str:
    outcome = case["outcome"]
    router = case["router_result"]
    executor = case["executor_result"]
    verifier = case["runtime_verifier_result"]
    adoption = case["adoption_gate_result"]
    decision_lock = case["decision_lock"]
    scorer = case["post_lock_scorer_result"]
    artifact_score = case["artifact_score"]

    preserved_badge = (
        '<span class="badge preserved">baseline preserved</span>'
        if case["preserved_baseline"]
        else ""
    )
    verifier_label, verifier_tone = _verifier_display(verifier)
    router_label = "Allowed" if router["allowed"] else "Denied"
    router_tone = "good" if router["allowed"] else "protected"
    executor_label = "Executed" if executor["status"] == "executed" else "Skipped by route"
    executor_tone = "neutral" if executor["status"] == "executed" else "protected"
    adoption_label = (
        "Candidate adopted"
        if adoption["decision"] == "candidate_adopted"
        else "Baseline preserved"
    )
    adoption_tone = "good" if adoption["decision"] == "candidate_adopted" else "protected"
    scorer_label, scorer_tone = _scorer_display(scorer)
    score_tone = "good" if artifact_score["score"] >= 90 else "warning" if artifact_score["score"] < 70 else "neutral"
    executor_output = executor["output"] if executor["status"] == "executed" else "Not executed — router denied this path."

    event_rows = []
    for event in case["event_log"]:
        title, status, tone, detail = _event_display(event)
        event_rows.append(
            '<li class="event-row">'
            f'<span class="event-step">{_esc(event["step"])}</span>'
            '<div class="event-copy">'
            '<div class="event-title">'
            f'<b>{_esc(title)}</b><span class="event-status {tone}">{_esc(status)}</span>'
            '</div>'
            f'<p>{_esc(detail)}</p>'
            '</div></li>'
        )

    open_attribute = " open" if expanded else ""
    return f"""
    <article class="case-card" id="{_esc(case['case_id'])}">
      <div class="case-head">
        <div><span class="eyebrow">{_esc(case['case_id'])}</span><h2>{_esc(case['prompt'])}</h2></div>
        <div class="badges"><span class="badge {outcome}">{_esc(outcome.replace('_', ' '))}</span>{preserved_badge}</div>
      </div>
      <div class="answer-grid">
        <section><h3>Baseline output</h3><pre>{_esc(case['baseline_output'])}</pre></section>
        <section><h3>Executor output</h3><pre>{_esc(executor_output)}</pre></section>
        <section class="final"><h3>Final answer</h3><pre>{_esc(case['final_answer'])}</pre></section>
      </div>
      <div class="decision-grid">
        <section><span>Router</span><b class="decision-value {router_tone}">{_esc(router_label)}</b><small>{_esc(router['reason'])}</small></section>
        <section><span>Executor</span><b class="decision-value {executor_tone}">{_esc(executor_label)}</b><small>{_esc(executor['executor'])} · {_esc(executor['mode'])} · generated_live=false</small></section>
        <section><span>Runtime Verifier · {_esc(_humanize(verifier['method']))}</span><b class="decision-value {verifier_tone}">{_esc(verifier_label)}</b><small>{_esc(verifier['reason'])} · target_accessed=false</small></section>
        <section><span>Adoption Gate</span><b class="decision-value {adoption_tone}">{_esc(adoption_label)}</b><small>{_esc(adoption['reason'])}</small></section>
        <section><span>Decision Lock</span><b class="decision-value good">Locked</b><small>SHA-256 {_esc(decision_lock['decision_sha256'][:12])}… · before scoring</small></section>
        <section><span>Post-lock Scorer</span><b class="decision-value {scorer_tone}">{_esc(scorer_label)}</b><small>{_esc(scorer['reason'])}</small></section>
        <section><span>Artifact Score</span><b class="decision-value {score_tone}">{_esc(artifact_score['score'])}/100</b><small>{_esc(artifact_score['reason'])} · public demonstration score, not a benchmark metric</small></section>
      </div>
      <details{open_attribute}><summary><span>Ordered decision trace</span><small>{len(case['event_log'])} recorded stages</small></summary><ol class="event-log">{''.join(event_rows)}</ol></details>
    </article>
    """


def render_summary(report: dict[str, Any]) -> str:
    """Render a compact, human-readable replay summary."""

    summary = report["summary"]
    sign = "+" if summary["delta_percentage_points"] > 0 else ""
    rows = "\n".join(
        "| {case_id} | {router} | {executor} | {verifier} | {adoption} | {lock} | {scorer} | {score}/100 | {outcome} |".format(
            case_id=str(case["case_id"]).replace("|", "\\|"),
            router=case["router_result"]["decision"],
            executor=case["executor_result"]["status"],
            verifier=_verifier_display(case["runtime_verifier_result"])[0],
            adoption=case["adoption_gate_result"]["decision"],
            lock=case["decision_lock"]["status"],
            scorer=_scorer_display(case["post_lock_scorer_result"])[0],
            score=case["artifact_score"]["score"],
            outcome=case["outcome"],
        )
        for case in report["cases"]
    )
    artifact_summary = summary["artifact_score"]
    return f"""# {report['title']}

> {report['policy_label']}

## Visible pipeline

Baseline → Router → Executor → Runtime Verifier → Adoption Gate → Decision Lock → Post-lock Scorer → Scored Artifact

The runtime path cannot read the post-lock scoring target. Route and adoption are
hashed and locked before the scorer is invoked.

## Runtime boundary

- **Live product:** {report['runtime_boundary']['live_product']}
- **Public repository:** {report['runtime_boundary']['public_repository']}
- **Evidence status:** {report['runtime_boundary']['evidence_status']}

## Replay summary

- Cases: {summary['case_count']}
- Baseline correct: {summary['baseline_correct']} ({summary['baseline_score_percent']}%)
- Governed final correct: {summary['governed_correct']} ({summary['governed_score_percent']}%)
- Sample delta: {sign}{summary['delta_percentage_points']} percentage points
- Candidate adoptions: {summary['adoption_count']}
- Preserved baselines: {summary['preserved_baseline_count']}
- Beneficial flips: {summary['beneficial_flip_count']}
- Harmful flips: {summary['harmful_flip_count']}
- Floor preserved: {summary['floor_preserved_count']}/{summary['case_count']}

## Public demonstration artifact score

- Mean: {artifact_summary['mean']}/100
- Range: {artifact_summary['minimum']}–{artifact_summary['maximum']}
- Label: `{artifact_summary['label']}`

This transparent score explains the committed demonstration outcomes. It is not a benchmark metric.

## Case decisions

| Case | Router | Executor | Runtime Verifier | Adoption Gate | Decision Lock | Post-lock Scorer | Artifact Score | Outcome |
|---|---|---|---|---|---|---|---:|---|
{rows}

## Claim boundary

{report['claim_boundary']}
"""


def render_html(report: dict[str, Any]) -> str:
    summary = report["summary"]
    cards = "".join(
        _case_card(case, expanded=index == 0)
        for index, case in enumerate(report["cases"])
    )
    direction = summary["direction"]
    sign = "+" if summary["delta_percentage_points"] > 0 else ""
    embedded = json.dumps(report, ensure_ascii=False).replace("</", "<\\/")
    metrics = "".join(
        [
            _metric("Baseline", f"{summary['baseline_score_percent']}%"),
            _metric("Final", f"{summary['governed_score_percent']}%", "accent"),
            _metric(
                "Sample delta",
                f"{sign}{summary['delta_percentage_points']} pp {direction}",
                "accent",
            ),
            _metric("Adopted", summary["adoption_count"]),
            _metric("Baseline preserved", summary["preserved_baseline_count"]),
            _metric("Beneficial flips", summary["beneficial_flip_count"], "good"),
            _metric("Harmful flips", summary["harmful_flip_count"], "danger"),
            _metric(
                "Floor preserved",
                f"{summary['floor_preserved_count']}/{summary['case_count']}",
                "good",
            ),
        ]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='24' fill='%23fff'/%3E%3Ccircle cx='32' cy='32' r='11' fill='%23ff365f'/%3E%3C/svg%3E">
  <title>{_esc(report['title'])}</title>
  <style>
    :root {{ color-scheme: dark; --bg:#070707; --panel:#111; --line:#2b2b2b; --text:#f4f4f0; --muted:#9f9f9a; --red:#ff365f; --green:#54e39e; --amber:#ffc66d; --blue:#8bc8ff; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:radial-gradient(circle at 85% 5%,#291018 0,transparent 28rem),var(--bg); color:var(--text); font:15px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    a {{ color:inherit; }}
    .shell {{ width:min(1280px,calc(100% - 32px)); margin:auto; padding:48px 0 80px; }}
    header {{ display:grid; grid-template-columns:1fr auto; gap:32px; align-items:end; padding-bottom:28px; border-bottom:1px solid var(--line); }}
    .mark {{ display:inline-flex; align-items:center; gap:9px; font-weight:800; letter-spacing:-.03em; }}
    .mark i {{ width:17px; height:17px; display:block; border:5px solid #fff; border-radius:50%; box-shadow:inset 0 0 0 2px var(--red); }}
    h1 {{ margin:16px 0 8px; font-size:clamp(36px,7vw,76px); letter-spacing:-.065em; line-height:.94; max-width:900px; }}
    .lede {{ max-width:820px; color:var(--muted); font-size:18px; }}
    .runtime-note {{ max-width:900px; margin:18px 0 0; display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1px; overflow:hidden; border:1px solid var(--line); border-radius:12px; background:var(--line); color:#c7c7c1; font-size:13px; }}
    .runtime-note span {{ display:block; padding:12px 14px; background:#101010; }}
    .runtime-note strong {{ display:block; margin-bottom:2px; color:var(--text); }}
    .actions {{ display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end; }}
    .download {{ border:1px solid var(--line); padding:11px 16px; border-radius:999px; text-decoration:none; white-space:nowrap; }}
    .boundary {{ margin:28px 0; padding:16px 18px; border-left:3px solid var(--red); background:#151012; color:#f5cbd4; }}
    .flow {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin:24px 0 32px; }}
    .flow span {{ border:1px solid var(--line); border-radius:999px; padding:8px 12px; color:var(--muted); }}
    .flow span:not(:last-child)::after {{ content:"  →"; color:var(--red); margin-left:10px; }}
    .metrics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:10px; margin-bottom:40px; }}
    .metric {{ min-height:112px; padding:16px; background:var(--panel); border:1px solid var(--line); border-radius:16px; display:flex; flex-direction:column; justify-content:space-between; }}
    .metric span {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.08em; }}
    .metric strong {{ font-size:22px; letter-spacing:-.04em; }}
    .metric.accent strong {{ color:var(--red); }} .metric.good strong {{ color:var(--green); }} .metric.danger strong {{ color:#ff8ca4; }}
    .cases {{ display:grid; gap:18px; }}
    .case-card {{ background:rgba(17,17,17,.94); border:1px solid var(--line); border-radius:22px; padding:24px; }}
    .case-head {{ display:flex; justify-content:space-between; gap:22px; align-items:start; }}
    .eyebrow {{ color:var(--red); font:700 11px/1.2 ui-monospace,SFMono-Regular,Menlo,monospace; text-transform:uppercase; letter-spacing:.11em; }}
    h2 {{ margin:5px 0 20px; font-size:21px; letter-spacing:-.025em; }} h3 {{ margin:0 0 9px; font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }}
    .badges {{ display:flex; gap:7px; flex-wrap:wrap; justify-content:flex-end; }}
    .badge {{ border:1px solid var(--line); border-radius:999px; padding:7px 11px; white-space:nowrap; font-size:12px; }}
    .badge.beneficial_flip {{ color:var(--green); }} .badge.harmful_flip {{ color:#ff8ca4; }} .badge.preserved {{ color:#e7b8c3; }}
    .answer-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }}
    .decision-grid {{ display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); gap:10px; }}
    .answer-grid section,.decision-grid section {{ border:1px solid var(--line); border-radius:14px; padding:14px; min-width:0; }}
    .answer-grid .final {{ border-color:#713146; background:#180d11; }}
    pre {{ margin:0; white-space:pre-wrap; overflow-wrap:anywhere; font:600 14px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace; }}
    .decision-grid {{ margin-top:10px; }} .decision-grid span,.decision-grid small {{ display:block; color:var(--muted); }} .decision-grid span {{ font-size:11px; text-transform:uppercase; letter-spacing:.08em; }} .decision-grid b {{ display:block; margin:5px 0; }}
    .decision-value.good {{ color:var(--green); }} .decision-value.warning {{ color:var(--amber); }} .decision-value.protected {{ color:#f0b3c1; }} .decision-value.neutral {{ color:var(--blue); }}
    details {{ margin-top:14px; border:1px solid var(--line); border-radius:14px; background:#0c0c0c; color:var(--muted); overflow:hidden; }}
    summary {{ cursor:pointer; display:flex; align-items:center; justify-content:space-between; gap:16px; padding:14px 16px; list-style:none; color:var(--text); font-weight:700; }}
    summary::-webkit-details-marker {{ display:none; }} summary::after {{ content:"↓"; color:var(--red); transition:transform .18s ease; }} details[open] summary {{ border-bottom:1px solid var(--line); }} details[open] summary::after {{ transform:rotate(180deg); }} summary small {{ margin-left:auto; color:var(--muted); font-size:12px; font-weight:500; }}
    .event-log {{ position:relative; list-style:none; display:grid; gap:0; margin:0; padding:14px 16px 16px; }}
    .event-log::before {{ content:""; position:absolute; left:31px; top:30px; bottom:31px; width:1px; background:var(--line); }}
    .event-row {{ position:relative; display:grid; grid-template-columns:32px minmax(0,1fr); gap:12px; padding:7px 0; }}
    .event-step {{ position:relative; z-index:1; width:28px; height:28px; display:grid; place-items:center; border:1px solid #444; border-radius:50%; background:#151515; color:var(--text); font:700 11px/1 ui-monospace,SFMono-Regular,Menlo,monospace; }}
    .event-copy {{ min-width:0; padding-top:2px; }} .event-title {{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; }} .event-title b {{ color:var(--text); }} .event-copy p {{ margin:3px 0 0; color:var(--muted); font-size:13px; overflow-wrap:anywhere; }}
    .event-status {{ border:1px solid var(--line); border-radius:999px; padding:2px 8px; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:.07em; }} .event-status.good {{ color:var(--green); border-color:#245d43; }} .event-status.warning {{ color:var(--amber); border-color:#6a5526; }} .event-status.protected {{ color:#f0b3c1; border-color:#653544; }} .event-status.neutral {{ color:var(--blue); border-color:#2e526f; }}
    footer {{ color:var(--muted); margin-top:32px; font-size:13px; }}
    @media (max-width:1050px) {{ .decision-grid {{ grid-template-columns:repeat(2,1fr); }} }}
    @media (max-width:900px) {{ .metrics {{ grid-template-columns:repeat(2,1fr); }} .answer-grid {{ grid-template-columns:1fr; }} header {{ grid-template-columns:1fr; }} .case-head {{ flex-direction:column; gap:4px; }} .badges {{ justify-content:flex-start; }} }}
    @media (max-width:620px) {{ .decision-grid,.runtime-note {{ grid-template-columns:1fr; }} }}
    @media (max-width:520px) {{ .shell {{ width:min(100% - 20px,1280px); padding-top:28px; }} .case-card {{ padding:16px; border-radius:18px; }} .metrics {{ gap:8px; }} .metric {{ min-height:96px; }} summary {{ align-items:flex-start; }} summary small {{ text-align:right; }} }}
  </style>
</head>
<body>
  <main class="shell">
    <header>
      <div><div class="mark"><i></i>OmarAGI</div><h1>Reliability BYOK Replay</h1><p class="lede">The sanitized offline demonstration of the public decision path around live OmarAGI BYOK model runs: route a candidate, execute the replay, verify without the scoring target, lock adoption, then score and emit an artifact.</p><div class="runtime-note"><span><strong>Live BYOK product · omaragi.com</strong>Real model execution with a user-supplied API key.</span><span><strong>Public demo mode</strong>Sanitized deterministic replay; no credentials, external calls, or benchmark claim.</span></div></div>
      <div class="actions"><a class="download" href="https://omaragi.com/run" target="_blank" rel="noopener">Open live BYOK</a><a class="download" href="https://omaragi.com/results/run_1779840603_8c2cfeec9d" target="_blank" rel="noopener">Inspect live diagnostic</a><a class="download" href="replay_summary.md" download>Download summary</a><a class="download" href="report.json" download>Download JSON</a></div>
    </header>
    <p class="boundary">{_esc(report['policy_label'])}</p>
    <div class="flow"><span>Baseline</span><span>Router</span><span>Executor</span><span>Runtime Verifier</span><span>Adoption Gate</span><span>Decision Lock</span><span>Post-lock Scorer</span><span>Scored Artifact</span></div>
    <section class="metrics">{metrics}</section>
    <section class="cases">{cards}</section>
    <footer>{_esc(report['claim_boundary'])}</footer>
  </main>
  <script type="application/json" id="replay-report">{embedded}</script>
</body>
</html>
"""


def export_reports(report: dict[str, Any], output_dir: str | Path) -> dict[str, Path]:
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    json_path = destination / "report.json"
    html_path = destination / "report.html"
    summary_path = destination / "replay_summary.md"
    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    html_path.write_text(render_html(report), encoding="utf-8")
    summary_path.write_text(render_summary(report), encoding="utf-8")
    return {"summary": summary_path, "json": json_path, "html": html_path}
