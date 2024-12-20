import asyncio
import websockets # type: ignore
import json
import pytz
from datetime import datetime, timezone

ais_API_KEY= "910382efc9331d0e1e5875ec1cb0952c38d46af2"

async def connect_ais_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": ais_API_KEY, "BoundingBoxes": [[[38.48612617288902, 121.11894601803752], [34.16626273878638, 130.89015000762663]]], "FiltersShipMMSI": ["440016180"], "FilterMessageTypes": ["PositionReport"]}

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            ais_message = message['Message']['PositionReport']
            utc_time = datetime.now(timezone.utc)
            kst_time = utc_time.astimezone(pytz.timezone('Asia/Seoul'))

            print(f"[{kst_time}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']}")

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())
