const slider = document.getElementById("date-slider-input");
const datePicker = document.getElementById("map-date-picker");
const infobox = document.getElementById("left-bottom");

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