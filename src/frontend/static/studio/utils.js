const slider = document.getElementById("date-slider-input");
const datePicker = document.getElementById("map-date-picker");
const infobox = document.getElementById("left-bottom");
const realtimeCheckbox = document.getElementById("realtime-checkbox");

function getToken() {
  const token = sessionStorage.getItem("AquaSensorToken");
  if (!token) window.location.href = "/login";
  return token;
}

var currentObservedSensorId = null;

function observeSensorId(sensorId) {
  if (currentObservedSensorId === sensorId) return;
  currentObservedSensorId = sensorId;
}

function getObservedSensorId() {
  return currentObservedSensorId;
}

realtimeCheckbox.addEventListener("change", function () {
  setrealtime(realtimeCheckbox.checked);
});

function setrealtime(checked) {
  if (checked) {
    datePicker.value = null;
    slider.value = slider.max;
    fetchAndRenderCharts();
    fetchRivers();

    pollIntervalId = setInterval(() => {
      fetchAndRenderCharts();
      fetchRivers();
    }, 3000);

  } else {
    datePicker.value = Date.now();
    clearInterval(pollIntervalId);
    pollIntervalId = null;
  }
}
