
from fastapi import APIRouter, Response, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import xml.etree.ElementTree as ET

db_url = str(os.getenv('DB_URL'))
router = APIRouter(prefix='/xml_file')
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

def validate_xml_str(data:str)->bool:
    try:
        # Can do more validation later
        tree = ET.fromstring(data)
    except Exception:
        return False
    return True

@router.get('/')
def get_xml_files()->dict:
    session = SessionLocal()

    res = session.execute(text(
        """SELECT id, xml_data from xmlfiles
        """
    ))

    values = {}
    for value in res.all():
        values[value[0]] = value[1]
    session.close()

    return values

@router.get('/{id}')
def get_xml_file_by_id(id:int)->dict:
    session = SessionLocal()
    res = session.execute(text(
        """SELECT id, xml_data from xmlfiles WHERE id={}
        """.format(id)
    ))
    values = {}
    for value in res.all():
        values[value[0]] = value[1]
    session.close()

    if len(values) == 0:
        raise HTTPException(status_code=404, detail='record not found')

    return values


@router.post('/')
def receive_xml_file(xml_data:str)->str:
    if not validate_xml_str(xml_data):
        raise HTTPException(status_code=400, detail='invalid xml data')
    session = SessionLocal()
    session.execute(text("""
        INSERT INTO xmlfiles(xml_data)
            VALUES('{}'::xml);
    """.format(xml_data)))
    session.commit()
    session.close()
    return 'Received'