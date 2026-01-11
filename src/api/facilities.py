from fastapi import APIRouter,Body
from src.api.dependencies import DBDep
from src.schemas.facilitites import FacilityAdd
from fastapi_cache.decorator import cache

from src.tasks.tasks import test_task

router= APIRouter(prefix = '/facilities',tags=['Facilities'])

@router.get('')
@cache(expire=10)
async def get_all_facilities(db:DBDep):
        test_task.delay()
        return await db.facilities.get_all()


@router.post('')
async def create_facilities(db:DBDep,facility_info:FacilityAdd = Body()):
    facility = await db.facilities.add(facility_info)
    await db.commit()


    return {"status": "OK", "data": facility}