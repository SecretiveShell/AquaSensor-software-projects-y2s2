var map = L.map("map").setView([53.32, -1.66], 15);

function imputeMissingTemperatures(coords) {
  const temps = coords.map((n) =>
    n.sensor_temperature !== undefined
      ? parseFloat(n.sensor_temperature)
      : null,
  );

  for (let i = 0; i < coords.length; i++) {
    if (temps[i] !== null) continue;

    // Look backward
    let leftIdx = i - 1;
    while (leftIdx >= 0 && temps[leftIdx] === null) leftIdx--;

    // Look forward
    let rightIdx = i + 1;
    while (rightIdx < temps.length && temps[rightIdx] === null) rightIdx++;

    if (leftIdx >= 0 && rightIdx < temps.length) {
      // Interpolate linearly
      const leftTemp = temps[leftIdx];
      const rightTemp = temps[rightIdx];
      const frac = (i - leftIdx) / (rightIdx - leftIdx);
      temps[i] = leftTemp + frac * (rightTemp - leftTemp);
    } else if (leftIdx >= 0) {
      temps[i] = temps[leftIdx];
    } else if (rightIdx < temps.length) {
      temps[i] = temps[rightIdx];
    }
  }

  // Save into the node under a new key
  for (let i = 0; i < coords.length; i++) {
    if (temps[i] !== null) {
      coords[i].sensor_temperature_imputed = temps[i];
    }
  }

  return coords;
}

function tempToColor(temp) {
  const minT = 3,
    maxT = 18;
  const clamped = Math.max(minT, Math.min(maxT, temp));
  const ratio = (clamped - minT) / (maxT - minT);

  // Hue: 240 (blue) to 0 (red)
  const hue = 240 - 240 * ratio;
  const saturation = 100;
  const lightness = 50;

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

async function fetchRivers() {
  try {
    const bounds = map.getBounds();
    const minLat = bounds.getSouth();
    const minLng = bounds.getWest();
    const maxLat = bounds.getNorth();
    const maxLng = bounds.getEast();
    const dateStr = datePicker.value;

    let url = `/api/v1/studio/riverpoints?x1=${minLat}&y1=${minLng}&x2=${maxLat}&y2=${maxLng}`;
    if (dateStr) {
      url += `&date=${encodeURIComponent(dateStr)}`;
    }

    const res = await fetch(url);
    const data = await res.json();

    if (window.riverTempLayerGroup) {
      window.riverTempLayerGroup.clearLayers();
    } else {
      window.riverTempLayerGroup = L.layerGroup().addTo(map);
    }

    for (const el of data.elements) {
      if (el.type !== "way" || !Array.isArray(el.geometry)) continue;

      const coords = imputeMissingTemperatures(el.geometry);

      for (let i = 0; i < coords.length - 1; i++) {
        const nodeA = coords[i];
        const nodeB = coords[i + 1];
        const t1 = nodeA.sensor_temperature_imputed;
        const t2 = nodeB.sensor_temperature_imputed;

        if (t1 !== undefined && t2 !== undefined) {
          const avgTemp = (t1 + t2) / 2;
          const color = tempToColor(avgTemp);

          const polyline = L.polyline(
            [
              [nodeA.lat, nodeA.lon],
              [nodeB.lat, nodeB.lon],
            ],
            {
              color: color,
              weight: 16,
              opacity: 1,
            },
          );

          window.riverTempLayerGroup.addLayer(polyline);
        }
      }

      for (const node of coords) {
        const { lat, lon, sensor_temperature, sensor_dissolved_oxygen, sensor_id, sensor_name } = node;

        if (sensor_temperature !== undefined) {
          const temp = parseFloat(sensor_temperature);
          const color = tempToColor(temp);

          const circle = L.circleMarker([lat, lon], {
            radius: 12,
            fillColor: color,
            fillOpacity: 0.95,
            color: color,
            weight: 1,
            opacity: 1,
            className: "sensor-hidden",
          }).bindPopup(`🌡️ Temp: ${temp}°C<br/>🧪 DO: ${sensor_dissolved_oxygen || "?"}`);

          circle.addEventListener("click", () => {
            observeSensorId(sensor_id);
            fetchAndRenderCharts();
            renderInfoPanel(sensor_name, sensor_dissolved_oxygen, sensor_temperature);
          });

          window.riverTempLayerGroup.addLayer(circle);

          if (sensor_id) {
            const marker = L.marker([lat, lon], {
              title: `Sensor: ${sensor_id}`,
              opacity: 0,
            });

            marker.bindPopup(`Temperature: ${temp}°C<br/>DO: ${sensor_dissolved_oxygen || "?"}`);

            marker.addEventListener("click", () => {
              observeSensorId(sensor_id);
              fetchAndRenderCharts();
              renderInfoPanel(sensor_name, sensor_dissolved_oxygen, sensor_temperature);
            });

            marker._icon?.classList?.add("sensor-hidden");
            window.riverTempLayerGroup.addLayer(marker);
          }
        }
      }
    }
  } catch (err) {
    console.error("Error fetching riverpoints:", err);
  }
}


// Trigger river heatmap update
map.on("load", fetchRivers);
map.on("moveend", fetchRivers);
