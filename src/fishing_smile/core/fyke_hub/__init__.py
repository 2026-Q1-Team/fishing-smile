from fastapi import FastAPI, Request
from pydantic import (
    BaseModel,
    Field,
)
import pymysql

from fishing_smile.settings import get_settings
from sqlmodel import Field, Session, select
from fishing_smile.database.engine import engine
from fishing_smile.database.sqlmodel import SQLModel
from fishing_smile.core.model import *
from datetime import datetime
import hashlib
import json

settings = get_settings()
app = FastAPI(title = 'Fyke Hub: Handling interactions from anti-phish training participants')


# TODO: Each endpoint should be defined as part of an attack component
# instead of being hardcoded in fyke_hub server.
@app.get('/change_password')
async def change_password_ui(
    k: str,
    request: Request
):
    client_host = request.client.host # This is used to get ip
    try:
        with Session(engine) as session:
            result1 = session.exec(
                select(AttackTable)
                    .where(AttackTable.external_id == str(k))
            ).first()
            time = datetime.now()
            detail_json = json.dumps({'ip': client_host})
            event = EventTable(parent_attack_id=result1.id, kind="Email sent, Link clicked", time=time, detail=detail_json)
            session.add(event)
            session.commit()
            session.refresh(event) 
            return json.dumps({
                "k" : k,
                "result" : result1.id,
                "kind" : "Email sent, Link clicked",
                "time" : str(time),
                "event" : str(event.model_dump()),
                "detail" : detail_json
            })
    except Exception as e:
        return f"error: {e}"
        
    # TODO: shouldn't this also serve next-stage HTML payload?
    # TODO: Log error when key does not match.
    # Currently it just does not insert because select is empty.


class ChangePasswordApiBody(BaseModel):
    k: str = Field(description = 'Key identifying attack instance (fishcast)')
    p: str = Field(description = 'Old password phish target gave out')


@app.post('/api/change_password')
async def change_password_api(
    body: ChangePasswordApiBody,
    request: Request
):
    client_host = request.client.host
    try:
        with Session(engine) as session:
            result1 = session.exec(
                select(AttackTable)
                    .where(AttackTable.external_id == str(body.k))
            ).first()

            hashed_password = hashlib.sha256(body.p.encode('utf8')) # hash password
            time = datetime.now()
            detail_json = json.dumps({'ip': client_host, 'password' : hashed_password.hexdigest()})
            event = EventTable(parent_attack_id=result1.id, kind="Email sent, Link clicked, Password inserted", time=time, detail=detail_json)
            session.add(event)
            session.commit()
            session.refresh(event) 
            return json.dumps({
                "k" : body.k,
                "result" : result1.id,
                "kind" : "Email sent, Link clicked, Password inserted",
                "time" : str(time),
                "event" : str(event.model_dump()),
                "detail" : detail_json
            })
    except Exception as e:
        return f"error: {e}"

    # This is the end of "change password" attack scheme.
    # TODO: Serve HTML explaining the red-flags of this attack scheme
    # to the user who fell through.
    # TODO: Log error when key does not match.
    # Currently it just does not insert because select is empty.
