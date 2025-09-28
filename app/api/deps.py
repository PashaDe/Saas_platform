from fastapi import Depends

from app.config.database import get_session


def get_db(session=Depends(get_session)):
    return session


