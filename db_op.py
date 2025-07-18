from sqlalchemy import text
from app import db, app, Program

"""def add_user_code_column():
    try:
        with db.engine.connect() as connection:
            # For PostgreSQL/SQLite/MySQL
            connection.execute(text("ALTER TABLE user ADD COLUMN user_code VARCHAR(20)"))
            
            # For SQL Server:
            # connection.execute(text("ALTER TABLE users ADD user_code VARCHAR(20)"))
            
            connection.commit()
            print("Column added successfully")
    except Exception as e:
        print(f"Error adding column: {e}")
        connection.rollback()


with app.app_context():
    add_user_code_column()"""






















def remove_program(slug):
    try:
        program = Program.query.filter_by(slug=slug).first()
        if program:
            # Check if there are any subscriptions first
            if program.subscriptions:
                return False, "Cannot delete - program has active subscriptions"
            
            db.session.delete(program)
            db.session.commit()
            return True, f"Program '{program.name}' deleted successfully"
        return False, "Program not found"
    except Exception as e:
        db.session.rollback()
        return False, f"Error deleting program: {str(e)}"

with app.app_context():
    success, message = remove_program('innovator')
    print(message)