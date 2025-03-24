document.addEventListener("DOMContentLoaded", function () {
    const chartContainers = document.querySelectorAll(".chart-container");
    
    chartContainers.forEach((container) => {
        container.addEventListener("click", ()  => {
            container.classList.toggle("enlarged");
        });
    });
});