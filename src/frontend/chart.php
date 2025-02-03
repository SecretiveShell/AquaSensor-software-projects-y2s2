<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AquaSensor</title>
  <link
      rel="stylesheet"
      href="css/index.css"
    />
    <link rel="stylesheet" href="css/chart.css"/>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <?php include("includes/header.php")
    ?>
  <!-- Graph 1: Today's River Data -->
  <div class="chart-container">
    <h2>Today's River Data</h2>
    <canvas id="todayChart"></canvas>
  </div>

  <!-- Graph 2: Yesterday's River Data -->
  <div class="chart-container">
    <h2>Yesterday's River Data</h2>
    <canvas id="yesterdayChart"></canvas>
  </div>

  <!-- Graph 3: River Data from the Last 5 Years -->
  <div class="chart-container">
    <h2>River Data from the Last 5 Years</h2>
    <canvas id="fiveYearChart"></canvas>
  </div>

  <script>
    // Sample Data (Replace with your actual data)
    const todayLabels = ["00:00", "06:00", "12:00", "18:00", "24:00"];
    const todayData = [10, 15, 20, 18, 12]; // Example water levels for today

    const yesterdayLabels = ["00:00", "06:00", "12:00", "18:00", "24:00"];
    const yesterdayData = [8, 14, 19, 17, 11]; // Example water levels for yesterday

    const fiveYearLabels = ["2018", "2019", "2020", "2021", "2022", "2023"];
    const fiveYearData = [50, 55, 60, 58, 62, 65]; // Example water levels for the last 5 years

    // Graph 1: Today's River Data
    const todayCtx = document.getElementById('todayChart').getContext('2d');
    new Chart(todayCtx, {
      type: 'line',
      data: {
        labels: todayLabels,
        datasets: [{
          label: 'Water Level (Today)',
          data: todayData,
          borderColor: 'blue',
          fill: false,
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Time'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Water Level'
            }
          }
        }
      }
    });

    // Graph 2: Yesterday's River Data
    const yesterdayCtx = document.getElementById('yesterdayChart').getContext('2d');
    new Chart(yesterdayCtx, {
      type: 'line',
      data: {
        labels: yesterdayLabels,
        datasets: [{
          label: 'Water Level (Yesterday)',
          data: yesterdayData,
          borderColor: 'green',
          fill: false,
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Time'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Water Level'
            }
          }
        }
      }
    });

    // Graph 3: River Data from the Last 5 Years
    const fiveYearCtx = document.getElementById('fiveYearChart').getContext('2d');
    new Chart(fiveYearCtx, {
      type: 'line',
      data: {
        labels: fiveYearLabels,
        datasets: [{
          label: 'Water Level (Last 5 Years)',
          data: fiveYearData,
          borderColor: 'red',
          fill: false,
        }]
      },
      options: {
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Year'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Water Level'
            }
          }
        }
      }
    });
  </script>
</body>
</html>