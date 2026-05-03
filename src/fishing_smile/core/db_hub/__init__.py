from fastapi import (
    FastAPI,
    Depends,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    JSONResponse,
    RedirectResponse,
)
from pydantic import BaseModel
from datetime import datetime

import sqlalchemy as sa
from sqlmodel import (
    Field,
    Session,
    select,
)

from fishing_smile.database.engine import get_session
from fishing_smile.core.model import *


app = FastAPI(title='db hub: Data service for fishing-smile system')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CampaignResponse(BaseModel):
    id: int
    scheme_name: str
    targeted_count: int


class TrackingResponse(BaseModel):
    attack_id: int
    email: str
    status: str
    sent_ts: datetime | None = None
    click_ts: datetime | None = None
    submit_ts: datetime | None = None
    detail: dict | None = None


class DashboardResponse(BaseModel):
    campaigns: list[CampaignResponse]
    tracking: list[TrackingResponse]


@app.get('/api/tracking', response_model=list[TrackingResponse])
async def get_tracking(
    session: Session = Depends(get_session),
):
    e_sent = sa.orm.aliased(EventTable, name='e_sent')
    e_click = sa.orm.aliased(EventTable, name='e_click')
    e_submit = sa.orm.aliased(EventTable, name='e_submit')

    status_expr = sa.case(
        (e_submit.id.is_not(None), 'submitted'),
        (e_click.id.is_not(None), 'clicked'),
        else_='sent',
    ).label('status')

    query = (
        select(
            AttackTable.id.label('attack_id'),
            TargetProfileTable.email,
            AttackTable.scheme_name,
            e_sent.time.label('sent_ts'),
            e_click.time.label('click_ts'),
            e_submit.time.label('submit_ts'),
            e_submit.detail,
            status_expr,
        )
        .join(TargetProfileTable, AttackTable.target_id == TargetProfileTable.id)
        .outerjoin(e_sent, sa.and_(
            e_sent.parent_attack_id == AttackTable.id,
            e_sent.kind == 'sent',
        ))
        .outerjoin(e_click, sa.and_(
            e_click.parent_attack_id == AttackTable.id,
            e_click.kind == 'click',
        ))
        .outerjoin(e_submit, sa.and_(
            e_submit.parent_attack_id == AttackTable.id,
            e_submit.kind == 'submit',
        ))
        .order_by(AttackTable.id)
    )

    rows = session.exec(query).mappings().all()
    return rows


@app.get('/api/campaigns')
async def get_campaigns(
    session: Session = Depends(get_session),
) -> list[CampaignResponse]:
    rows = session.exec(
        select(
            AttackTable.id,
            AttackTable.scheme_name,
            sa.func.count(AttackTable.id).label('targeted_count'),
        )
            .group_by(
                # FIXME: It makes no sense to group by ID which is the PRIMARY KEY of the table 
                # This will always result in each row being the only member of the group.
                AttackTable.id,
                AttackTable.scheme_name,
            )
            # TODO: Might need to add `.order_by()` to make output deterministic
            # which will help with automated testing.
    ).mappings().all()
    return rows


@app.get('/api/dashboard')
async def get_dashboard_data(
    session: Session = Depends(get_session),
):
    campaigns = await get_campaigns(session)
    tracking = await get_tracking(session)
    return {
        'campaigns': campaigns,
        'tracking': tracking,
    }


class contact_security_team(BaseModel):
    k: str = Field(description = 'Key identifying attack instance (fishcast)')


@app.post('/api/contact_security_team', response_class=JSONResponse)
async def contact_security_team_api(
    body: contact_security_team,
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

    event = EventTable(
        parent_attack_id = attack.id,
        kind = "contact_security_team",
        detail = {
            'ip': request.client.host,
        },
    )
    session.add(event)
    session.commit()
    return JSONResponse({"result" : "done"})  # can change to more suitable response later. 


@app.get('/')
async def default_page():
    return RedirectResponse(
        '/dashboard',
        status_code = status.HTTP_308_PERMANENT_REDIRECT,
    )
