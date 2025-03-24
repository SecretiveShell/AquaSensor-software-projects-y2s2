const container = document.getElementById("right-bottom");

function renderInfoPanel(name, sensor_dissolved_oxygen, sensor_temperature) {
    container.innerHTML = ""; // clean content
    container.innerHTML = `
        <div class="info-panel">
            <div class="info-panel-header">
                <div class="info-panel-header-title">${name}</div>
            </div>
            <div class="info-panel-content">
                <div class="info-panel-content-item">
                    <div class="info-panel-content-item-title">Temperature</div>
                    <div class="info-panel-content-item-value">${sensor_temperature}</div>
                </div>
                <div class="info-panel-content-item">
                    <div class="info-panel-content-item-title">Dissolved Oxygen</div>
                    <div class="info-panel-content-item-value">${sensor_dissolved_oxygen}</div>
                </div>
            </div>
        </div>
    `;
    console.log("drawn info box");
}