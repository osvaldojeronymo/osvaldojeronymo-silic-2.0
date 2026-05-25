from __future__ import annotations

import shutil
from html import escape
from pathlib import Path

from common import list_story_files, load_story
from export_user_story import run_pandoc, story_to_ewm_payload
from index_user_stories import build_index
from common import dump_json


ROOT = Path(__file__).resolve().parents[2]
STORIES_DIR = ROOT / "docs" / "user-stories"
GENERATED_DIR = STORIES_DIR / "generated"
SITE_DIR = GENERATED_DIR / "site"


def story_kind(story_id: str, file_name: str) -> str:
    if file_name == "HU-TEMPLATE.md" or "XXX" in story_id:
        return "template"
    return "user-story"


def build_story_site_assets(story_path: Path) -> dict[str, str]:
    story = load_story(story_path)
    story_dir = SITE_DIR / "stories" / story.story_id
    story_dir.mkdir(parents=True, exist_ok=True)

    html_name = f"{story.story_id}.html"
    pdf_name = f"{story.story_id}.pdf"
    docx_name = f"{story.story_id}.docx"
    ewm_name = f"{story.story_id}.ewm.json"
    md_name = f"{story.story_id}.md"

    run_pandoc(story_path, story_dir / html_name)
    run_pandoc(story_path, story_dir / pdf_name)
    run_pandoc(story_path, story_dir / docx_name)
    dump_json(story_dir / ewm_name, story_to_ewm_payload(story_path))
    shutil.copy2(story_path, story_dir / md_name)

    return {
        "html": f"stories/{story.story_id}/{html_name}",
        "pdf": f"stories/{story.story_id}/{pdf_name}",
        "docx": f"stories/{story.story_id}/{docx_name}",
        "ewm_json": f"stories/{story.story_id}/{ewm_name}",
        "markdown": f"stories/{story.story_id}/{md_name}",
    }


def build_index_html(index_payload: dict) -> str:
    rows = []
    for item in index_payload["items"]:
        artifacts = item.get("site_artifacts", {})
        links = []
        for label, key in [("HTML", "html"), ("PDF", "pdf"), ("DOCX", "docx"), ("EWM JSON", "ewm_json"), ("MD", "markdown")]:
            href = artifacts.get(key)
            if href:
                links.append(f'<a href="{escape(href)}">{label}</a>')
        rows.append(
            "<tr>"
            f"<td>{escape(str(item.get('id', '')))}</td>"
            f"<td>{escape(str(item.get('title', '')))}</td>"
            f"<td>{escape(str(item.get('module', '')))}</td>"
            f"<td>{escape(str(item.get('status', '')))}</td>"
            f"<td>{escape(str(item.get('kind', '')))}</td>"
            f"<td>{' | '.join(links)}</td>"
            "</tr>"
        )

    generated_at = escape(index_payload["generated_at"])
    total = index_payload["counts"]["total"]
    user_stories = index_payload["counts"]["user_stories"]
    templates = index_payload["counts"]["templates"]

    return f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>SILIC 2.0 - Historias de Usuario</title>
  <style>
    :root {{ color-scheme: light; --bg: #f5f1e8; --panel: #fffdf8; --ink: #1f2a37; --accent: #005ca9; --muted: #5b6777; --line: #d9d1c3; }}
    body {{ margin: 0; font-family: Georgia, 'Source Serif 4', serif; background: linear-gradient(180deg, #ede7da 0%, #f8f5ef 100%); color: var(--ink); }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 48px 24px 64px; }}
    h1 {{ margin: 0 0 12px; font-size: 2.4rem; }}
    p, li {{ line-height: 1.6; }}
    .hero {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 28px; box-shadow: 0 18px 50px rgba(31, 42, 55, 0.08); }}
    .meta {{ color: var(--muted); margin-bottom: 18px; }}
    .stats {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 20px 0 0; padding: 0; list-style: none; }}
    .stats li {{ background: #eef5fb; color: var(--accent); border: 1px solid #c6d9ed; border-radius: 999px; padding: 8px 14px; font-size: 0.95rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 28px; background: var(--panel); border: 1px solid var(--line); border-radius: 18px; overflow: hidden; box-shadow: 0 18px 50px rgba(31, 42, 55, 0.08); }}
    th, td {{ text-align: left; padding: 14px 16px; border-bottom: 1px solid var(--line); vertical-align: top; }}
    th {{ background: #f1eadf; font-size: 0.92rem; letter-spacing: 0.02em; text-transform: uppercase; }}
    tr:last-child td {{ border-bottom: none; }}
    a {{ color: var(--accent); text-decoration: none; font-weight: 600; }}
    a:hover {{ text-decoration: underline; }}
    footer {{ margin-top: 28px; color: var(--muted); font-size: 0.95rem; }}
    @media (max-width: 760px) {{ main {{ padding: 24px 14px 40px; }} table, thead, tbody, th, td, tr {{ display: block; }} thead {{ display: none; }} td {{ padding: 10px 14px; }} tr {{ border-bottom: 1px solid var(--line); }} }}
  </style>
</head>
<body>
  <main>
    <section class=\"hero\">
      <p class=\"meta\">Publicacao automatica via GitHub Pages</p>
      <h1>Historias de Usuario do SILIC 2.0</h1>
      <p>Catalogo publicado a partir do front matter canonico das historias mantidas em <code>docs/user-stories</code>.</p>
      <ul class=\"stats\">
        <li>Total: {total}</li>
        <li>Historias: {user_stories}</li>
        <li>Templates: {templates}</li>
        <li>Gerado em: {generated_at}</li>
      </ul>
    </section>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Titulo</th>
          <th>Modulo</th>
          <th>Status</th>
          <th>Tipo</th>
          <th>Artefatos</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
    <footer>
      O deploy depende do GitHub Pages configurado para GitHub Actions no repositorio remoto.
    </footer>
  </main>
</body>
</html>
"""


def main() -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    index_payload = build_index()
    items_with_artifacts = []
    for story_path in list_story_files(STORIES_DIR):
        story = load_story(story_path)
        kind = story_kind(story.story_id, story_path.name)
        item = next((entry for entry in index_payload["items"] if entry["id"] == story.story_id), None)
        if item is None:
            continue
        item["kind"] = kind
        item["site_artifacts"] = build_story_site_assets(story_path)
        items_with_artifacts.append(item)

    index_payload["items"] = items_with_artifacts
    dump_json(SITE_DIR / "index.json", index_payload)
    (SITE_DIR / ".nojekyll").write_text("\n", encoding="utf-8")
    (SITE_DIR / "index.html").write_text(build_index_html(index_payload), encoding="utf-8")
    print(f"Site gerado em {SITE_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()