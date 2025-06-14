import mysql


def get_mysql_db():
    db = mysql.SessionLocal()
    try:
        yield db
    finally:
        db.close()