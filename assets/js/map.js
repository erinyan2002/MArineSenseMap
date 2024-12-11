// const firebaseConfig = {
//   apiKey: "AIzaSyC6RM-JOezScoTB-vOWhMSXh7sYPpZKyhg",
//   authDomain: "asia-404305.firebaseapp.com",
//   databaseURL: "https://asia-404305-default-rtdb.firebaseio.com/",
//   projectId: "asia-404305",
//   storageBucket: "asia-404305.appspot.com",
//   messagingSenderId: "838765553299",
//   appId: "1:838765553299:web:fbf45f8afe5a80d8d8cf66",
//   measurementId: "G-SK4K6MNGVD",
// };
const firebaseConfig = {
  apiKey: "AIzaSyAt9PSSY7rAtEZ4s64Pc3YBd2Es8l9csTk",
  authDomain: "erinpython-a6829.firebaseapp.com",
  databaseURL: "https://erinpython-a6829-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "erinpython-a6829",
  storageBucket: "erinpython-a6829.firebasestorage.app",
  messagingSenderId: "592677237013",
  appId: "1:592677237013:web:8d0fc4b354a2ffd0fd791c",
  measurementId: "G-85YVNBYX33"
};
firebase.initializeApp(firebaseConfig);

function fetchGradeDataAndDisplayChart() {
  const dbRef = firebase.database().ref();
  dbRef.once("value", (snapshot) => {
    const data = snapshot.val();
    const gradeCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };

    // 각 Grade의 개수 집계
    for (const id in data) {
      for (const time in data[id]) {
        const grade = data[id][time].Grade;
        if (gradeCounts.hasOwnProperty(grade)) {
          gradeCounts[grade]++;
        }
      }
    }

    const totalCount = Object.values(gradeCounts).reduce(
      (acc, count) => acc + count,
      0
    );

    const totalElement = document.getElementById("totalGradeCount");
    if (totalElement) {
      totalElement.textContent = `총건수: ${totalCount}`;
    }

    // 차트 데이터 준비
    const chartData = {
      labels: Object.keys(gradeCounts),
      datasets: [
        {
          label: "Grade Counts",
          data: Object.values(gradeCounts),
          backgroundColor: ["#41a4ff", "green", "yellow", "orange", "red"],
        },
      ],
    };

    // 원형 차트 생성
    const ctx = document.getElementById("gradeChart").getContext("2d");
    new Chart(ctx, {
      type: "pie",
      data: chartData,
    });
  });
}

// 함수 호출
fetchGradeDataAndDisplayChart();

function fetchAllCoordinates(callback) {
  const coordinates = [];

  console.log("데이터베이스에서 데이터 가져오기를 시작합니다.");

  const dbRef = firebase.database().ref();
  dbRef.on("value", (snapshot) => {
    console.log("데이터베이스에서 데이터를 가져왔습니다.");


    snapshot.forEach((childSnapshot) => {
      const id = childSnapshot.key;
      let maxTimestamp = null;
      let maxTimestampData = null;

      childSnapshot.forEach((timestampSnapshot) => {
        const timestamp = timestampSnapshot.key;
        const data = timestampSnapshot.val();

        console.log(`ID: ${id}, Timestamp: ${timestamp}, Data:`, data);
        if (!maxTimestamp || new Date(timestamp) > new Date(maxTimestamp)) {
          maxTimestamp = timestamp;
          maxTimestampData = {
            tableId: id,
            moveKey: timestamp,
            lat: parseFloat(data.latitude),
            lng: parseFloat(data.longitude),
            oxg: data.dissolved_oxygen,
            ch: data.chlorophyll,
            tn: data.TN,
            tp: data.TP,
            din: data.DIN,
            dip: data.DIP,
            sd: data.SD,
            value: data.Grade,
          };
        }
      });

      if (maxTimestampData) {
        coordinates.push(maxTimestampData);
      }
    });

    if (coordinates.length > 0) {
      console.log("処理されたデータ: ", coordinates);
      callback(coordinates);
    } else {
      console.log("データが見つかりませんでした。");
    }
  });
}


function getBounds(coordinate, zoomLevel) {
  const delta = 5 / Math.pow(2, zoomLevel);

  return {
    north: coordinate.lat + delta,
    south: coordinate.lat - delta,
    east: coordinate.lng + delta,
    west: coordinate.lng - delta,
  };
}

const rectangles = [];
let existingRectangles = [];

