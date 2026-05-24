"""Legacy entry point — use `python run.py` instead."""

from run import app

if __name__ == "__main__":
    import os

    from app.config import Config

    port = int(os.getenv("PORT", Config.PORT))
    app.run(debug=True, port=port, host="127.0.0.1")
