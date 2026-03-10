from datetime import datetime
from pathlib import Path
import hashlib

from jinja2 import Template
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
    attack = session.exec(
        select(AttackTable)
            .where(AttackTable.external_id == k)
    ).first()
    if (
        attack == None
        or attack.scheme_name != 'generic_org_change_password'
    ):
        raise HTTPException(
            status_code = 404,
            # NOTE: Report error using the neutral term `session` instead of `attack`
            # because at this point we are still trying to deceive target.
            detail = 'Key does not match existing session',
        )

    event = EventTable(
        parent_attack_id = attack.id,
        kind = "Email.sent, Link.clicked",
        detail = {'ip': request.client.host},
    )
    session.add(event)
    session.commit()

    scheme = attack.scheme
    html_content = (
        scheme
        .components.first(kind = 'html', name = 'form_page_change_password')
        .templates['html']
        .jinja.render()
    )
    return HTMLResponse(content = html_content)


class ChangePasswordApiBody(BaseModel):
    k: str = Field(description = 'Key identifying attack instance (fishcast)')
    p: str = Field(description = 'Old password phish target gave out')


@app.post('/api/change_password', response_class=HTMLResponse)
async def change_password_api(
    body: ChangePasswordApiBody,
    request: Request,
    session: Session = Depends(get_session),
):
    attack = session.exec(
        select(AttackTable)
            .where(AttackTable.external_id == body.k)
    ).first()
    if attack == None:
        raise HTTPException(
            status_code = 404,
            detail = 'Key does not match existing session',
        )

    hashed_password = hashlib.sha256(body.p.encode('utf8'))
    event = EventTable(
        parent_attack_id = attack.id,
        kind = "Email.sent, Link.clicked, Password.inserted",
        detail = {
            'ip': request.client.host,
            'password' : hashed_password.hexdigest(),
        },
    )
    session.add(event)
    session.commit()

    scheme = attack.scheme
    all_red_flags = []
    for component in scheme.components:
        all_red_flags.extend(component.red_flags)

    html_component = scheme.components.first(name ='form_page')
    html_spec = getattr(html_component, 'templates', {}).get('html')
    template_str = html_spec.value if html_spec is not None and hasattr(html_spec, 'value') else getattr(html_component, 'html_template', '') or ''
    jinja_template = Template(template_str)
    html_content = jinja_template.render(
        scheme_name=scheme.name,
        description=scheme.description or "",
        red_flags=[
            {"name": rf.name, "explanation": rf.explanation}
            for rf in all_red_flags
        ],
    )
    return HTMLResponse(content=html_content)

@app.get('/payroll_update', response_class=HTMLResponse)
async def update_payroll(
    k: str,
    request: Request,
    session: Session = Depends(get_session)
):
    client_host = request.client.host
    attack = session.exec(
        select(AttackTable).where(AttackTable.external_id == str(k))
    ).first()
    if attack == None:
        raise HTTPException(
            status_code=404,
            detail = 'Key does not match existing session',
        )

    detail_json = {'ip': client_host}
    event = EventTable(parent_attack_id=attack.id, kind="Email.sent, Link.clicked", detail=detail_json)
    session.add(event)
    session.commit()

    scheme = attack.scheme
    html_component = scheme.components.first(name = 'payroll_update_page')
    jinja_template = Template(html_component.templates['html'].value)
    html_content = jinja_template.render()
    return HTMLResponse(html_content)

@app.get('/internal/hr-portal', response_class=HTMLResponse)
async def hr_benefits_update_login(
    k: str,
    request: Request,
    session: Session = Depends(get_session)
):
    client_host = request.client.host
    attack_table = session.exec(
        select(AttackTable).where(AttackTable.external_id == str(k))
    ).first()
    if attack_table == None:
        raise HTTPException(
            status_code=404,
            detail = 'Key does not match existing session',
        )

    detail_json = {'ip': client_host}
    event = EventTable(parent_attack_id=attack_table.id, kind="Email.sent, Link.clicked", detail=detail_json)
    session.add(event)
    session.commit()

    session.refresh(attack_table)
    scheme = attack_table.scheme

    html_component = scheme.components.first(name = 'hr_login')
    jinja_template = Template(html_component.templates['html'].value)
    html_content = jinja_template.render(attack = attack_table)
    return HTMLResponse(html_content)
