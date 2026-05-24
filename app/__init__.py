from flask import Flask

from app.config import Config
from app.extensions import csrf, db, login_manager
from app.models import AdminUser, Customer


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_key):
        if not user_key:
            return None
        if user_key.startswith("admin:"):
            return AdminUser.query.get(int(user_key.split(":", 1)[1]))
        if user_key.startswith("customer:"):
            return Customer.query.get(user_key.split(":", 1)[1])
        return None

    from app.blueprints.admin import bp as admin_bp
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.customer import bp as customer_bp
    from app.blueprints.main import bp as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(customer_bp, url_prefix="/customer")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    register_cli(app)
    register_template_filters(app)

    return app


def register_template_filters(app):
    from datetime import datetime

    @app.context_processor
    def inject_globals():
        return {"current_year": datetime.now().year}

    @app.template_filter("currency")
    def currency_filter(value):
        try:
            return f"PKR {float(value):,.0f}"
        except (TypeError, ValueError):
            return "PKR 0"


def register_cli(app):
    import click

    @app.cli.command("init-db")
    @click.option("--seed", is_flag=True, default=True, help="Load demo data")
    def init_db(seed):
        """Create tables and optional seed data."""
        from app.seed import run_seed

        db.create_all()
        if seed:
            run_seed()
        click.echo("Database initialized.")

    @app.cli.command("hash-passwords")
    def hash_passwords():
        """Migrate plain-text passwords to hashed values."""
        from app.seed import hash_legacy_passwords

        count = hash_legacy_passwords()
        click.echo(f"Updated {count} password(s).")
