const today = new Date();
const baseDate = new Date();
baseDate.setMonth(baseDate.getMonth() - 3);
baseDate.setMinutes(0, 0, 0); // normalize to full hour

// Handle end-of-month rollover
if (baseDate.getDate() !== today.getDate()) baseDate.setDate(0);

const diffTime = today - baseDate;
const maxHours = Math.floor(diffTime / (1000 * 60 * 60));

// Slider setup
slider.min = 0;
slider.max = maxHours;
slider.value = maxHours;


function updateDatePicker(offsetHours) {
  const newDate = new Date(baseDate);
  newDate.setHours(baseDate.getHours() + parseInt(offsetHours));

  const yyyy = newDate.getFullYear();
  const mm = String(newDate.getMonth() + 1).padStart(2, "0");
  const dd = String(newDate.getDate()).padStart(2, "0");
  const hh = String(newDate.getHours()).padStart(2, "0");
  const min = "00";

  datePicker.value = `${yyyy}-${mm}-${dd}T${hh}:${min}`;
}

// Initial update
updateDatePicker(slider.value);

// Prevent picking future dates manually
const isoNow = today.toISOString().slice(0, 16); // up to minutes
datePicker.max = isoNow;

let fetchTimeout = null;
const FETCH_DEBOUNCE_MS = 200;

function debounced_updater() {
  if (fetchTimeout) clearTimeout(fetchTimeout);
  fetchTimeout = setTimeout(async () => {
    try {
      Promise.all([fetchRivers(), fetchAndRenderCharts()]);
    } catch (e) {
      console.error("Error during debounced fetch:", e);
    } finally {
      fetchTimeout = null;
    }
  }, FETCH_DEBOUNCE_MS);
}


slider.addEventListener("input", () => {
  updateDatePicker(slider.value);
  debounced_updater();
});

datePicker.addEventListener("input", (e) => {
  const selected = new Date(e.target.value);
  const offset = Math.floor((selected - baseDate) / (1000 * 60 * 60));
  if (offset >= 0 && offset <= maxHours) {
    slider.value = offset;
    debounced_updater();
  }
});
