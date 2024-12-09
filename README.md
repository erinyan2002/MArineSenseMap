프로젝트 개요
선저폐수 모니터링 시스템은 선박에 부착된 센서를 통해 수집된 데이터를 기반으로, 실시간으로 수질 상태를 모니터링하고 시각적으로 표시하는 플랫폼입니다. 그러나 본 프로젝트에서는 실제 센서 데이터를 대신하여 시뮬레이션 데이터를 생성하여 시스템의 주요 기능을 테스트하고 시연할 수 있도록 설계되었습니다.

시뮬레이션 환경에서는 선박 이동, 수질 상태, 그리고 수질 지수(WQI)를 기반으로 생성된 데이터를 활용하여 지도와 차트를 통해 정보를 제공합니다.


시뮬레이션 기반 데이터 구성
1. AIS 데이터
선박의 실시간 위치 및 ID 데이터를 생성.
위도 및 경도를 무작위로 변동시키며 이동 경로를 시뮬레이션.
2. 수질 데이터
수질 변수(온도, 염도, 탁도)를 무작위로 생성.
수질 지수(WQI)를 기준으로 5단계 등급으로 색상화:
매우 좋음 (파란색): 80~100
좋음 (초록색): 60~79
보통 (노란색): 40~59
나쁨 (주황색): 20~39
매우 나쁨 (빨간색): 0~19
3. 시간 변화 데이터
특정 시간 간격(예: 10초)마다 데이터를 업데이트하며 실시간 모니터링을 시뮬레이션.
주요 기능
1. AIS Stream 데이터 시뮬레이션
선박의 ID, 위치(위도 및 경도)를 실시간으로 생성.
지도 상에 선박의 이동 경로를 표시하여 사용자가 실시간으로 위치를 확인 가능.
2. WQI 기반 색상화
수질 지수를 기반으로 선박의 상태를 시각적으로 구분:
파란색: 매우 좋음
초록색: 좋음
노란색: 보통
주황색: 나쁨
빨간색: 매우 나쁨
3. 경유 선박 리스트
WQI 기준에서 "나쁨" 이하로 평가된 선박을 자동으로 식별하고 리스트업.
해당 선박의 상세 정보를 제공하여 수질 오염 원인을 추적.
4. 수질 데이터 시각화
지도에서 각 선박의 위치와 WQI 상태를 확인.
파이 차트를 통해 전체 선박의 수질 분포를 요약.
5. 상세 측정 정보
온도, 염도, 탁도 등의 데이터를 사용자에게 제공.
6. 측정 현황 분석
시간에 따른 WQI 변화를 차트로 표현하여 경향성을 분석.
시뮬레이션 데이터 생성
Python 스크립트를 활용한 데이터 생성 예제
python
Copy code
import random
import time

def generate_ship_data(num_ships):
    ships = []
    for i in range(num_ships):
        ship = {
            "id": f"SHIP-{i+1}",
            "latitude": random.uniform(30.0, 40.0),
            "longitude": random.uniform(120.0, 130.0),
            "wqi": random.randint(0, 100),
            "temperature": random.uniform(10, 30),
            "salinity": random.uniform(30, 40),
            "turbidity": random.uniform(1, 10)
        }
        ships.append(ship)
    return ships

def simulate_data(ships):
    while True:
        for ship in ships:
            ship["latitude"] += random.uniform(-0.1, 0.1)
            ship["longitude"] += random.uniform(-0.1, 0.1)
            ship["wqi"] = random.randint(0, 100)
            print(f"Ship {ship['id']} | Lat: {ship['latitude']}, Lon: {ship['longitude']}, WQI: {ship['wqi']}")
        time.sleep(5)

ships = generate_ship_data(10)  # 10개의 선박 데이터 생성
simulate_data(ships)
설치 및 실행 방법
요구사항
Node.js >= 16
Python >= 3.9
MongoDB (시뮬레이션 데이터 저장)
GIS 데이터 처리 라이브러리
실행 방법
저장소를 클론합니다.
bash
Copy code
git clone https://github.com/username/repo-name.git
의존성을 설치합니다.
bash
Copy code
pip install -r requirements.txt
npm install
Python 시뮬레이션 스크립트를 실행하여 데이터 생성:
bash
Copy code
python simulate.py
백엔드 서버를 실행합니다.
bash
Copy code
npm run start
브라우저에서 **http://localhost:3000**에 접속하여 시뮬레이션 데이터를 확인합니다.
사용 방법
지도 인터페이스:

각 선박의 아이콘을 클릭하면 상세 데이터를 확인할 수 있습니다.
수질 등급 필터링:

"나쁨" 이하의 선박만 필터링하여 지도에 표시.
데이터 분석 차트:

파이 차트에서 전체 선박의 수질 등급 분포를 확인.
선박별 시간 경과에 따른 WQI 변화를 분석.
오염 의심 선박 추적:

"경유 선박 리스트"에서 오염 원인 추적 가능.
기대 효과
실시간 데이터 모니터링:

시뮬레이션을 통해 시스템의 기능과 성능을 검증 가능.
환경 관리 시뮬레이션:

실제 데이터를 수집하기 전에 시스템을 환경 보호 목적으로 최적화.
확장성 테스트:

다양한 선박 수와 시나리오에서 시스템의 확장성과 성능 검증.
직관적 데이터 시각화:

지도와 차트를 통해 데이터를 이해하기 쉽게 표현.
