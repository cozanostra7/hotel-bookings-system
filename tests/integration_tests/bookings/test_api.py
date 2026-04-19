

async def test_add_bookings(db,authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post('/bookings',
                        json={
                            'room_id':room_id,
                            'date_from':'2026-01-19',
                            'date_to':'2026-01-29',
                        })
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res,dict)
    assert res['status'] == 'Ok'
 
   
    assert 'data' in res
