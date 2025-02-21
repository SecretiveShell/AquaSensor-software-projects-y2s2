function eSmoothing(x) {
  if (
    x[0] == 0 ||
    x[0] > 9000 ||
    x[x.length - 1] == 0 ||
    x[x.length - 1] > 9000
  ) {
    let t = 0;
    let n = 0;
    for (a = 0; a < x.length; a++) {
      if (x[a] != 0 && x[a] != NaN && x[a] < 9000) {
        t += Number(x[a]);
        ++n;
      }
    }
    let avg = t / n;
    if (x[0] == 0) x[0] = avg;
    if (x[x.length - 1] == 0) x[x.length - 1] = avg;
  }
  for (i = 1; i < x.length; i++) {
    if (x[i] == 0 || x[i] > 9000) {
      let g = 0;
      while (x[i + g] == 0 || x[i + g] > 9000) ++g;
      let dif = x[i + g] - x[i - 1];
      let d = dif / (g + 1);
      while (x[i] == 0 || x[i] > 9000) {
        x[i] = Number(x[i - 1]) + Number(d);
        ++i;
      }
    }
  }
  return x;
}
