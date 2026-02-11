from fastapi import FastAPI
from pydantic import (
    BaseModel,
    Field,
)
import pymysql

from fishing_smile.settings import get_settings


settings = get_settings()
app = FastAPI(title = 'Fyke Hub: Handling interactions from anti-phish training participants')


# TODO: Each endpoint should be defined as part of an attack component
# instead of being hardcoded in fyke_hub server.
@app.get('/change_password')
async def change_password_ui(
    k: str,
):
    """Simulate fake "change password" HTML page.

    Also track the participant who visit this endpoint.
    """
    with pymysql.connect(**settings.db.model_dump()) as connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO fishhook(`ID`, `KEY`, `CLICK`)
                SELECT `ID`, `KEY`, NOW()
                FROM fishcast
                WHERE `KEY` = %s
            """
            # TODO: Log error when key does not match.
            # Currently it just does not insert because select is empty.
            cursor.execute(sql, (k,))
        connection.commit()
    # TODO: shouldn't this also serve next-stage HTML payload?


class ChangePasswordApiBody(BaseModel):
    k: str = Field(description = 'Key identifying attack instance (fishcast)')
    p: str = Field(description = 'Old password phish target gave out')


@app.post('/api/change_password')
async def change_password_api(
    body: ChangePasswordApiBody,
):
    """Simulate fake "change password" API.

    Also track the participant who visit this endpoint.
    """
    with pymysql.connect(**settings.db.model_dump()) as connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO fishcook(`ID`, `KEY`, `PWND`, `TEXT`)
                SELECT `ID`, `KEY`, NOW(), %s
                FROM fishcast
                WHERE `KEY` = %s
            """
            # TODO: should not be storing plain text password
            # TODO: Log error when key does not match.
            # Currently it just does not insert because select is empty.
            cursor.execute(sql, (body.p, body.k))
        connection.commit()
    # This is the end of "change password" attack scheme.
    # TODO: Serve HTML explaining the red-flags of this attack scheme
    # to the user who fell through.

