var logged;
await isLoggedIn().then((value)=>logged=value);
if(!logged){
  document.getElementById("warnings").innerHTML+="<p><em>No Authentication, please <a href=\"login?r=/correlate\">login</a> to use this page</em></p>";
  Array.from(document.getElementsByClassName("authrequired")).forEach((arg)=>arg.setAttribute("disabled",""));
}
if(logged){
  //
  var chart=echarts.init(document.getElementById("chart-section"));


  var level;
  var flow;
  let now=new Date();
  await getLevel(now).then((value)=>level=value);
  await getFlow(now).then((value)=>flow=value);
  
  var sm=DerwentWidthM*level/flow;
  
  //temporary values until I make the distance endpoint
  //distance end point will probably be added post merge, as to avoid conflicts
  var d1=5;
  var d2=3;

  let timeoff1=d1*sm;
  let timeoff2=d2*sm;

  let start=new Date();
  start.setDate(now.getDate()-1);
  start.setHours(23,0,0);
  let till=new Date();
  till.setDate(now.getDate()+1);
  till.setHours(1,0,0);
    
  var data21={'time':[],'temperature':[],'dissolved_oxygen':[]};
  var data1350={'time':[],'temperature':[],'dissolved_oxygen':[]};
  var data13={'time':[],'temperature':[],'dissolved_oxygen':[]};
  let r21 = dataRequest("941205",start,till); 
  let r1350 = dataRequest("sensor044",start,till);
  let r13 = dataRequest("sensor022",start,till);
  await r21.then((value)=>value.json().then((value)=>
		value["readings"].forEach((v)=>
			{
				data21['time'].push(new Date(v.datetime).addSeconds(timeoff1+timeoff2));
				data21['temperature'].push(v.temperature);
				data21['dissolved_oxygen'].push(v.dissolved_oxygen);
			}
		)
  	)
  );
    //this can be removed in deployment
    //only needed for data seed from the middleware
    data21['temperature']=eSmoothing(data21['temperature']);
    data21['dissolved_oxygen']=eSmoothing(data21['dissolved_oxygen']);
  await r1350.then((value)=>value.json().then((value)=>
      value["readings"].forEach((v)=>
			{
				data1350['time'].push(new Date(v.datetime).addSeconds(timeoff2));
				data1350['temperature'].push(v.temperature);
				data1350['dissolved_oxygen'].push(v.dissolved_oxygen);
			}
		)
  	)
    );
    //this can be removed in deployment
    //only needed for data seed from the middleware
    data1350['temperature']=eSmoothing(data1350['temperature']);
    data1350['dissolved_oxygen']=eSmoothing(data1350['dissolved_oxygen']);
    await r13.then((value)=>value.json().then((value)=>
		value["readings"].forEach((v)=>
			{
				data13['time'].push(new Date(v.datetime));
				data13['temperature'].push(v.temperature);
				data13['dissolved_oxygen'].push(v.dissolved_oxygen);
			}
		)
    	)
    );
    //this can be removed in deployment
    //only needed for data seed from the middleware
    data13['temperature']=eSmoothing(data13['temperature']);
    data13['dissolved_oxygen']=eSmoothing(data13['dissolved_oxygen']);
    var chartoptions={
	    tooltip: {
		    trigger: 'item',
		    axisPointer:{type:'cross'}
	    },
	    xAxis: [
		{
		type: 'time',
		boundaryGap:false,
		name: "Sensor Readings",
		nameGap: 0,
		nameTextStyle: {
			align:"center",
			verticalAlign:"bottom"
		}
		}
	    ],
	    yAxis: [
		{
			type:"value"
		},
		{
			type:"value"
		},
		{
			type:"value"
		},
		{
			type:"value"
		},
		{
			type:"value"
		},
		{
			type:"value"
		}
	    ],
	    dataZoom: [
		    {
		    type:"inside"
		    }
	    ],
	    legend: {
		    data: ["Dissolved Oxygen","Temperature"]
	    },
	    series: [
		{
			name: "Dissolved Oxygen",
			data: data21["time"].map((x,index)=>[x,data21["dissolved_oxygen"][index]]),
			smooth:false,
			symbol: "none",
			type: "line"
		},
		{
			name: "Temperature",
			data: data21["time"].map((x,index)=>[x,data21["temperature"][index]]),
			smooth:false,
			symbol: "none",
			type: "line"
		},
		{
			name: "Dissolved Oxygen",
			data: data1350["time"].map((x,index)=>[x,data1350["dissolved_oxygen"][index]]),
			smooth:false,
			symbol: "none",
			type: "line"
		},
		{
			name: "Temperature",
			data: data1350["time"].map((x,index)=>[x,data1350["temperature"][index]]),
			smooth:false,
			symbol: "none",
			type: "line"
		},
		{
			name: "Dissolved Oxygen",
			data: data13["time"].map((x,index)=>[x,data13["dissolved_oxygen"][index]]),
			smooth:false,
			symbol: "none",
			type: "line"
		},
		{
			name: "Temperature",
			data: data13["time"].map((x,index)=>[x,data13["temperature"][index]]),
			smooth:false,
			symbol: "none",
			type: "line"
		}
	    ]
    };
    chart.setOption(chartoptions);
}

