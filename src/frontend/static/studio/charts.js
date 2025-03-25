function getToken() {
  const token = sessionStorage.getItem("AquaSensorToken");
  if (!token) window.location.href = "/login";
  return token;
}

function renderTemperatureChart(containerId, xData, yData, color) {
  const chart = echarts.init(document.getElementById(containerId));
  const title = "Water Temperature";
  chart.setOption({
    title: { text: title, left: "center" },
    xAxis: {
      type: "category",
      data: xData,
      name: "Time",
      boundaryGap: false,
    },
    yAxis: { type: "value", name: "Water Temperature (°C)" },
    dataZoom: [{ type: "inside" }],
    series: [
      {
        data: yData,
        type: "line",
        smooth: true,
        lineStyle: { color },
      },
    ],
  });
}

function renderDOChart(containerId, xData, yData, color) {
  const chart = echarts.init(document.getElementById(containerId));
  const title = "Dissolved Oxygen";
  chart.setOption({
    title: { text: title, left: "center" },
    xAxis: {
      type: "category",
      data: xData,
      name: "Time",
      boundaryGap: false,
    },
    yAxis: { type: "value", name: "Dissolved Oxygen" },
    dataZoom: [{ type: "inside" }],
    series: [
      {
        data: yData,
        type: "line",
        smooth: true,
        lineStyle: { color },
      },
    ],
  });
}

async function fetchAndRenderCharts(sensorId) {
  const selectedDate = new Date(datePicker.value);
  if (isNaN(selectedDate)) {
    console.error("Invalid date selected.");
    return;
  }

  const startDateObj = new Date(selectedDate);
  startDateObj.setDate(startDateObj.getDate() - 1);
  const endDateObj = new Date(selectedDate);
  endDateObj.setDate(endDateObj.getDate() + 1);

  const startDate = startDateObj.toISOString();
  const endDate = endDateObj.toISOString();
  const color = "blue";

  const token = getToken();
  const url = `/api/v1/sensors/${sensorId}/readings?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`;

  try {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        "AquaSensor-Login-Token": token,
      },
    });

    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const { readings } = await response.json();
    if (!Array.isArray(readings)) throw new Error("Invalid readings format.");

    const xData = readings.map(r => new Date(r.datetime).toLocaleString());
    const yData = readings.map(r => r.temperature);
    const smoothedYData = typeof eSmoothing === "function" ? eSmoothing(yData) : yData;

    renderTemperatureChart("right-top", xData, smoothedYData, color);

    const doData = readings.map(r => r.dissolved_oxygen);
    const smoothedDOData = typeof eSmoothing === "function" ? eSmoothing(doData) : doData;
    renderDOChart("right-bottom", xData, smoothedDOData, color);

  } catch (err) {
    console.error("Data fetch/render error:", err);
  }
}
