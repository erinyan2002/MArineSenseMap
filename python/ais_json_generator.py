import asyncio
import websockets
import json
from datetime import datetime, timezone

# 수집된 데이터를 저장할 딕셔너리 생성
data = {}

# 추적할 선박 수
number_of_ships_to_track = 5
tracked_ships = {}


async def connect_ais_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {
            "APIKey": "63a67e10bee025e05c8e7c2f6332cbdedfc570da",
            "BoundingBoxes": [[[38.48612617288902, 121.11894601803752], [34.16626273878638, 130.89015000762663]]]
        }
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                ais_message = message['Message']['PositionReport']
                print(
                    f"[{datetime.now(timezone.utc)}] 선박 ID: {ais_message['UserID']} 위도: {ais_message['Latitude']} 경도: {ais_message['Longitude']}")
                
                ship_id = ais_message['UserID']
                format_data(ais_message)  # 데이터 딕셔너리 업데이트

                # 추적 중인 선박 수 업데이트
                if ship_id not in tracked_ships:
                    tracked_ships[ship_id] = 1
                else:
                    tracked_ships[ship_id] += 1

                # 추적 중인 선박 수가 목표에 도달하면 루프를 종료
                if len(tracked_ships) >= number_of_ships_to_track:
                    break


def format_data(ais_message):
    time_key = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # UserID를 키로 사용하여 데이터 딕셔너리 업데이트
    if ais_message['UserID'] not in data:
        data[ais_message['UserID']] = {}

    data[ais_message['UserID']][time_key] = {
        "latitude": ais_message['Latitude'],
        "longitude": ais_message['Longitude'],
        "times": time_key
    }


if __name__ == "__main__":
    asyncio.run(connect_ais_stream())

# 데이터 수집 완료 후 JSON 파일에 저장
with open('json/ais_data.json', 'w') as file:
    json.dump(data, file, indent=4)
