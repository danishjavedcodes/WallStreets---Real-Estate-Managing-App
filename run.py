import os

from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.config import Config

app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", Config.PORT))
    app.run(debug=True, port=port, host="127.0.0.1")
