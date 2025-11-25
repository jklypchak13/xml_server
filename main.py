from fastapi import FastAPI, Response
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

db_url = str(os.getenv('DB_URL'))
app = FastAPI()
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

@app.post('/xml_file')
async def xml_receive(xml_data:str):
    # Do something with xml_str, e.g., store in DB
    print(xml_data)

    session = SessionLocal()

    session.execute(text("""
        INSERT INTO xmlfiles(xml_data)
            VALUES('{}'::xml);
    """.format(xml_data)))
    session.commit()
    session.close()
    return Response(content="XML received", media_type="text/plain")


@app.get('/')
def root():
    return {'hello': 'world'}

