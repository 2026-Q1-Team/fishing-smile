from datetime import datetime
from pathlib import Path
import hashlib

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import (
    BaseModel,
    Field,
)
from sqlmodel import Field, Session, select

from fishing_smile.settings import get_settings
from fishing_smile.database.engine import get_session
from fishing_smile.database.sqlmodel import SQLModel
from fishing_smile.core.model import *

settings = get_settings()
app = FastAPI(title = 'Fyke Hub: Handling interactions from anti-phish training participants')
webpage_path = Path(__file__).resolve().parent.parent.parent.parent / "webpage"
app.mount('/webpage', StaticFiles(directory=f'{webpage_path}'), name="webpage")
templates = Jinja2Templates(directory=webpage_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Each endpoint should be defined as part of an attack component
# instead of being hardcoded in fyke_hub server.
@app.get('/change_password', response_class=HTMLResponse)
async def change_password_ui(
    k: str,
    request: Request,
    session: Session = Depends(get_session)
):
    result = session.exec(
        select(AttackTable)
            .where(AttackTable.external_id == k)
    ).first()
    if result == None:
        raise HTTPException(status_code=404)

    time = datetime.now()
    event = EventTable(
        parent_attack_id = result.id,
        kind = "Email.sent, Link.clicked",
        time = time,
        detail = {'ip': request.client.host},
    )
    session.add(event)
    session.commit()

    # check the attack scheme component
    scheme = AttackScheme.list()

    if result.scheme_name in AttackScheme.list():
        return templates.TemplateResponse(
            request=request, name="index.html" , context={"k": k}
        )
    else:
        raise HTTPException(status_code=404)
    # TODO: Log error when key does not match.
    # Currently it just does not insert because select is empty.


class ChangePasswordApiBody(BaseModel):
    k: str = Field(description = 'Key identifying attack instance (fishcast)')
    p: str = Field(description = 'Old password phish target gave out')


@app.post('/api/change_password', response_class=HTMLResponse)
async def change_password_api(
    body: ChangePasswordApiBody,
    request: Request,
    session: Session = Depends(get_session),
):
    result = session.exec(
        select(AttackTable)
            .where(AttackTable.external_id == str(body.k))
    ).first()
    if result == None:
        raise HTTPException(status_code=404)

    hashed_password = hashlib.sha256(body.p.encode('utf8')) # hash password
    time = datetime.now()
    event = EventTable(
        parent_attack_id = result.id,
        kind = "Email.sent, Link.clicked, Password.inserted",
        time = time,
        detail = {
            'ip': request.client.host,
            'password' : hashed_password.hexdigest(),
        },
    )
    session.add(event)
    session.commit()

    scheme = AttackScheme.list()
    for atkscheme in scheme:
        if atkscheme == result.scheme_name:
            sscheme = AttackScheme.get(result.scheme_name)

            html_content = f"""
            <html>
                <head>
                    <title>Phishing attack scheme</title>
                </head>
                <body>
                    <h1>{sscheme.name}</h1>
                    <p>{sscheme.description}</p><br>
                </body>
            </html>
            """
            return HTMLResponse(content=html_content, status_code=200)

    else:
        raise HTTPException(status_code=404, detail="Scheme doesn't match")

    # This is the end of "change password" attack scheme.
    # TODO: Log error when key does not match.
    # Currently it just does not insert because select is empty.
