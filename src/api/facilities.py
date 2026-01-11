import json
from fastapi import APIRouter,Body
from init import redis_manager
from src.api.dependencies import DBDep
from src.schemas.facilitites import FacilityAdd

router= APIRouter(prefix = '/facilities',tags=['Facilities'])

@router.get('')
async def get_all_facilities(db:DBDep):
    facilities_from_cache = await redis_manager.get('facilities')
    print(f'{facilities_from_cache}')
    if not facilities_from_cache:
        print('I will check the database')
        facilities =  await db.facilities.get_all()
        facilities_schemas :list[dict] = [f.model_dump()for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set('facilities',facilities_json,10)
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post('')
async def create_facilities(db:DBDep,facility_info:FacilityAdd = Body()):
    facility = await db.facilities.add(facility_info)
    await db.commit()
    return {"status": "OK", "data": facility}