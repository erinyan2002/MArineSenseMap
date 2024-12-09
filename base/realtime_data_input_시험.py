import pandas as pd
import numpy as np
import datetime
import random
import os
from firebase_admin import initialize_app, credentials, db
from datetime import datetime, timedelta
import time
import threading

min_values = {
    "temperature": 12.92,
    "salinity": 29.06,
    "pH": 8.05,
    "dissolved_oxygen": 7.6,
    "COD": 1.03,
    "chlorophyll": 0.43,
    "TN": 121.6,
    "DIP": 4.1,
    "TP": 13.6,
    "Si_OH4": 100.9,
    "SPM": 4.4,
    "DIN": 30.2
}
max_values = {
    "temperature": 18.95,
    "salinity": 33.87,
    "pH": 8.26,
    "dissolved_oxygen": 10.04,
    "COD": 2.21,
    "chlorophyll": 4.2,
    "TN": 389.0,
    "DIP": 25.9,
    "TP": 39.3,
    "Si_OH4": 476.5,
    "SPM": 50.4,
    "DIN": 237.1
}
ranges = {
    '제주도 ': {'lat': (31.0, 34.50), 'lon': (121.8, 129.3)},
    '동중국해(제주도 아래)': {'lat': (28.0, 31.0), 'lon': (122.0, 130.0)},
    '황해 1': {'lat': (34.5, 35.8), 'lon': (120.1, 126.20)},
    '황해 2': {'lat': (35.8, 36.8), 'lon': (121.1, 126.50)},
    '동해 아래 1': {'lat': (37.3, 41.5), 'lon': (128.8, 138.5)},
    '동해 아래 2': {'lat': (35.4, 41.5), 'lon': (130.5, 135.5)},
    '동해 위': {'lat': (41.5, 42.5), 'lon': (130.2, 139.5)},
    '후쿠오카 한국': {'lat': (33.58, 34.84), 'lon': (127.78, 130.26)},
}


def get_area_name(lat, lon):
    for area, range_values in ranges.items():  # 변수 이름을 range_values로 변경
        if range_values['lat'][0] <= lat <= range_values['lat'][1] and range_values['lon'][0] <= lon <= range_values['lon'][1]:
            return area
    return None


num_rows = 1
random_columns = list(min_values.keys())

current_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(
    current_dir, 'asia-404305-firebase-adminsdk-c5mjl-1579518c37.json')
cred = credentials.Certificate(cred_path)
app = initialize_app(
    cred, {'databaseURL': 'https://asia-404305-default-rtdb.firebaseio.com/'})

table_names = [f"A-{i:02}" for i in range(1, 51)]  # A-01부터 A-02까지의 테이블명을 리스트화
last_move_numbers = {name: 0 for name in table_names}  # 각 테이블의 마지막 move 번호
table_counters = {name: 1 for name in table_names}
latest_data = None
last_key = None

DIRECTION_RANGE = (0, 360)
new_direction = None

SHIP_SPEEDS = {
    'tanker': 22,
    'ferry': 40,
    'fishing_boat': 47,
    'high_speed_ferry': 66,
    'boat': 74,
}

SHIP_PROBABILITIES = {
    'tanker': 0.2,
    'ferry': 0.3,
    'fishing_boat': 0.25,
    'high_speed_ferry': 0.15,
    'boat': 0.1,
}
# ship_type, AVERAGE_SPEED, DISTANCE_CHANGE_RANGE = select_ship_and_speed(SHIP_SPEEDS, SHIP_PROBABILITIES)

ship_type = np.random.choice(list(SHIP_PROBABILITIES.keys()), p=list(SHIP_PROBABILITIES.values()))
AVERAGE_SPEED = SHIP_SPEEDS[ship_type]

SPEED_VARIATION = 0.2 # 20% variation

min_speed = AVERAGE_SPEED * (1 - SPEED_VARIATION) # 80% of average speed
max_speed = AVERAGE_SPEED * (1 + SPEED_VARIATION) # 120% of average speed

TIME_INTERVAL = 1 # hour
DISTANCE_CHANGE_RANGE = (min_speed * TIME_INTERVAL, max_speed * TIME_INTERVAL)


