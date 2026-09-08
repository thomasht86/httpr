# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "pandas",
#     "tabulate",
# ]
# ///
"""Render the HTTP-client comparison into a chart and an HTML page.

Reads the CSVs written by ``benchmark.py`` (``session=False.csv``,
``session=True.csv``, ``session='Async'.csv``, ``threads.csv``) from
``--results`` and writes to ``--out``:

- ``comparison.png``: one bar chart per scenario, wall-clock seconds for
  400 requests, lower is better. This is the image embedded in the README
  and the docs.
- ``index.html``: the chart plus the full tables (wall and CPU time).
- ``comparison.md``: the same tables as Markdown.

Run with: uv run --script benchmark/render_comparison.py --results <dir> --out <dir>
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

SIZES = ["5k", "50k", "200k"]
HTTPR_COLOR = "#e4572e"
OTHER_COLOR = "#8da0cb"

# (title, csv file, filter column, filter value)
SCENARIOS = [
    ("Sync, one client reused", "session=True.csv", "session", "True"),
    ("Sync, new client per request", "session=False.csv", "session", "False"),
    ("Async, one client reused", "session='Async'.csv", "session", "Async"),
    ("32 threads, one client reused", "threads.csv", "threads", "32"),
]


def load(results: pathlib.Path, csv: str, col: str, value: str) -> pd.DataFrame | None:
    path = results / csv
    if not path.exists():
        return None
    df = pd.read_csv(path)
    df = df[df[col].astype(str) == value].copy()
    return df if not df.empty else None


def short_name(name: str) -> str:
    """'httpx2 2.12.0' -> 'httpx2\\n2.12.0' for axis labels."""
    parts = name.split(" ", 1)
    return "\n".join(parts) if len(parts) == 2 else name


def plot(results: pathlib.Path, out: pathlib.Path, generated: str) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    for ax, (title, csv, col, value) in zip(axes.flat, SCENARIOS, strict=True):
        df = load(results, csv, col, value)
        ax.set_title(title, fontsize=12, loc="left")
        if df is None:
            ax.text(0.5, 0.5, "no data", ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off()
            continue
        # Order by total wall time so the fastest client is on the left.
        cols = [f"time {s}" for s in SIZES if f"time {s}" in df.columns]
        df["total"] = df[cols].sum(axis=1)
        df = df.sort_values("total")
        names = list(df["name"])
        x = range(len(names))
        width = 0.8 / len(cols)
        for i, c in enumerate(cols):
            offsets = [xi + (i - (len(cols) - 1) / 2) * width for xi in x]
            colors = [HTTPR_COLOR if n.startswith("httpr") else OTHER_COLOR for n in names]
            alpha = 0.45 + 0.55 * (i / max(len(cols) - 1, 1))
            bars = ax.bar(offsets, df[c], width, color=colors, alpha=alpha, label=c.replace("time ", ""))
            ax.bar_label(bars, fmt="%.2f", fontsize=7, padding=1)
        ax.set_xticks(list(x))
        ax.set_xticklabels([short_name(n) for n in names], fontsize=8)
        ax.set_ylabel("seconds for 400 requests (lower is better)", fontsize=9)
        ax.legend(title="response size", fontsize=8, title_fontsize=8, frameon=False)
        ax.spines[["top", "right"]].set_visible(False)
        ax.margins(y=0.15)
    fig.suptitle("HTTP client comparison", fontsize=15, x=0.01, ha="left", fontweight="bold")
    fig.text(
        0.01,
        0.945,
        f"httpr vs. the latest release of each library, generated {generated}. "
        "Local uvicorn server, gzip responses; wall-clock time, so absolute numbers depend on the runner.",
        fontsize=9,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out / "comparison.png", dpi=110)
    plt.close(fig)


def tables(results: pathlib.Path) -> list[tuple[str, pd.DataFrame]]:
    out = []
    for title, csv, col, value in SCENARIOS:
        df = load(results, csv, col, value)
        if df is None:
            continue
        wall = [c for c in df.columns if c.startswith("time ")]
        cpu = [c for c in df.columns if c.startswith("cpu_time ")]
        keep = ["name", *wall, *cpu]
        df = df[keep].sort_values(keep[1]).round(2)
        df.columns = [c.replace("cpu_time ", "cpu ").replace("time ", "wall ") for c in keep]
        df = df.dropna(axis=1, how="all")  # sync runs have no JSON columns
        out.append((title, df))
    return out


def write_pages(results: pathlib.Path, out: pathlib.Path, generated: str, run_url: str | None) -> None:
    tbls = tables(results)
    md = ["# HTTP client comparison", "", f"Generated {generated}. Seconds for 400 requests; lower is better.", ""]
    body = []
    for title, df in tbls:
        md += [f"## {title}", "", df.to_markdown(index=False), ""]
        body.append(f"<h2>{html.escape(title)}</h2>\n{df.to_html(index=False, border=0)}")
    (out / "comparison.md").write_text("\n".join(md))
    source = f'<a href="{html.escape(run_url)}">workflow run</a>' if run_url else "the compare workflow"
    page = f"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>httpr — HTTP client comparison</title>
<style>
  body {{ font: 15px/1.5 -apple-system, system-ui, sans-serif; max-width: 1100px;
         margin: 2rem auto; padding: 0 1rem; color: #222; }}
  img {{ max-width: 100%; }}
  table {{ border-collapse: collapse; margin: 0 0 2rem; font-size: 14px; }}
  th, td {{ padding: 4px 10px; text-align: right; border-bottom: 1px solid #ddd; }}
  th:first-child, td:first-child {{ text-align: left; }}
  .meta {{ color: #555; }}
</style>
<h1>HTTP client comparison</h1>
<p class="meta">Generated {html.escape(generated)} by {source} against the latest release of every library.
400 requests per cell against a local uvicorn server with gzip responses; wall-clock seconds, lower is better.
Absolute numbers depend on the GitHub runner, so compare rows, not weeks.
See also the <a href="../">httpr performance trend</a> and the
<a href="https://github.com/thomasht86/httpr/tree/main/benchmark">benchmark source</a>.</p>
<p><img src="comparison.png" alt="Bar charts comparing HTTP clients"></p>
{"".join(body)}
<p class="meta">Raw data:
<a href="session=True.csv">session=True.csv</a>,
<a href="session=False.csv">session=False.csv</a>,
<a href="session='Async'.csv">session='Async'.csv</a>,
<a href="threads.csv">threads.csv</a>,
<a href="comparison.md">comparison.md</a>.</p>
"""
    (out / "index.html").write_text(page)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("."))
    parser.add_argument("--run-url", default=None, help="Link to the CI run that produced the data")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    generated = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    plot(args.results, args.out, generated)
    write_pages(args.results, args.out, generated, args.run_url)
    for csv in ("session=False.csv", "session=True.csv", "session='Async'.csv", "threads.csv"):
        src = args.results / csv
        if src.exists() and src.resolve() != (args.out / csv).resolve():
            (args.out / csv).write_bytes(src.read_bytes())
    print(f"wrote {args.out / 'comparison.png'}, index.html, comparison.md")


if __name__ == "__main__":
    main()
