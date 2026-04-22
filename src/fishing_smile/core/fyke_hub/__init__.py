from pathlib import Path

from argon2 import PasswordHasher
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from fishing_smile.core.model import *
from fishing_smile.database.engine import get_session
from fishing_smile.settings import get_settings

settings = get_settings()
app = FastAPI(title = 'Fyke Hub: Handling interactions from anti-phish training participants')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CheckInputPayload(BaseModel):
    k: str = Field(description = 'Key identifying attack instance (fishcast)')
    p: str = Field(description = 'Payload that victim input')

def create_endpoint(scheme_name, component, method):
    async def universal_endpoint(
        request: Request,
        k: str | None = None,
        p: str | None = None,
        body: CheckInputPayload | None = None,
        session: Session = Depends(get_session),
    ):
        if k != None:
            attack = session.exec(
                select(AttackTable)
                .where(AttackTable.external_id == k)
            ).first()
        elif body != None:
            attack = session.exec(
                select(AttackTable)
                .where(AttackTable.external_id == body.k)
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
        elif component.templates['eventdetail'].value == 'ip, password':
            hashed_password = PasswordHasher().hash(body.p)
            event_detail  = {
                'ip': request.client.host,
                'password' : hashed_password,
            }
            event = EventTable(
                parent_attack_id = attack.id,
                kind = str(component.templates['eventkind'].value),
                detail = event_detail,
            )
            session.add(event)
            session.commit()


        scheme = attack.scheme
        if method == 'GET':
            html_content = component.templates['html'].jinja.render(attack = attack)
            return HTMLResponse(content = html_content)
        elif method == 'POST':
            all_red_flags = []
            for comp in scheme.components:
                all_red_flags.extend(comp.red_flags)

            html_content = component.templates['html'].jinja.render(
                scheme_name=scheme.name,
                description=scheme.description or "",
                red_flags=[
                    {"name": rf.name, "explanation": rf.explanation}
                    for rf in all_red_flags
                ],
            )
            return HTMLResponse(content=html_content)
    return universal_endpoint


for scheme_name in standard_schemes.schemes:
    webpage_path = Path(__file__).resolve().parent.parent / "model" / "attack_schemes" / scheme_name
    app.mount(f'/{scheme_name}', StaticFiles(directory=f'{webpage_path}'), name=f"/{scheme_name}")
    for component in standard_schemes.get(scheme_name).components:
        if (
            component.kind != 'web'
            or component.templates['method'].value not in ('GET', 'POST')
        ):
            continue
        app.add_api_route(
            path=  component.templates['url'].value,
            endpoint=create_endpoint(scheme_name=scheme_name, component=component, method=component.templates['method'].value),
            methods=[component.templates['method'].value],
            response_class=HTMLResponse,
        )

