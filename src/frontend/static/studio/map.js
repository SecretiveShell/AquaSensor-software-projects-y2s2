const map = L.map("map").setView([53.32, -1.66], 15);

function imputeMissingTemperatures(coords) {
  const temps = coords.map((n) =>
    n.sensor_temperature !== undefined ? parseFloat(n.sensor_temperature) : null
  );

  for (let i = 0; i < coords.length; i++) {
    if (temps[i] !== null) continue;

    let left = i - 1;
    while (left >= 0 && temps[left] === null) left--;

    let right = i + 1;
    while (right < temps.length && temps[right] === null) right++;

    if (left >= 0 && right < temps.length) {
      const frac = (i - left) / (right - left);
      temps[i] = temps[left] + frac * (temps[right] - temps[left]);
    } else if (left >= 0) {
      temps[i] = temps[left];
    } else if (right < temps.length) {
      temps[i] = temps[right];
    }
  }

  coords.forEach((n, i) => {
    if (temps[i] !== null) n.sensor_temperature_imputed = temps[i];
  });

  return coords;
}

function tempToColor(temp) {
  const minT = 3,
    maxT = 18;
  const clamped = Math.max(minT, Math.min(maxT, temp));
  const ratio = (clamped - minT) / (maxT - minT);
  const hue = 240 - 240 * ratio;
  return `hsl(${hue}, 100%, 50%)`;
}

function isValidSensor(node) {
  return node.sensor_id && !String(node.sensor_id).startsWith("fake");
}

function createPopupContent(temp, oxygen) {
  return `🌡️ Temp: ${temp}°C<br/>🧪 DO: ${oxygen ?? "?"}`;
}

function createSensorClickHandler(sensor_id, sensor_name, oxygen, temp) {
  return () => {
    observeSensorId(sensor_id);
    fetchAndRenderCharts();
    renderInfoPanel(sensor_name, oxygen, temp);
  };
}

async function fetchRivers() {
  try {
    const { _southWest: sw, _northEast: ne } = map.getBounds();
    const dateStr = datePicker.value;
    let url = `/api/v1/studio/riverpoints?x1=${sw.lat}&y1=${sw.lng}&x2=${ne.lat}&y2=${ne.lng}`;

    const realtime = realtimeCheckbox.checked;

    if (dateStr && !realtime) url += `&date=${encodeURIComponent(dateStr)}`;

    const token = getToken();

    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        "AquaSensor-Login-Token": token,
      },
    });
    const { elements } = await res.json();

    if (window.riverTempLayerGroup) {
      window.riverTempLayerGroup.clearLayers();
    } else {
      window.riverTempLayerGroup = L.layerGroup().addTo(map);
    }

    for (const el of elements) {
      if (el.type !== "way" || !Array.isArray(el.geometry)) continue;

      const coords = imputeMissingTemperatures(el.geometry);

      // Render temperature polylines
      for (let i = 0; i < coords.length - 1; i++) {
        const a = coords[i],
          b = coords[i + 1];
        const t1 = a.sensor_temperature_imputed,
          t2 = b.sensor_temperature_imputed;
        if (t1 !== undefined && t2 !== undefined) {
          const avgTemp = (t1 + t2) / 2;
          const polyline = L.polyline(
            [
              [a.lat, a.lon],
              [b.lat, b.lon],
            ],
            { color: tempToColor(avgTemp), weight: 16, opacity: 1 }
          );
          window.riverTempLayerGroup.addLayer(polyline);
        }
      }

      // Render valid sensors as visible circle markers with black outline
      for (const node of coords) {
        const {
          lat,
          lon,
          sensor_temperature,
          sensor_dissolved_oxygen,
          sensor_id,
          sensor_name,
        } = node;

        if (!isValidSensor(node)) continue;
        if (sensor_temperature === undefined) continue;

        const temp = parseFloat(sensor_temperature);
        const color = tempToColor(temp);
        const popupContent = createPopupContent(temp, sensor_dissolved_oxygen);
        const clickHandler = createSensorClickHandler(
          sensor_id,
          sensor_name,
          sensor_dissolved_oxygen,
          temp
        );

        const circle = L.circleMarker([lat, lon], {
          radius: 12,
          fillColor: color,
          fillOpacity: 0.95,
          color: "black", // black outline
          weight: 2, // stroke thickness
          opacity: 1,
        }).bindPopup(popupContent);

        circle.addEventListener("click", clickHandler);
        window.riverTempLayerGroup.addLayer(circle);
      }
    }
  } catch (err) {
    console.error("Error fetching riverpoints:", err);
  }
}

// Trigger updates
map.on("load", fetchRivers);
map.on("moveend", fetchRivers);

// Initial render
fetchRivers();
