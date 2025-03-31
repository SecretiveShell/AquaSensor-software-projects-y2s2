// static/studio/mobileButtons.js
document.addEventListener("DOMContentLoaded", () => {
  function hideAllPanels() {
    document.getElementById("left-top").style.display = "none";
    document.getElementById("left-bottom").style.display = "none";
    document.getElementById("right-top").style.display = "none";
    document.getElementById("right-bottom").style.display = "none";
  }
  function setupCloseFunctionality() {

    const panels = [
      "left-top", 
      "left-bottom", 
      "right-top", 
      "right-bottom"
    ];
    
    panels.forEach(panelId => {
      const panel = document.getElementById(panelId);
      if (panel) {
        if (!panel.querySelector('.mobile-close-button')) {
          const closeButton = document.createElement('button');
          closeButton.className = 'mobile-close-button';
          closeButton.innerHTML = '×';
          closeButton.addEventListener('click', (e) => {
            e.stopPropagation();
            panel.style.display = 'none';
          });
          panel.appendChild(closeButton);
        }
      }
    });

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.mobile-button') && !e.target.closest('[id$="-top"], [id$="-bottom"]')) {
        hideAllPanels();
      }
    });
  }

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

  setupCloseFunctionality();
});
