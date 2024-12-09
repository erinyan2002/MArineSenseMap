import random
import json
from datetime import datetime

def generate_random_coordinates(bounding_boxes, num_points_per_box):
    """
    지정된 여러 BoundingBox 내에서 랜덤한 좌표를 생성합니다.

    Parameters:
    bounding_boxes (list of lists): BoundingBox의 리스트. 각 BoundingBox는 두 개의 좌표로 정의됩니다 [bottom_left, top_right]
    num_points_per_box (int): 각 BoundingBox마다 생성할 랜덤 좌표의 개수

    Returns:
    list of dicts: 랜덤 좌표와 타임스탬프를 포함한 딕셔너리의 리스트
    """
    random_coordinates = []
    for box in bounding_boxes:
        min_lat, min_lon = box[0]
        max_lat, max_lon = box[1]
        for _ in range(num_points_per_box):
            latitude = random.uniform(min_lat, max_lat)
            longitude = random.uniform(min_lon, max_lon)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            random_coordinates.append({"latitude": latitude, "longitude": longitude, "times": timestamp})
    
    return random_coordinates

def save_to_json(data, filename):
    """
    데이터를 JSON 파일에 저장합니다.

    Parameters:
    data (dict): 저장할 데이터
    filename (str): 저장할 파일 이름
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# BoundingBox 정의
bounding_boxes = [
    [[31.0, 121.8], [34.5, 129.3]],   # 제주도
    [[28.0, 122.0], [31.0, 130.0]],   # 동중국해(제주도 아래)
    [[34.5, 120.1], [35.8, 126.2]],   # 황해 1
    [[35.8, 121.1], [36.8, 126.5]],   # 황해 2
    [[37.3, 128.8], [41.5, 138.5]],   # 동해 아래 1
    [[35.4, 130.5], [41.5, 135.5]],   # 동해 아래 2
    [[41.5, 130.2], [42.5, 139.5]],   # 동해 위
    [[33.58, 127.78], [34.84, 130.26]] # 후쿠오카 한국
]

# 각 BoundingBox마다 생성할 점의 수
num_points_per_box = 50

# 랜덤 좌표 생성
coordinates = generate_random_coordinates(bounding_boxes, num_points_per_box)

# 필요한 형식으로 데이터 정리
formatted_data = {}
for i, coord in enumerate(coordinates):
    identifier = str(random.randint(100000000, 999999999))
    formatted_data[identifier] = {
        coord["times"]: {
            "latitude": coord["latitude"],
            "longitude": coord["longitude"],
            "times": coord["times"]
        }
    }

# 데이터를 JSON 파일로 저장
json_filename = "json/random_coordinates.json"
save_to_json(formatted_data, json_filename)
