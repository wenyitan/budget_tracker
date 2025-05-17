from api.app_factory import create_app
from config.config import env

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port="4000" if env=="dev" else "5000")
    ## to start app, run docker compose up api-dev