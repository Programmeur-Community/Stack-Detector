import os
import httpx
from flask import Flask, render_template, redirect, url_for, request, flash
from utils import validate_url
from detector import detect_technologies

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


@app.after_request
def security(response):
  response.headers["X-Frame-Options"] = "DENY"
  return response


@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    target_url = request.form.get("url", "").strip()

    if not target_url:
      return redirect(url_for("index"))

    is_valid = validate_url(target_url)
    if not is_valid:
      flash("L'URL est invalide !!")
      return redirect(url_for("index"))

    return redirect(url_for("result", url=target_url))
  
  return render_template("index.html")


@app.route("/result")
def result():
  target_url = request.args.get("url", "")

  if not target_url:
    return redirect(url_for("index"))

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
    return redirect(url_for("index"))
  except httpx.HTTPStatusError as e:
    flash(f"Un code de statut {e.response.status_code} a été retouné pendant la requete vers {e.request.url}")
    return redirect(url_for("index"))

  return render_template("result.html", url=target_url, data=data)


if __name__ == "__main__":
  app.run()
