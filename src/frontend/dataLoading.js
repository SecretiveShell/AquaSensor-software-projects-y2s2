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
  
  dates=res.readings.map(index=>index.datetime);
  DO=eSmoothing(res.readings.map(index=>index.dissolved_oxygen));
  temp=eSmoothing(res.readings.map(index=>index.temperature));
  
  var option = {
	  	tooltip: {
			trigger: 'item',
			axisPointer : { type: 'cross'}
		},
		xAxis : [{
			type: 'category',
			boundaryGap:false,
			data: dates,
			name: x,
			nameGap: 0,
			nameTextStyle: {
				align:'center',
				verticalAlign:'bottom'
			}
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
	  	legend: {
			data: ['Dissolved Oxygen','Temperature']
		},
		series : [
			{
				name:'Dissolved Oxygen',
				type:'line',
				smooth:false,
				data: DO
			},
			{
				name:'Temperature',
				type:'line',
				smooth:false,
				data: temp
			}
		]
	};

  chartvar.setOption(option);
}
