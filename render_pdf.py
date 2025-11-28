import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


ROOT = Path(__file__).parent


def load_data():
  with open(ROOT / "data.json", "r", encoding="utf-8") as f:
    return json.load(f)


def paginate_comments(comments, max_chars=1100, max_per_page=3):
  """
  Group comments into pages.

  A page takes:
    - up to max_per_page comments
    - or until roughly max_chars of message text
  """
  pages = []
  current_page = []
  current_len = 0

  for c in comments:
    msg = c.get("message", "")
    msg_len = len(msg)
    # very short sympathy messages count less toward the limit
    effective_len = msg_len if msg_len > 120 else msg_len * 0.5

    # if adding this one would overflow limits, start a new page
    if current_page and (current_len + effective_len > max_chars or len(current_page) >= max_per_page):
      pages.append(current_page)
      current_page = []
      current_len = 0

    current_page.append(c)
    current_len += effective_len

  if current_page:
    pages.append(current_page)

  return pages


def parse_background(bg_config, default_size="cover", default_position="center"):
  """Parse background config - supports both string and object formats."""
  if isinstance(bg_config, str):
    return {
      "image": bg_config,
      "size": default_size,
      "position": default_position
    }
  elif isinstance(bg_config, dict):
    return {
      "image": bg_config.get("image", ""),
      "size": bg_config.get("size", default_size),
      "position": bg_config.get("position", default_position)
    }
  return {"image": "", "size": default_size, "position": default_position}


def render_pdf():
  data = load_data()
  comments = data["comments"]
  pages = paginate_comments(comments, max_chars=2400, max_per_page=2)

  print(f"Generated {len(pages)} pages:")
  for i, page in enumerate(pages, 1):
    authors = [c["author"] for c in page]
    print(f"  Page {i}: {len(page)} comments - {', '.join(authors)}")

  backgrounds = data.get("backgrounds", {})
  background_cover = parse_background(backgrounds.get("cover", data.get("background_image")))
  background_pages = parse_background(backgrounds.get("pages", backgrounds.get("cover")))

  # Process pages_list
  pages_list_raw = backgrounds.get("pages_list", [])
  background_pages_list = [parse_background(bg) for bg in pages_list_raw]

  env = Environment(loader=FileSystemLoader(str(ROOT)))
  template = env.get_template("template.html")

  html_str = template.render(
    person=data["person"],
    background_image=data.get("background_image"),
    background_cover=background_cover,
    background_pages=background_pages,
    background_pages_list=background_pages_list,
    pages=pages,
  )

  # Save HTML for debugging
  html_debug_path = ROOT / "bryan-memories-debug.html"
  with open(html_debug_path, "w", encoding="utf-8") as f:
    f.write(html_str)
  print(f"Debug HTML written to {html_debug_path}")

  output_path = ROOT / "bryan-memories.pdf"
  HTML(string=html_str, base_url=str(ROOT)).write_pdf(str(output_path))
  print(f"Written {output_path}")


if __name__ == "__main__":
  render_pdf()
