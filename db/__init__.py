from db.connection import close_db
import db.terminal_commands as cmd


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(cmd.init_db_command)
    app.cli.add_command(cmd.create_admin_command)
    app.cli.add_command(cmd.ensure_admin)
    app.cli.add_command(cmd.create_employee_command)
    app.cli.add_command(cmd.master_reset_command)
