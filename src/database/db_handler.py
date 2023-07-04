from sqlalchemy import create_engine
from sqlalchemy.engine import URL


class DBHandler:
    drivername : str
    username : str
    host : str
    database : str
    password : str
        
    url = URL.create(
        drivername="postgresql",
        username="verdete",
        host="localhost",
        database="verdete",
        password="123456"
    )
    engine = create_engine(url)
    connection = engine.connect()   