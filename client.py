import pandas as pd
import aiohttp
from aiohttp import web

data = pd.read_json("main.json", lines=True)

def generate_client_ids():
    client_ids = list(range(1, 10001))
    return client_ids

def divide_dataset_to_clients(df, client_ids):
    rows_per_client = int(len(df) / len(client_ids))
    clients = {id: [] for id in client_ids}
    for client_id, codes in clients.items():
        from_row = (client_id - 1) * rows_per_client
        to_row = from_row + rows_per_client
        for _, row in df.iloc[from_row + 1:to_row + 1].iterrows():
            codes.append(row.get("content"))
    return clients

def calculate_average_word_count(codes):
    total = 0
    for code in codes:
        total += len(code.split())
    average = total / len(codes)
    return average

async def send_data_to_server(codes):
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:8081'
        data = {'codes': codes}
        async with session.post(url, json=data) as response:
            result = await response.json()
            return result['SUM']

clientID = generate_client_ids()

clients = divide_dataset_to_clients(data, clientID)

async def handle_request(request):
    client_ids = list(clients.keys())
    word_counts = [calculate_average_word_count(codes) for codes in clients.values()]
    response_data = {'clientID': client_ids, 'words': word_counts}
    return web.json_response(response_data)

app = web.Application()
app.router.add_get('/', handle_request)

web.run_app(app, port=8001)
