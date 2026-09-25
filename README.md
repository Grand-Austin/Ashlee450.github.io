# Updating the website

- Home page headings and profile links: edit `content/home.md`.
- About section: edit `content/about.md`. The `name` field sets the name below the avatar.
- Education: edit `content/education.md`. Put school images in `assets/` and reference them in the Markdown file.
- Publications and projects: edit `content/publications.md` and `content/projects.md`.
- Avatar: replace `assets/avatar.svg`.
- CV: replace `assets/aoxue_li_cv.pdf` with the new PDF, keeping the same filename.

Commit and push changes to `main` to update the GitHub Pages site. To preview locally, install the packages in `requirements.txt`, run `python build.py`, then run `python -m http.server 8000 --directory site` and open <http://localhost:8000>.
