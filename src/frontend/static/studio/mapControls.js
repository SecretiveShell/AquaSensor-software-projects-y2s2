const tileLayers = {
  "Esri Satellite": L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    {
      attribution: "Tiles © Esri",
    },
  ),
  OpenStreetMap: L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      attribution: "© OpenStreetMap contributors",
    },
  ),
  // "Stadia Dark": L.tileLayer(
  //   "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
  //   {
  //     attribution: "© Stadia Maps, © OpenStreetMap",
  //   },
  // ),
  // "Stadia Smooth": L.tileLayer(
  //   "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png",
  //   {
  //     attribution: "© Stadia Maps, © OpenStreetMap",
  //   },
  // ),
  "CartoDB Light": L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    {
      attribution: "© OpenStreetMap, © CartoDB",
    },
  ),
  "CartoDB Dark": L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    {
      attribution: "© OpenStreetMap, © CartoDB",
    },
  ),
};

// Create the map and set default layer
let currentLayer = tileLayers["Esri Satellite"];
map.addLayer(currentLayer);

// Generate radio buttons dynamically
const controlsDiv = document.getElementById("map-controls");
Object.keys(tileLayers).forEach((name, index) => {
  const id = `layer-${index}`;
  const label = document.createElement("label");
  label.innerHTML = `<input type="radio" name="layer" value="${name}" ${
    index === 0 ? "checked" : ""
  }> ${name}`;
  controlsDiv.appendChild(label);
});

// Handle change events
document.querySelectorAll('input[name="layer"]').forEach((input) => {
  input.addEventListener("change", function () {
    if (this.checked && tileLayers[this.value]) {
      map.removeLayer(currentLayer);
      currentLayer = tileLayers[this.value];
      map.addLayer(currentLayer);
    }
  });
});
