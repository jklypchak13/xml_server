from fastapi import FastAPI
import xml_server.xml_file

app = FastAPI()
app.include_router(xml_server.xml_file.router)

@app.get('/')
def root():
    return "XML placeholder"

