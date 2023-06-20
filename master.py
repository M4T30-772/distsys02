import aiohttp
from aiohttp import web
import asyncio

async def clientdata(request):
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:8001'
        async with session.get(url) as response:
            data = await response.json()
            client_ids = data['clientID']
            word_counts = data['words']
            response_data = {'client_ids': client_ids, 'word_counts': word_counts}
            return web.json_response(response_data)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

async def worker1(request):
    data = {
        'master.py': read_file('master.py'),
        'client.py': read_file('client.py')
    }
    return web.json_response(data)

async def worker2(request):
    data = {
        'master.py': read_file('master.py'),
        'client.py': read_file('client.py')
    }
    return web.json_response(data)

async def worker3(request):
    data = {
        'master.py': read_file('master.py'),
        'client.py': read_file('client.py')
    }
    return web.json_response(data)

app = web.Application()
app.router.add_get('/', clientdata)
app.router.add_get('/worker1', worker1)
app.router.add_get('/worker2', worker2)
app.router.add_get('/worker3', worker3)
web.run_app(app, port=8080)
