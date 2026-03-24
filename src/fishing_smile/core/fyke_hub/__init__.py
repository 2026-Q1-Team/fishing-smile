from datetime import datetime
from pathlib import Path
import hashlib

from fastapi.openapi.models import Components
from jinja2 import Template
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
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

# Dynamic Endpoint Creation
for scheme_name in standard_schemes.schemes:
    for component in standard_schemes.get(scheme_name).components:
        if component.kind == 'web' and component.templates['method'].value == 'GET':
            def create_endpoint(scheme_name):
                async def universal_endpoint(
                    k: str,
                    request: Request,
                    session: Session = Depends(get_session),
                ):
                    attack = session.exec(
                        select(AttackTable)
                            .where(AttackTable.external_id == k)
                    ).first()
                    if (
                        attack == None
                        or attack.scheme_name != scheme_name
                    ):
                        raise HTTPException(
                            status_code = 404,
                            # NOTE: Report error using the neutral term `session` instead of `attack`
                            # because at this point we are still trying to deceive target.
                            detail = 'Key does not match existing session',
                        )

                    event_detail = {}
                    if component.templates['eventdetail'].value == 'ip':
                        event_detail  = {'ip': request.client.host} 
                    event = EventTable(
                        parent_attack_id = attack.id,
                        kind = component.templates['eventkind'].value,
                        detail = event_detail,
                    )
                    session.add(event)
                    session.commit()

                    scheme = attack.scheme
                    html_component = scheme.components.first(kind = 'web')
                    html_content = html_component.templates['html'].jinja.render(attack = attack)
                    return HTMLResponse(content = html_content)
                return universal_endpoint

            app.add_api_route(
                path= standard_schemes.get(scheme_name).components.first(kind = 'web').templates['url'].value,
                endpoint=create_endpoint(scheme_name=scheme_name),
                methods=["GET"],
                response_class=HTMLResponse
            )

        elif component.kind == 'web' and component.templates['method'].value == 'POST':
            class ChangePasswordApiBody(BaseModel):
                k: str = Field(description = 'Key identifying attack instance (fishcast)')
                p: str = Field(description = 'Old password phish target gave out')

            def create_endpoint(scheme_component):
                async def universal_endpoint(
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
                        
                    event_detail = {}
                    if scheme_component.templates['eventdetail'].value == 'ip, password':
                        hashed_password = hashlib.sha256(body.p.encode('utf8'))
                        event_detail  = {
                            'ip': request.client.host,
                            'password' : hashed_password.hexdigest(),
                        }
                    event = EventTable(
                        parent_attack_id = attack.id,
                        kind = str(scheme_component.templates['eventkind'].value),
                        detail = event_detail,
                    )
                    session.add(event)
                    session.commit()

                    scheme = attack.scheme
                    all_red_flags = []
                    for component in scheme.components:
                        all_red_flags.extend(component.red_flags)

                    html_component = scheme.components.first(name ='form_page')
                    html_content = html_component.templates['html'].jinja.render(
                        scheme_name=scheme.name,
                        description=scheme.description or "",
                        red_flags=[
                            {"name": rf.name, "explanation": rf.explanation}
                            for rf in all_red_flags
                        ],
                    )
                    return HTMLResponse(content=html_content)
                return universal_endpoint

            app.add_api_route(
                path= component.templates['url'].value,
                endpoint=create_endpoint(scheme_component=component),
                methods=["POST"],
                response_class=HTMLResponse
            )

