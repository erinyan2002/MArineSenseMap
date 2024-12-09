var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['12-21 14:20:25','12-23 11:20:25', '12-25 10:50:11', '12-26 19:40:11', '12-27 12:50:00'],
        datasets: [{
            label: '등급',
            data: [1, 3, 2, 5, 4],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 3
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1, // Y축 단위를 1씩 증가
                    color: 'white' // Y축 글자 색상을 흰색으로 설정
                },
                grid: {
                    color: '#c9d0e0' // Y축 선 색상을 설정
                }
            },
            x: {
                ticks: {
                    color: 'white' // X축 글자 색상을 흰색으로 설정
                },
                grid: {
                    color: '#c9d0e0' // X축 선 색상을 설정
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white' // 범례의 글자 색상을 흰색으로 설정
                }
            }
        }
    }
});
