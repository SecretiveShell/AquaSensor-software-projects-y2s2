// static/studio/mobileButtons.js
document.addEventListener("DOMContentLoaded", () => {

  function hideAllPanels() {
    document.getElementById("left-top").style.display = "none";
    document.getElementById("left-bottom").style.display = "none";
    document.getElementById("right-top").style.display = "none";
    document.getElementById("right-bottom").style.display = "none";
  }

  function isMobileViewport() {
    return window.matchMedia('only screen and (max-width: 720px)').matches;
  }

  map.on("click", function (e) {
    if (isMobileViewport()) {
      hideAllPanels();
    }
  });

  // Map of button IDs to action functions
  const buttonActions = {
    "mobile-map-control-button": () => {
      console.log("Map Controls button clicked");
      hideAllPanels();
      const panel = document.getElementById("left-top");
      if (panel) panel.style.display = panel.style.display === "block" ? "none" : "block";
    },
    "mobile-info-button": () => {
      console.log("Info button clicked");
      hideAllPanels();
      const panel = document.getElementById("left-bottom");
      if (panel) panel.style.display = panel.style.display === "block" ? "none" : "block";
    },
    "mobile-temp-button": () => {
      console.log("Temperature button clicked");
      hideAllPanels();
      const panel = document.getElementById("right-top");
      if (panel) panel.style.display = panel.style.display === "block" ? "none" : "block";
    },
    "mobile-oxy-button": () => {
      console.log("Dissolved Oxygen button clicked");
      hideAllPanels();
      const panel = document.getElementById("right-bottom");
      if (panel) panel.style.display = panel.style.display === "block" ? "none" : "block";
    }
  };

  // Attach click handlers
  for (const [id, handler] of Object.entries(buttonActions)) {
    const button = document.getElementById(id);
    if (button) {
      button.addEventListener("click", handler);
    } else {
      console.warn(`Button with ID ${id} not found.`);
    }
  }
});
