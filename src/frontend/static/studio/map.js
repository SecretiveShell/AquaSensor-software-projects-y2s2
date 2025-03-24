var map = L.map("map").setView([53.32, -1.66], 15);

// L.tileLayer(
//   "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
//   {
//     maxZoom: 17,
//     minZoom: 10,
//     attribution:
//       "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
//   }
// ).addTo(map);

function imputeMissingTemperatures(coords) {
  const temps = coords.map((n) =>
    n.sensor_temperature !== undefined ? parseFloat(n.sensor_temperature) : null
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
  const minT = 0,
    maxT = 25;
  const clamped = Math.max(minT, Math.min(maxT, temp));
  const ratio = (clamped - minT) / (maxT - minT);

  // Hue: 240 (blue) to 0 (red)
  const hue = 240 - 240 * ratio;
  const saturation = 100;
  const lightness = 50;

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

function fetchRivers() {
  const bounds = map.getBounds();
  const minLat = bounds.getSouth();
  const minLng = bounds.getWest();
  const maxLat = bounds.getNorth();
  const maxLng = bounds.getEast();
  const mapCenter = map.getCenter();

  var url = `/api/v1/studio/riverpoints?x1=${minLat}&y1=${minLng}&x2=${maxLat}&y2=${maxLng}`;

  const dateStr = datePicker.value;
  if (dateStr && dateStr !== new Date().toISOString().split('T')[0]) {
    url += `&date=${encodeURIComponent(dateStr)}`;
  }  

  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      if (window.riverTempLayerGroup) {
        window.riverTempLayerGroup.clearLayers();
      } else {
        window.riverTempLayerGroup = L.layerGroup().addTo(map);
      }

      data.elements
        .filter((el) => el.type === "way" && Array.isArray(el.geometry))
        .forEach((el) => {
          const coords = imputeMissingTemperatures(el.geometry);

          for (let i = 0; i < coords.length - 1; i++) {
            const nodeA = coords[i];
            const nodeB = coords[i + 1];

            const t1 = nodeA.sensor_temperature_imputed;
            const t2 = nodeB.sensor_temperature_imputed;

            if (t1 !== undefined && t2 !== undefined) {
              const avgTemp = (t1 + t2) / 2;
              const color = tempToColor(avgTemp);
              const midLat = (nodeA.lat + nodeB.lat) / 2;
              const midLon = (nodeA.lon + nodeB.lon) / 2;

              const polyline = L.polyline(
                [
                  [nodeA.lat, nodeA.lon],
                  [nodeB.lat, nodeB.lon],
                ],
                {
                  color: color,
                  weight: 16,
                  opacity: 1,
                }
              );

              window.riverTempLayerGroup.addLayer(polyline);
            }
          }

          // Add markers, hidden by default
          coords.forEach((node) => {
            const lat = node.lat;
            const lon = node.lon;

            if (node.sensor_temperature !== undefined) {
              const temp = parseFloat(node.sensor_temperature);
              const color = tempToColor(temp);

              const circle = L.circleMarker([lat, lon], {
                radius: 12,
                fillColor: color,
                fillOpacity: 0.95,
                color: color,
                weight: 1,
                opacity: 1,
                className: "sensor-hidden", // <-- Custom class
              }).bindPopup(
                `🌡️ Temp: ${temp}°C<br/>🧪 DO: ${
                  node.sensor_dissolved_oxygen || "?"
                }`
              );

              circle.addEventListener("click", () => {
                renderInfoPanel(node.sensor_name, node.sensor_dissolved_oxygen, node.sensor_temperature);
              });

              window.riverTempLayerGroup.addLayer(circle);

              if (node.sensor_id) {
                const marker = L.marker([lat, lon], {
                  title: `Sensor: ${node.sensor_id}`,
                  opacity: 0, // start hidden
                })
                
                marker.bindPopup(
                  `Temperature: ${temp}°C<br/>DO: ${
                    node.sensor_dissolved_oxygen || "?"
                  }`
                );

                marker.addEventListener("click", () => {
                  renderInfoPanel(node.sensor_name, node.sensor_dissolved_oxygen, node.sensor_temperature);
                });

                marker._icon?.classList?.add("sensor-hidden"); // class for control
                window.riverTempLayerGroup.addLayer(marker);
              }
            }
          });
        });
    })
    .catch((err) => console.error("Error fetching riverpoints:", err));
}

// Trigger river heatmap update
map.on("load", fetchRivers);
map.on("moveend", fetchRivers);
