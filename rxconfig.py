import reflex as rx

import os
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

config = rx.Config(
    app_name="proyectofinal",
    upload_dir="static",
    db_url=os.getenv("DATABASE_URL"),  # usa tu MySQL
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],  # opcional: silencia warning
)