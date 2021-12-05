from fastapi import APIRouter

from app.db import database


router = APIRouter()

@router.get('/attributes')
def get_attributes_list():
    """
    Get list of attributes and its values
    :return: List of attributes
    """
    collection = database.attributes.find({}, {'_id': False})
    return [attr for attr in collection]


@router.get('/breeds')
def get_breeds_list():
    """
    Get list of breeds
    :return: List of breeds
    """
    collection = database.breeds.find({}, {'_id': False})
    return [breed for breed in collection]


@router.get('/cameras')
def get_cameras_list():
    """
    Get list of available cameras
    :return: List of cameras as json
    """
    collection = database.cameras.find({}, {'_id': False})
    return [camera for camera in collection]
