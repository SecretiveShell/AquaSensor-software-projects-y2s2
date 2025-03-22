var map = L.map("map").setView([53.3811, -1.4701], 14);

L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
  {
    maxZoom: 19,
    attribution:
      "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
  }
).addTo(map);

function fetchRivers() {
  var bounds = map.getBounds();
  var minLat = bounds.getSouth();
  var minLng = bounds.getWest();
  var maxLat = bounds.getNorth();
  var maxLng = bounds.getEast();

  var overpassURL =
    `/api/v1/studio/riverpoints?x1=${minLat}&y1=${minLng}&x2=${maxLat}&y2=${maxLng}`;

  fetch(overpassURL)
    .then((response) => response.json())
    .then((data) => {
      var riverPoints = [];

      data.elements
        .filter((element) => element.type === "way" && element.geometry)
        .forEach((element) => {
          var coords = element.geometry.map((coord) => [coord.lat, coord.lon]);

          // Add original points
          coords.forEach((point) => riverPoints.push([...point, 0.9]));

          // Interpolate extra points to fill gaps
          for (let i = 0; i < coords.length - 1; i++) {
            let [lat1, lon1] = coords[i];
            let [lat2, lon2] = coords[i + 1];
            let numInterpolatedPoints = Math.ceil(
              L.latLng(lat1, lon1).distanceTo(L.latLng(lat2, lon2)) / 20
            ); // Controls density

            for (let j = 1; j < numInterpolatedPoints; j++) {
              let frac = j / numInterpolatedPoints;
              let latInterp = lat1 + frac * (lat2 - lat1);
              let lonInterp = lon1 + frac * (lon2 - lon1);
              riverPoints.push([latInterp, lonInterp, 0.6]); // Lower intensity for smooth blending
            }
          }
        });

      // Remove previous river heat points if any
      if (window.riverHeatLayer) {
        map.removeLayer(window.riverHeatLayer);
      }

      // Add river heat layer to the existing heatmap
      window.riverHeatLayer = L.heatLayer(riverPoints, {
        radius: 20, // Increased for smoother water effect
        blur: 40,
        maxZoom: 17,
        max: 1.0,
      }).addTo(map);
    })
    .catch((error) => console.error("Error loading river data:", error));
}

// Trigger river heatmap update
map.on("load", fetchRivers);
map.on("moveend", fetchRivers);
