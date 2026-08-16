import httpx
from flask import Blueprint, render_template, redirect, url_for, request, flash
from utils import validate_url
from detector import detect_technologies

main = Blueprint("main", __name__)

@main.after_request
def security(response):
  response.headers["X-Frame-Options"] = "DENY"
  return response


@main.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    target_url = request.form.get("url", "").strip()

    if not target_url:
      return redirect(url_for("main.index"))

    is_valid = validate_url(target_url)
    if not is_valid:
      flash("L'URL est invalide !!")
      return redirect(url_for("main.index"))

    return redirect(url_for("main.result", url=target_url))
  
  return render_template("index.html")


@main.route("/result")
def result():
  target_url = request.args.get("url", "")

  if not target_url:
    return redirect(url_for("main.index"))

  try:
    response = httpx.get(
      url=target_url,
      timeout=10.0,
      headers={
        "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Mobile Safari/537.36",
        "Accept-Language": "fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      },
      follow_redirects=True
    )
    data = detect_technologies(response=response)
  except httpx.RequestError as e:
    flash(f"Une erreur est survenue pendant vers {e.request.url}")
    return redirect(url_for("main.index"))
  except httpx.HTTPStatusError as e:
    flash(f"Un code de statut {e.response.status_code} a été retouné pendant la requete vers {e.request.url}")
    return redirect(url_for("main.index"))

  return render_template("result.html", url=target_url, data=data)
