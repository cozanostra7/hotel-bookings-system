

async def test_get_hotel(ac):
    response = await ac.get(
        '/hotels',
                params={
                    'date_from':'2026-04-19',
                    'date_to':'2026-04-29',
                            })
    print(f'{response.json()=}')
    
    assert response.status_code == 200