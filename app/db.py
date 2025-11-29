import psycopg2
import app.config as cfg

def get_conn():
    return psycopg2.connect(
        host=cfg.PGHOST,
        port=cfg.PGPORT,
        dbname=cfg.PGDATABASE,
        user=cfg.PGUSER,
        password=cfg.PGPASSWORD,
        sslmode="require",
        connect_timeout=10,
    )