def process_table(table_name):
    new_area = None
    last_move_number = last_move_numbers[table_name]
    ref = db.reference(table_name)
    new_time = datetime.now()
    sea = random.choice(list(ranges.keys()))  # 해역을 랜덤으로 선택
    new_lat = round(random.uniform(*ranges[sea]['lat']), 4)
    new_lon = round(random.uniform(*ranges[sea]['lon']), 4)
    new_direction = np.random.randint(*DIRECTION_RANGE)

    latest_data = ref.order_by_key().limit_to_last(1).get()

    if latest_data:  # 데이터가 있을 경우
        while True:
            latest_key = list(latest_data.keys())[0]
            latest_move_number = int(latest_key[4:])
            if latest_move_number > last_move_number:
                last_move_number = latest_move_number
                print(f'Processed: {latest_key}')
                time.sleep(3)
                break
            else:
                time.sleep(3)

        latest_time_data = latest_data[latest_key]
        latest_time_str = latest_time_data['times']
        latest_time = datetime.strptime(latest_time_str, "%Y-%m-%d %H:%M:%S")
        new_time = latest_time + timedelta(hours=1)

        latest_direction = latest_data[latest_key]['direction']  
        min_direction = (latest_direction - 45) % 360  
        max_direction = (latest_direction + 45) % 360 
        if min_direction > max_direction:
            new_direction = np.random.randint(0, max_direction + 1) if random.random() > 0.5 else np.random.randint(min_direction, 360)
        else:
            new_direction = np.random.randint(min_direction, max_direction + 1) 

        current_lat = latest_time_data['latitude']
        current_lon = latest_time_data['longitude']
        sea = latest_time_data['area']

        distance_change = np.random.uniform(*DISTANCE_CHANGE_RANGE)

        lat_change = distance_change * np.sin(np.radians(new_direction))
        lon_change = distance_change * np.cos(np.radians(new_direction))

        new_lat = current_lat + lat_change
        new_lon = current_lon + lon_change

        new_lat = round(new_lat, 4)
        new_lon = round(new_lon, 4)

        new_area = get_area_name(new_lat, new_lon)
        if new_area is None: 
            sea = "지역외"
        else:  
            sea = new_area


    else:  # 데이터가 없을 경우 현재 시간 사용
        new_time = datetime.now()

        new_direction = np.random.randint(*DIRECTION_RANGE)


    # print(new_time)
    print(sea)
    fixed_values = {
        "times": new_time.strftime("%Y-%m-%d %H:%M:%S"),
        "area": sea,
        "layer_name": "표층",
    }
    # 랜덤 데이터 생성 

    random_data = {}
    for column in random_columns:
        raw_data = np.random.uniform(
            min_values[column], max_values[column], num_rows)
        # 소수점 두 자리까지 반올림 
        random_data[column] = np.around(raw_data, 2)

    # 고정값과 랜덤 데이터를 단일 DataFrame으로 결합 
    df_random = pd.DataFrame({**fixed_values, **random_data})

    df_random.reset_index(drop=True, inplace=True)
    df_random.index += 1

    start, end, step = 1, 6, 1
    df_random['SD'] = np.round(np.random.choice(
        np.arange(start, end + step, step), num_rows), 1)

    # 수질 평가 지수를 계산합니다 

    DOValue = df_random['dissolved_oxygen']
    ChlValue = df_random['chlorophyll']
    DINValue = df_random['DIN']
    DIPValue = df_random['DIP']

    DOValue = (DOValue / 9.1) * 100
    if new_area is None:
        result_re = 0
    else:
        if DOValue.item() > 90:
            DoValue_DO = 1
        elif DOValue.item() > 81:
            DoValue_DO = 2
        elif DOValue.item() > 67.5:
            DoValue_DO = 3
        elif DOValue.item() > 45:
            DoValue_DO = 4
        else:
            DoValue_DO = 5

        if ChlValue.item() < 6.3:
            ChlValue_Chl = 1
        elif ChlValue.item() < 6.93:
            ChlValue_Chl = 2
        elif ChlValue.item() < 7.88:
            ChlValue_Chl = 3
        elif ChlValue.item() < 9.45:
            ChlValue_Chl = 4
        else:
            ChlValue_Chl = 5

        if DINValue.item() < 220:
            DINValue_DIN = 1
        elif DINValue.item() < 242:
            DINValue_DIN = 2
        elif DINValue.item() < 275:
            DINValue_DIN = 3
        elif DINValue.item() < 330:
            DINValue_DIN = 4
        else:
            DINValue_DIN = 5

        if DIPValue.item() < 35:
            DIPValue_DIP = 1
        elif DIPValue.item() < 38.50:
            DIPValue_DIP = 2
        elif DIPValue.item() < 43.75:
            DIPValue_DIP = 3
        elif DIPValue.item() < 52.50:
            DIPValue_DIP = 4
        else:
            DIPValue_DIP = 5

        result = 10 * DoValue_DO + 6 * \
            ((ChlValue_Chl + df_random['SD']) / 2) + \
            4 * ((DINValue_DIN + DIPValue_DIP) / 2)
        result_re = result

        if result_re.item() <= 23:
            result_re = 1
        elif result_re.item() <= 33:
            result_re = 2
        elif result_re.item() <= 46:
            result_re = 3
        elif result_re.item() <= 59:
            result_re = 4
        else:
            result_re = 5
        print(result_re)

    df_random['Grade'] = result_re
    # print(df_random['Grade'])

    df_random['latitude'] = new_lat
    df_random['longitude'] = new_lon
    df_random['direction'] = new_direction

    columns_order = ['times', 'latitude', 'longitude', 'Grade', 'area', 'direction', 'layer_name', 'temperature', 'salinity',
                'pH', 'dissolved_oxygen', 'COD', 'chlorophyll', 'TN', 'DIP', 'TP', 'Si_OH4', 'SPM', 'DIN', 'SD']

    df_random = df_random[columns_order]

    ref = db.reference(table_name)

    i = table_counters[table_name] 
    key = f"move{i:02}"

    ref.child(key).set(df_random.to_dict(orient='records')[0])

    # print(f"{table_name}: {df_random}")
    # print(df_random.head())

    table_counters[table_name] += 1  


while True:
    threads = []
    for table_name in table_names:
        thread = threading.Thread(target=process_table, args=(table_name,))
        thread.start()
        threads.append(thread)

    # 모든 스레드가 종료될 때까지 대기
    for thread in threads:
        thread.join()

    # 필요한 경우 전체 루프의 지연을 추가 (예: time.sleep(10))
