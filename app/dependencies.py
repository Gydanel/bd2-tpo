import mysql
import neo

def get_mysql_db():
    db = mysql.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_neo4j_db():
    yield neo.driver