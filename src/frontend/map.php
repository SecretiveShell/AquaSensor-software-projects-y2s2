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
    <link rel="stylesheet" href="css/map.css"/>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  
</head>
<body>
    <?php include("includes/header.php")
    ?>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    // Initialize the map
    const map = L.map('map').setView([54.5, -4], 6); // Centered on the UK

    // Add a base map (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Example GeoJSON data for rivers (replace with actual river data)
    const rivers = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            "name": "River Thames"
          },
          "geometry": {
            "type": "LineString",
            "coordinates": [
              [-0.609, 51.499], // Example coordinates (replace with actual river path)
              [-0.609, 51.498],
              [-0.608, 51.497]
            ]
          }
        },
        {
          "type": "Feature",
          "properties": {
            "name": "River Severn"
          },
          "geometry": {
            "type": "LineString",
            "coordinates": [
              [-2.48, 52.50], // Example coordinates (replace with actual river path)
              [-2.48, 52.49],
              [-2.47, 52.48]
            ]
          }
        }
        // Add more rivers here
      ]
    };

    // Add rivers to the map
    L.geoJSON(rivers, {
      style: {
        color: 'blue', // River color
        weight: 15 // River line thickness
      },
      onEachFeature: function (feature, layer) {
        layer.bindPopup(feature.properties.name); // Show river name on click
      }
    }).addTo(map);
  </script>
  <?php include("includes/footer.php")?>
</body>
</html>