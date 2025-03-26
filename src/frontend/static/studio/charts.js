function chartClickHandler(chart) {
  const zr = chart.getZr();

  zr.off("click");

  zr.on("click", function (params) {
    console.log("clicked on graph");
    const pixel = [params.offsetX, params.offsetY];

    const dataCoord = chart.convertFromPixel("grid", pixel);

    const timestamp = dataCoord[0];
    const date = new Date(timestamp);

    console.log("Timestamp:", timestamp);
    console.log("Date:", date.toISOString());

    const formatted = date.toISOString().slice(0, 16);
    datePicker.value = formatted;
    debounced_updater();
  });
}

function renderTemperatureChart(
  containerId,
  xData,
  yData,
  color,
  selectedDate
) {
  const chart = echarts.init(document.getElementById(containerId));
  chart.setOption({
    title: { text: "Water Temperature", left: "center" },
    grid: { left: 50, right: 50, bottom: 60, top: 60 },
    xAxis: {
      type: "time",
      name: "Time (UTC)",
      boundaryGap: false,
    },
    yAxis: { type: "value", name: "Water Temperature (°C)" },
    dataZoom: [{ type: "inside" }],
    series: [
      {
        data: xData.map((time, i) => [time, yData[i]]),
        type: "line",
        smooth: true,
        lineStyle: { color },
        symbol: "none", // <-- Hide data point symbols
        markLine: {
          data: [
            {
              xAxis: selectedDate.toISOString(),
              label: {
                formatter: "Selected Time",
                position: "insideTop",
                color: "red",
              },
            },
          ],
          lineStyle: { type: "dashed", color: "red" },
          symbol: "none",
        },
      },
    ],
  });
  chartClickHandler(chart);
}

function renderDOChart(containerId, xData, yData, color, selectedDate) {
  const chart = echarts.init(document.getElementById(containerId));
  chart.setOption({
    title: { text: "Dissolved Oxygen", left: "center" },
    grid: { left: 50, right: 50, bottom: 60, top: 60 },
    xAxis: {
      type: "time",
      name: "Time (UTC)",
      boundaryGap: false,
    },
    yAxis: { type: "value", name: "Dissolved Oxygen" },
    dataZoom: [{ type: "inside" }],
    series: [
      {
        data: xData.map((time, i) => [time, yData[i]]),
        type: "line",
        smooth: true,
        lineStyle: { color },
        symbol: "none", // <-- Hide data point symbols
        markLine: {
          data: [
            {
              xAxis: selectedDate.toISOString(),
              label: {
                formatter: "Selected Time",
                position: "insideTop",
                color: "red",
              },
            },
          ],
          lineStyle: { type: "dashed", color: "red" },
          symbol: "none",
        },
      },
    ],
  });
  chartClickHandler(chart);
}

async function fetchAndRenderCharts() {
  const sensorId = getObservedSensorId();
  var selectedDate = new Date(datePicker.value);

  const color = "blue";

  const token = getToken();

  var url;

  if (!realtimeCheckbox.checked) {
    if (isNaN(selectedDate)) {
      console.error("Invalid date selected.");
      return;
    }

    const startDateObj = new Date(selectedDate);
    startDateObj.setUTCDate(startDateObj.getUTCDate() - 1);
    const endDateObj = new Date(selectedDate);
    endDateObj.setUTCDate(endDateObj.getUTCDate() + 1);

    const startDate = startDateObj.toISOString();
    const endDate = endDateObj.toISOString();

    url = `/api/v1/sensors/${sensorId}/readings?start_date=${encodeURIComponent(
      startDate
    )}&end_date=${encodeURIComponent(endDate)}`;
  } else {
    url = `/api/v1/sensors/${sensorId}/readings/latest?limit=10`;
    selectedDate = new Date();
  }

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

    const xData = readings.map((r) => new Date(r.datetime));
    const yData = readings.map((r) => r.temperature);
    const smoothedYData =
      typeof eSmoothing === "function" ? eSmoothing(yData) : yData;
    renderTemperatureChart(
      "right-top",
      xData,
      smoothedYData,
      color,
      selectedDate
    );

    const doData = readings.map((r) => r.dissolved_oxygen);
    const smoothedDOData =
      typeof eSmoothing === "function" ? eSmoothing(doData) : doData;
    renderDOChart("right-bottom", xData, smoothedDOData, color, selectedDate);
  } catch (err) {
    console.error("Data fetch/render error:", err);
  }
}
