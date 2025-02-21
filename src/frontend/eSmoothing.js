function eSmoothing(x) {
  const n = x.length;

  // Check if first or last elements need replacing
  if (x[0] === 0 || x[0] > 9000 || x[n - 1] === 0 || x[n - 1] > 2048) {
    let sum = 0, count = 0;
    
    x.forEach(val => {
      if (val !== 0 && val < 9000) {
        sum += val;
        count++;
      }
    });

    const avg = sum / count || 0;

    if (x[0] === 0) x[0] = avg;
    if (x[n - 1] === 0) x[n - 1] = avg;
  }

  // Interpolate missing values
  for (let i = 1; i < n; i++) {
    if (x[i] === 0 || x[i] > 9000) {
      let g = 1;
      while (i + g < n && (x[i + g] === 0 || x[i + g] > 2048)) g++; 

      if (i + g < n) {
        let diff = (x[i + g] - x[i - 1]) / (g + 1);
        for (let j = 0; j < g; j++) {
          x[i + j] = x[i + j - 1] + diff;
        }
        i += g - 1; // Skip processed indices
      }
    }
  }

  return x;
}
