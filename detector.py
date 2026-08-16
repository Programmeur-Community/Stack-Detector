import re
import json
import httpx
from bs4 import BeautifulSoup


with open("signatures.json", "r", encoding="utf-8") as f:
  signatures = json.load(f)


def detect_technologies(response: httpx.Response) -> list:
  soup = BeautifulSoup(response.text, "html.parser")
  detected = []

  html_text = response.text
  headers = {k.lower(): v for k, v in response.headers.items()}
  cookies = list(response.cookies.keys())
  scripts_src = [s["src"] for s in soup.find_all("script", src=True)]
  inline_scripts = [s.get_text(" ", strip=True) for s in soup.find_all("script") if s.get_text(strip=True)]
  link_href = [l["href"] for l in soup.find_all("link", href=True)]

  for tech in signatures:
    rules = tech.get("rules", {})
    is_detected = False
    source = ""

    # ici on vérifie les headers
    for h_rule in rules.get("headers", []):
      h_name = h_rule["name"].lower()
      if h_name in headers:
        pattern = h_rule.get("pattern")
        if not pattern or re.search(pattern, headers[h_name], re.I):
          is_detected = True
          source = "En-têtes HTTP"
          break

    # ici on vérifie les cookies
    if not is_detected and rules.get("cookies"):
      for cookies_pattern in rules["cookies"]:
        if any(re.search(cookies_pattern, c, re.I) for c in cookies):
          is_detected = True
          source = "Cookies"
          break

    # Ici on vérifie les balises meta
    if not is_detected and rules.get("meta"):
      for m_rule in rules["meta"]:
        meta_tag = soup.find("meta", attrs={"name": re.compile(f"^{m_rule['name']}$", re.I)})
        if meta_tag:
          pattern = m_rule.get("pattern")
          if not pattern or (meta_tag.get("content") and re.search(pattern, meta_tag["content"], re.I)):
            is_detected = True
            source = "<meta name='' />"
            break

    # On vérifie le contenu des scripts inline
    if not is_detected and rules.get("script_contents"):
      for script_pattern in rules["script_contents"]:
        if any(re.search(script_pattern, script_text, re.I) for script_text in inline_scripts):
          is_detected = True
          source = "<script></script>"
          break

    # On vérifie les scripts src
    if not is_detected and rules.get("scripts"):
      for script_pattern in rules["scripts"]:
        if any(re.search(script_pattern, src, re.I) for src in scripts_src):
          is_detected = True
          source = "<script src=''></script>"
          break

    # On vérifie les links href
    if not is_detected and rules.get("links"):
      for link_pattern in rules["links"]:
        if any(re.search(link_pattern, href, re.I) for href in link_href):
          is_detected = True
          source = "<link href=''></link>"
          break

    # Ici on vérifie les classes HTML
    if not is_detected and rules.get("html_classes"):
      for class_pattern in rules["html_classes"]:
        if re.search(r'class=["\'][^"\']*' + class_pattern, html_text, re.I):
          is_detected = True
          source = "Classes HTML"
          break

    # Ici on vérifie les attributs HTML
    if not is_detected and rules.get("attributes"):
      for attr in rules["attributes"]:
        if soup.find(attrs={attr: True}):
          is_detected = True
          source = "Attributs HTML"
          break

    if is_detected:
      detected.append({
        "name": tech["name"],
        "description": tech["description"],
        "category": tech["category"],
        "source": source
      })

  return detected
