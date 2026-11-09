
from flask import Flask, render_template, request
from github_search import search_repositories, GitHubSearchError


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    results = []
    error = None
    searched = False

    if request.method == "POST":
        searched = True

        query = request.form.get("query", "").strip()
        language = request.form.get("language", "").strip()

        try:
            min_stars = int(request.form.get("min_stars", 0))
            per_page = int(request.form.get("per_page", 10))

            sort = request.form.get("sort", "stars")

            if min_stars < 0:
                raise ValueError("Minimum Stars cannot be negative.")

            if not 1 <= per_page <= 100:
                raise ValueError("Results must be between 1 and 100.")

            results = search_repositories(
                query=query,
                language=language or None,
                min_stars=min_stars,
                sort=sort,
                per_page=per_page
            )

        except ValueError as exc:
            error = str(exc)

        except GitHubSearchError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        results=results,
        error=error,
        searched=searched
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
