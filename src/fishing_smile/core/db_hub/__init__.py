from fastapi import (
    FastAPI,
    Depends,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

import pymysql
import sqlalchemy as sa
from sqlmodel import (
    Session,
    select,
)

from fishing_smile.settings import get_settings
from fishing_smile.database.engine import get_session
from fishing_smile.core.model import *


settings = get_settings()
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


# TODO: Replace usage of `_get_connection` with dependency injection of `get_session`
# See https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/#use-the-dependency
def _get_connection():
    db = settings.db
    return pymysql.connect(
        host=db.host,
        port=db.port,
        user=db.username,
        password=db.password,
        database=db.database,
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.get('/api/tracking', response_model=list[TrackingResponse])
async def get_tracking():
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    a.id              AS attack_id,
                    tp.email          AS email,
                    a.scheme_name     AS scheme_name,
                    e_sent.time       AS sent_ts,
                    e_click.time      AS click_ts,
                    e_submit.time     AS submit_ts,
                    e_submit.detail   AS detail,
                    CASE
                        WHEN e_submit.id IS NOT NULL THEN 'submitted'
                        WHEN e_click.id  IS NOT NULL THEN 'clicked'
                        ELSE 'sent'
                    END AS status
                FROM attack a
                JOIN target_profile tp ON a.target_id = tp.id
                LEFT JOIN event e_sent
                    ON e_sent.parent_attack_id = a.id AND e_sent.kind = 'sent'
                LEFT JOIN event e_click
                    ON e_click.parent_attack_id = a.id AND e_click.kind = 'click'
                LEFT JOIN event e_submit
                    ON e_submit.parent_attack_id = a.id AND e_submit.kind = 'submit'
                ORDER BY a.id
            """)
            rows = cur.fetchall()
    return rows


@app.get('/api/campaigns')
async def get_campaigns(
    session: Session = Depends(get_session),
) -> list[CampaignResponse]:
    rows = session.exec(
        select(
            AttackTable.id.label('uid'),
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
    ).all()
    return rows


@app.get('/api/dashboard')
async def get_dashboard_data():
    campaigns = await get_campaigns()
    tracking = await get_tracking()
    return {
        'campaigns': campaigns,
        'tracking': tracking,
    }
