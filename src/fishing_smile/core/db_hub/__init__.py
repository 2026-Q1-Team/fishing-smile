from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

import pymysql

from fishing_smile.settings import get_settings

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
    uid: int
    scheme: str
    targeted_count: int


class TrackingResponse(BaseModel):
    attack_uid: int
    email: str
    status: str
    sent_ts: datetime | None = None
    click_ts: datetime | None = None
    submit_ts: datetime | None = None
    detail: dict | None = None


class DashboardResponse(BaseModel):
    campaigns: list[CampaignResponse]
    tracking: list[TrackingResponse]


def _get_connection():
    return pymysql.connect(
        **settings.db.model_dump(),
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.get('/api/tracking', response_model=list[TrackingResponse])
async def get_tracking():
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    a.uid            AS attack_uid,
                    tp.email         AS email,
                    a.scheme         AS scheme,
                    e_sent.ts        AS sent_ts,
                    e_click.ts       AS click_ts,
                    e_submit.ts      AS submit_ts,
                    e_submit.detail  AS detail,
                    CASE
                        WHEN e_submit.uid IS NOT NULL THEN 'submitted'
                        WHEN e_click.uid  IS NOT NULL THEN 'clicked'
                        ELSE 'sent'
                    END AS status
                FROM `Attack` a
                JOIN `Target Profile` tp ON a.target = tp.uid
                LEFT JOIN `Event` e_sent
                    ON e_sent.atk_id = a.uid AND e_sent.kind = 'sent'
                LEFT JOIN `Event` e_click
                    ON e_click.atk_id = a.uid AND e_click.kind = 'click'
                LEFT JOIN `Event` e_submit
                    ON e_submit.atk_id = a.uid AND e_submit.kind = 'submit'
                ORDER BY a.uid
            """)
            rows = cur.fetchall()
    return rows


@app.get('/api/campaigns', response_model=list[CampaignResponse])
async def get_campaigns():
    with _get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    a.uid,
                    a.scheme,
                    COUNT(*) AS targeted_count
                FROM `Attack` a
                GROUP BY a.uid, a.scheme
            """)
            rows = cur.fetchall()
    return rows


@app.get('/api/dashboard')
async def get_dashboard_data():
    campaigns = await get_campaigns()
    tracking = await get_tracking()
    return {
        'campaigns': campaigns,
        'tracking': tracking,
    }
