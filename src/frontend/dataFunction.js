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

async function call(x) {
  let now = new Date();
  let to = now.toISOString().substring(0, 10);
  now.setDate(now.getDate() - (document.getElementById("DateRange").value) + 1);
  let from = now.toISOString().substring(0,10);
  let r = await fetch("{{ base_url }}" + "/api/v1/sensors/sensors/" + x + "/readings?start_date=" + from + "&end_date=" + to,{
	headers: {
		'Accept': 'application/json',
		'AquaSensor-Login-Token':window.sessionStorage["AquaSensorToken"]
	}});
  let j = await r.json();
  return j;
}

async function load(x, chartvar) {
  if(!window.sessionStorage["AquaSensorToken"]){
	  console.log("no auth");
	  //no auth
	  return
  }
  let res = await call(x);
  
  dates=eSmoothing(res.readings.map(index=>index.datetime));
  DO=eSmoothing(res.readings.map(index=>index.dissolved_oxygen));
  temp=eSmoothing(res.readings.map(index=>index.temperature));
  
  var option = {
		xAxis : [{
			type: 'category',
			boundaryGap:false,
			data: dates
		}],
		yAxis : [{
			type: 'value'
		},
		{
			type: 'value'
		}],
	  	dataZoom:[{
			type:'inside'
		}],
		series : [
			{
				name:'DO',
				type:'line',
				smooth:false,
				data: DO
			},
			{
				name:'temp',
				type:'line',
				smooth:false,
				data: temp
			}
		]
	};

  chartvar.setOption(option);
}
