from fastapi import APIRouter, Request, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from bson import ObjectId

import io

from app.db import database


router = APIRouter()


@router.get('/')
def get_images_by_attributes(request: Request):
    query = {'status': 'PROCESSED'}
    for key, value in request.query_params.items():
        query[f'attribute_values.{key}'] = value
    images = database.images.find(query, {'data': False})

    return [
        {
            'id': str(image['_id']),
            'filename': image['filename'],
            'ext': image['ext'],
            'elapsed_time': image['elapsed_time'],
            'attribute_values': image['attribute_values'],
        }
        for image in images
    ]


@router.post('/')
async def upload_image(file: UploadFile = File(...)):
    if file.content_type.startswith('image/'):
        _, ext = file.content_type.split('/')
        data = await file.read()
        filename = file.filename
        image_id = database.images.insert_one(
            {'data': data, 'filename': filename, 'ext': ext, 'status': 'PENDING'}
        ).inserted_id
        return {'id': str(image_id)}
    return {'file_size': file.filename, 'mimetype': file.content_type}


@router.get('/{image_id}')
def get_image_id(image_id: str):
    image_id = ObjectId(image_id)
    image = database.images.find_one({'_id': image_id})
    if image is None:
        raise HTTPException(status_code=404, detail='Image not found')
    mimetype = f'image/{image["ext"]}'
    return StreamingResponse(io.BytesIO(image['data']), media_type=mimetype)