function clearRectangles() {
  rectangles.forEach((rectObj) => {
    rectObj.rectangle.setMap(null);
  });
  rectangles.length = 0;
}
// map
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 7,
    center: { lat: 35.9078, lng: 127.7669 },
    mapTypeId: "terrain",
    styles: [
      {
        elementType: "geometry",
        stylers: [
          {
            color: "#f5f5f5",
          },
        ],
      },
      {
        elementType: "labels.icon",
        stylers: [
          {
            visibility: "off",
          },
        ],
      },
      {
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#616161",
          },
        ],
      },
      {
        elementType: "labels.text.stroke",
        stylers: [
          {
            color: "#f5f5f5",
          },
        ],
      },
      {
        featureType: "administrative.land_parcel",
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#bdbdbd",
          },
        ],
      },
      {
        featureType: "poi",
        elementType: "geometry",
        stylers: [
          {
            color: "#eeeeee",
          },
        ],
      },
      {
        featureType: "poi",
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#757575",
          },
        ],
      },
      {
        featureType: "poi.park",
        elementType: "geometry",
        stylers: [
          {
            color: "#e5e5e5",
          },
        ],
      },
      {
        featureType: "poi.park",
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#9e9e9e",
          },
        ],
      },
      {
        featureType: "road",
        elementType: "geometry",
        stylers: [
          {
            color: "#ffffff",
          },
        ],
      },
      {
        featureType: "road.arterial",
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#757575",
          },
        ],
      },
      {
        featureType: "road.highway",
        elementType: "geometry",
        stylers: [
          {
            color: "#dadada",
          },
        ],
      },
      {
        featureType: "road.highway",
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#616161",
          },
        ],
      },
      {
        featureType: "road.local",
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#9e9e9e",
          },
        ],
      },
      {
        featureType: "transit.line",
        elementType: "geometry",
        stylers: [
          {
            color: "#e5e5e5",
          },
        ],
      },
      {
        featureType: "transit.station",
        elementType: "geometry",
        stylers: [
          {
            color: "#eeeeee",
          },
        ],
      },
      {
        featureType: "water",
        elementType: "geometry",
        stylers: [
          {
            color: "#0B2161",
          },
        ],
      },
      {
        featureType: "water",
        elementType: "labels.text.fill",
        stylers: [
          {
            color: "#9e9e9e",
          },
        ],
      },
    ],
    disableDefaultUI: true,
  });
  map.addListener("center_changed", function () {
    currentCenter = map.getCenter();
  });

  function getColorByValue(value) {
    switch (value) {
      case 1:
        return "#41a4ff";
      case 2:
        return "#00bf03";
      case 3:
        return "#ffef00";
      case 4:
        return "#ffa500";
      case 5:
        return "#ff0000";
      default:
        return "#ffffff";
    }
  }

  function attachRectangleClickHandler(rectangle, coordinate) {
    google.maps.event.addListener(rectangle, "click", function () {
      showRectangleInfo(coordinate);
      track(coordinate); /* TODO */
    });
  }


  function calculateDistance(coord1, coord2) {
    const R = 6371; // 지구 반지름 (km)
    const lat1 = (coord1[0] * Math.PI) / 180;
    const lon1 = (coord1[1] * Math.PI) / 180;
    const lat2 = (coord2[0] * Math.PI) / 180;
    const lon2 = (coord2[1] * Math.PI) / 180;

    const dlat = lat2 - lat1;
    const dlon = lon2 - lon1;

    const a =
      Math.sin(dlat / 2) ** 2 +
      Math.cos(lat1) * Math.cos(lat2) * Math.sin(dlon / 2) ** 2;
    const c = 2 * Math.asin(Math.sqrt(a));

    return R * c;
  }


  function showTrackInfo(data) {
    var box = document.querySelector(".widget-content2");
    box.innerHTML = "";
    let htmlContent = "";
    data.forEach((item, index) => {

      const date = new Date(item.timeStr);


      const formattedDate = date.toLocaleString("ko-KR", {
        month: "long",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
      });

      htmlContent += `<p> ${formattedDate},<br>배 이름: ${item.shipId}</p>`;
    });


    box.innerHTML = htmlContent;
  }

  function track(dataa) {
    const dbRef = firebase.database().ref();

    dbRef.once("value", (snapshot) => {
      const data = snapshot.val();
      let grade5Ship = null;
      let grade5Time = null;
      let grade5Coords = null;

      for (let shipId in data) {
        for (let timeStr in data[shipId]) {
          const record = data[shipId][timeStr];
          if (record["Grade"] === 5) {
            grade5Ship = shipId;
            grade5Time = new Date(timeStr);
            grade5Coords = [record["latitude"], record["longitude"]];
            break;
          }
        }
        if (grade5Ship) break;
      }

      // 다른 선박들과의 거리 계산
      let shipDistances = [];
      if (grade5Ship) {
        for (let shipId in data) {
          if (shipId !== grade5Ship) {
            for (let timeStr in data[shipId]) {
              const record = data[shipId][timeStr];
              const recordTime = new Date(timeStr);
              if (recordTime < grade5Time) {
                const coords = [record["latitude"], record["longitude"]];
                const distance = calculateDistance(grade5Coords, coords);
                shipDistances.push({ shipId, coords, distance, timeStr });
              }
            }
          }
        }
      }

      // 거리에 따라 정렬하고 상위 3개 선박 선택
      const closestShips = shipDistances
        .sort((a, b) => a.distance - b.distance)
        .slice(0, 3);
      console.log(closestShips);
      showTrackInfo(closestShips);
    });
  }

  function showRectangleInfo(coordinate) {
    var content2 = document.querySelector(".content2");
    var box = document.querySelector(".widget-content1");

    content2.style.display = "block";
    box.innerHTML = "";

    const dbRef = firebase.database().ref();
    dbRef.once("value", (snapshot) => {
      snapshot.forEach((childSnapshot) => {
        childSnapshot.forEach((timestampSnapshot) => {
          const data = timestampSnapshot.val();

          // timestampSnapshot.key 값을 파싱하여 UTC 시간으로 처리
          var utcTimestamp = new Date(timestampSnapshot.key + "Z");

          // 로컬 시간으로 변환 (toLocaleString 사용)
          var kstTimestamp = utcTimestamp.toLocaleString("ko-KR", {
            timeZone: "Asia/Seoul",
          });

          if (
            parseFloat(data.latitude) === coordinate.lat &&
            parseFloat(data.longitude) === coordinate.lng
          ) {

            box.innerHTML += `<p>시각: ${kstTimestamp}</p>`;
            box.innerHTML += `<p>위도: ${parseFloat(data.latitude).toFixed(
              2
            )}</p>`;
            box.innerHTML += `<p>경도: ${parseFloat(data.longitude).toFixed(
              2
            )}</p>`;
            box.innerHTML += `<p>산소량: ${parseFloat(
              data.dissolved_oxygen
            ).toFixed(2)}</p>`;
            box.innerHTML += `<p>엽록소 수치: ${parseFloat(
              data.chlorophyll
            ).toFixed(2)}</p>`;
            box.innerHTML += `<p>질소 농도: ${parseFloat(data.TN).toFixed(
              2
            )}</p>`;
            box.innerHTML += `<p>인 농도: ${parseFloat(data.TP).toFixed(
              2
            )}</p>`;
            box.innerHTML += `<p>무기질소: ${parseFloat(data.DIN).toFixed(
              2
            )}</p>`;
            box.innerHTML += `<p>무기인: ${parseFloat(data.DIP).toFixed(
              2
            )}</p>`;
            box.innerHTML += `<p>투명도: ${parseFloat(data.SD).toFixed(2)}</p>`;
            box.innerHTML += `<p>오염도 수치: ${data.Grade}</p>`;
          }
        });
      });
    });
  }

  fetchAllCoordinates((coordinates) => {
    clearRectangles();
    coordinates.forEach((coordinate, index) => {
      const rectangle = new google.maps.Rectangle({
        strokeColor: getColorByValue(coordinate.value),
        strokeOpacity: 0,
        strokeWeight: 1,
        fillColor: getColorByValue(coordinate.value),
        fillOpacity: 1,
        map,
        zIndex: coordinate.value,
        bounds: getBounds(coordinate, map.getZoom()),
      });

      rectangles.push({ rectangle: rectangle, coordinate: coordinate });
      attachRectangleClickHandler(rectangle, coordinate);
    });

    google.maps.event.addListener(map, "zoom_changed", function () {
      const currentCenter = map.getCenter();
      rectangles.forEach((rect) => {
        rect.rectangle.setBounds(getBounds(rect.coordinate, map.getZoom()));
      });
      map.setCenter(currentCenter);
    });
  });
}

function fetchCoordinateDataByPosition(coordinate, callback) {
  const foundCoordinate = window.coordinatesData.find(
    (coord) => coord.lat === coordinate.lat && coord.lng === coordinate.lng
  );

  if (foundCoordinate) {
    callback(foundCoordinate);
  } else {
    callback(null);
  }
}

window.coordinatesData = null; 
