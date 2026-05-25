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
    cards = []
    for item in index_payload["items"]:
        artifacts = item.get("site_artifacts", {})
        links = []
        for label, key in [("Visualizar", "html"), ("PDF", "pdf"), ("DOCX", "docx"), ("EWM JSON", "ewm_json"), ("Markdown", "markdown")]:
            href = artifacts.get(key)
            if href:
                links.append(f'<a class="artifact-link" href="{escape(href)}">{label}</a>')

        repository = str(item.get("repository", "")).strip()
        prototype = str(item.get("prototype", "")).strip()
        repository_href = f"https://github.com/osvaldojeronymo/{repository}" if repository else ""
        quick_links = []
        if repository_href:
            quick_links.append(f'<a href="{escape(repository_href)}">Repositório</a>')
        if prototype:
            quick_links.append(f'<a href="{escape(prototype)}">Protótipo</a>')

        cards.append(
            "<article class=\"story-card\">"
            f"<div class=\"story-head\"><p class=\"story-id\">{escape(str(item.get('id', '')))}</p><span class=\"story-kind\">{escape(str(item.get('kind', '')).replace('-', ' '))}</span></div>"
            f"<h2>{escape(str(item.get('title', '')))}</h2>"
            f"<p class=\"story-module\">{escape(str(item.get('module', '')))}</p>"
            f"<p class=\"story-summary\">Status: <strong>{escape(str(item.get('status', '')))}</strong> · Responsável: <strong>{escape(str(item.get('owner', '')))}</strong> · Versão: <strong>{escape(str(item.get('version', '')))}</strong></p>"
            f"<div class=\"artifact-grid\">{''.join(links)}</div>"
            f"<div class=\"story-links\">{' · '.join(quick_links)}</div>"
            "</article>"
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
    :root {{ color-scheme: light; --bg: #f4efe5; --panel: #fffdf8; --ink: #14202b; --accent: #005ca9; --accent-2: #f39200; --muted: #5b6777; --line: #d9d1c3; --soft: #edf4fb; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Georgia, 'Source Serif 4', serif; background: radial-gradient(circle at top left, #fff6df 0%, #f4efe5 38%, #efe7d8 100%); color: var(--ink); }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 32px 24px 72px; }}
    h1 {{ margin: 0 0 12px; font-size: clamp(2.2rem, 4vw, 3.4rem); line-height: 1.05; }}
    h2 {{ margin: 0 0 10px; font-size: 1.35rem; }}
    p, li {{ line-height: 1.6; }}
    a {{ color: var(--accent); text-decoration: none; font-weight: 600; }}
    a:hover {{ text-decoration: underline; }}
    .hero {{ position: relative; overflow: hidden; background: linear-gradient(135deg, rgba(0, 92, 169, 0.96), rgba(7, 48, 86, 0.96)); color: #fff; border-radius: 24px; padding: 34px; box-shadow: 0 20px 60px rgba(20, 32, 43, 0.18); }}
    .hero::after {{ content: ''; position: absolute; inset: auto -120px -160px auto; width: 320px; height: 320px; background: radial-gradient(circle, rgba(243, 146, 0, 0.95) 0%, rgba(243, 146, 0, 0) 68%); }}
    .eyebrow {{ margin: 0 0 10px; font-size: 0.88rem; letter-spacing: 0.16em; text-transform: uppercase; opacity: 0.82; }}
    .hero-copy {{ max-width: 760px; position: relative; z-index: 1; }}
    .hero-actions {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }}
    .hero-actions a {{ display: inline-flex; align-items: center; justify-content: center; padding: 11px 16px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.24); background: rgba(255,255,255,0.1); color: #fff; text-decoration: none; }}
    .hero-actions a.primary {{ background: var(--accent-2); border-color: var(--accent-2); color: #14202b; }}
    .meta {{ color: rgba(255,255,255,0.84); margin-bottom: 12px; }}
    .stats {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 22px 0 0; padding: 0; list-style: none; position: relative; z-index: 1; }}
    .stats li {{ background: rgba(255,255,255,0.12); color: #fff; border: 1px solid rgba(255,255,255,0.16); border-radius: 999px; padding: 8px 14px; font-size: 0.95rem; }}
    .section-head {{ display: flex; justify-content: space-between; gap: 16px; align-items: end; margin-top: 28px; }}
    .section-head p {{ margin: 0; color: var(--muted); max-width: 780px; }}
    .stories-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin-top: 22px; }}
    .story-card {{ background: rgba(255,253,248,0.92); border: 1px solid var(--line); border-radius: 20px; padding: 22px; box-shadow: 0 18px 45px rgba(31, 42, 55, 0.08); backdrop-filter: blur(8px); }}
    .story-head {{ display: flex; justify-content: space-between; gap: 10px; align-items: center; margin-bottom: 12px; }}
    .story-id {{ margin: 0; color: var(--accent); font-weight: 700; letter-spacing: 0.04em; }}
    .story-kind {{ display: inline-flex; padding: 6px 10px; border-radius: 999px; background: var(--soft); color: var(--accent); font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.04em; }}
    .story-module {{ margin: 0 0 12px; color: var(--muted); font-style: italic; }}
    .story-summary {{ margin: 0 0 16px; color: var(--ink); }}
    .artifact-grid {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }}
    .artifact-link {{ display: inline-flex; align-items: center; justify-content: center; padding: 10px 12px; border-radius: 12px; background: #fff; border: 1px solid #cfd9e6; color: var(--accent); text-decoration: none; min-width: 108px; }}
    .artifact-link:hover {{ background: var(--soft); text-decoration: none; }}
    .story-links {{ margin-top: 16px; color: var(--muted); }}
    .story-links a {{ font-weight: 600; }}
    .note-panel {{ margin-top: 28px; background: #fff8ea; border: 1px solid #f3d29a; border-radius: 18px; padding: 18px 20px; }}
    .note-panel strong {{ color: #7c4b00; }}
    footer {{ margin-top: 28px; color: var(--muted); font-size: 0.95rem; }}
    code {{ background: rgba(20, 32, 43, 0.06); padding: 0.15rem 0.4rem; border-radius: 6px; }}
    @media (max-width: 760px) {{ main {{ padding: 18px 14px 40px; }} .hero {{ padding: 24px; }} .hero-actions {{ flex-direction: column; align-items: stretch; }} .section-head {{ display: block; }} }}
  </style>
</head>
<body>
  <main>
    <section class=\"hero\">
      <div class=\"hero-copy\">
      <p class=\"eyebrow\">CAIXA · SILIC 2.0 · Governança Documental</p>
      <p class=\"meta\">Publicacao automatica via GitHub Pages a partir do repositório canonico de documentação</p>
      <h1>Historias de Usuario do SILIC 2.0</h1>
      <p>Catálogo institucional publicado a partir do front matter canônico das histórias mantidas em <code>docs/user-stories</code>, com acesso direto aos artefatos de leitura, exportação e integração.</p>
      <div class=\"hero-actions\">
        <a class=\"primary\" href=\"#catalogo\">Abrir catálogo</a>
        <a href=\"index.json\">Baixar índice JSON</a>
        <a href=\"https://github.com/osvaldojeronymo/osvaldojeronymo-silic-2.0/tree/copilot-structure/docs/user-stories\">Abrir fontes no GitHub</a>
      </div>
      <ul class=\"stats\">
        <li>Total: {total}</li>
        <li>Historias: {user_stories}</li>
        <li>Templates: {templates}</li>
        <li>Gerado em: {generated_at}</li>
      </ul>
      </div>
    </section>
    <section id=\"catalogo\" class=\"section-head\">
      <div>
        <h2>Catálogo publicado</h2>
        <p>Cada card abaixo centraliza a navegação da história para leitura online, exportação em PDF e DOCX, fonte Markdown e payload EWM JSON.</p>
      </div>
    </section>
    <section class=\"stories-grid\">
      {''.join(cards)}
    </section>
    <section class=\"note-panel\">
      <strong>Observação operacional:</strong> o catálogo público publica artefatos estáticos e payloads estruturados, mas a sincronização direta com IBM Jazz / EWM continua dependente do ambiente corporativo interno da CAIXA.
    </section>
    <footer>
      Publicação mantida por GitHub Actions e GitHub Pages a partir do branch publicado do repositório.
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