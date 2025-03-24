const slider = document.getElementById("date-slider-input");
const datePicker = document.getElementById("map-date-picker");

// Get today's date
const today = new Date();

// Calculate base date = 3 months ago
const baseDate = new Date();
baseDate.setMonth(baseDate.getMonth() - 3);

// Ensure base date is valid (handles end-of-month edge cases)
if (baseDate.getDate() !== today.getDate()) {
  // Some months (e.g., Feb) have fewer days, reset to last valid date
  baseDate.setDate(0);
}

// Calculate max number of days between baseDate and today
const diffTime = today - baseDate;
const maxDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

// Configure slider
slider.min = 0;
slider.max = maxDays;
slider.value = maxDays; // Default to today

function updateDatePicker(offsetDays) {
  const newDate = new Date(baseDate);
  newDate.setDate(baseDate.getDate() + parseInt(offsetDays));

  const yyyy = newDate.getFullYear();
  const mm = String(newDate.getMonth() + 1).padStart(2, "0");
  const dd = String(newDate.getDate()).padStart(2, "0");

  datePicker.value = `${yyyy}-${mm}-${dd}`;
}

// Initial update
updateDatePicker(slider.value);

slider.addEventListener("input", (e) => {
  updateDatePicker(e.target.value);
});

// Prevent picking future dates manually
datePicker.max = today.toISOString().split("T")[0];

slider.addEventListener("input", () => {
  console.log("slider moved");
  updateDatePicker(slider.value);
  fetchRivers();
});
