from fastapi import APIRouter

from app.db import database

router = APIRouter()


@router.get('/')
def test_action():
    print(database.collection_names())
    return {
        'ping': 'pong'
    }
