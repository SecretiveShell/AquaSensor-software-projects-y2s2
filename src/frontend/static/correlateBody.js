var logged;
var level;
var flow;
var now=new Date();

var data21;
var data1350;
var data13;

var baseTime21;
var baseTime1350;
var baseTime13;

function newDateFetch(){
	now=new Date(document.getElementById("fetchDate").value);
	pullanddraw();

	return
}

async function pullanddraw(){
  await getLevel(now).then((value)=>level=value);
  await getFlow(now).then((value)=>flow=value);
  
  var sm=DerwentWidthM*level/flow;
  
  //temporary values until I make the distance endpoint
  //distance end point will probably be added post merge, as to avoid conflicts
  var d1=5;
  var d2=3;

  let timeoff1=d1*sm;
  let timeoff2=d2*sm;

  let start=new Date(now);
  start.setDate(now.getDate()-1);
  start.setHours(22,50,0);
  let till=new Date(now);
  till.setDate(now.getDate()+1);
  till.setHours(1,10,0);
    
  data21={'time':[],'temperature':[],'dissolved_oxygen':[]};
  data1350={'time':[],'temperature':[],'dissolved_oxygen':[]};
  data13={'time':[],'temperature':[],'dissolved_oxygen':[]};
  let r21 = dataRequest("941205",start,till); 
  let r1350 = dataRequest("sensor044",start,till);
  let r13 = dataRequest("sensor022",start,till);
  await r21.then((value)=>value.json().then((value)=>
		value["readings"].forEach((v)=>
			{
				data21['time'].push(new Date(v.datetime));
				data21['temperature'].push(v.temperature);
				data21['dissolved_oxygen'].push(v.dissolved_oxygen);
			}
		)
  	)
  );
  await r1350.then((value)=>value.json().then((value)=>
      value["readings"].forEach((v)=>
			{
				data1350['time'].push(new Date(v.datetime));
				data1350['temperature'].push(v.temperature);
				data1350['dissolved_oxygen'].push(v.dissolved_oxygen);
			}
		)
  	)
    );
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
    baseTime21=Array.from(data21["time"]);
    baseTime1350=Array.from(data1350["time"]);
    baseTime13=Array.from(data13["time"]);
    for(let i=0;i<data21["time"].length;i++)data21["time"][i].addSeconds(timeoff1+timeoff2);
    for(let i=0;i<data1350["time"].length;i++)data1350["time"][i].addSeconds(timeoff2);
    var chartoptions={
	    calculable:true,
	    tooltip: {
		    trigger: 'axis',
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
		    type:"inside",
		    filterMode: 'weakFilter'
		    }
	    ],
	    legend: {
		    data:[
			    {
				    name:"Dissolved Oxygen(ppm)"
			    },
			    {
				    name:"Temperature(°C)"
			    }
		    ],
		    selectedMode: false
	    },
	    series: [
		{
			name: "Dissolved Oxygen(ppm)",
			data: data21["time"].map((x,index)=>[x,data21["dissolved_oxygen"][index]]),
			smooth:true,
			symbol: "none",
			type: "line",
			lineStyle: {
				normal: {
					type:'solid'
				}
			}
		},
		{
			name: "Temperature(°C)",
			data: data21["time"].map((x,index)=>[x,data21["temperature"][index]]),
			smooth:true,
			symbol: "none",
			type: "line",
			lineStyle: {
				normal: {
					type:'solid'
				}
			}
		},
		{
			name: "Dissolved Oxygen(ppm)",
			data: data1350["time"].map((x,index)=>[x,data1350["dissolved_oxygen"][index]]),
			smooth:true,
			symbol: "none",
			type: "line",
			lineStyle: {
				normal: {
					type:[6,4]
				}
			}
		},
		{
			name: "Temperature(°C)",
			data: data1350["time"].map((x,index)=>[x,data1350["temperature"][index]]),
			smooth:true,
			symbol: "none",
			type: "line",
			lineStyle: {
				normal: {
					type:[6,4]
				}
			}
		},
		{
			name: "Dissolved Oxygen(ppm)",
			data: data13["time"].map((x,index)=>[x,data13["dissolved_oxygen"][index]]),
			smooth:true,
			symbol: "none",
			type: "line",
			lineStyle: {
				normal: {
					type:[4,10]
				}
			}
		},
		{
			name: "Temperature(°C)",
			data: data13["time"].map((x,index)=>[x,data13["temperature"][index]]),
			smooth:true,
			symbol: "none",
			type: "line",
			lineStyle: {
				normal: {
					type:[4,10]
				}
			}
		}
	    ]
    }; 
    chart.setOption(chartoptions);
    console.log(data21["time"][0]);
    console.log(data13["time"][0]);
    parseWarnings();
}

await isLoggedIn().then((value)=>logged=value);
if(!logged){
  document.getElementById("warnings").innerHTML+="<p><em>No Authentication, please <a href=\"login?r=/correlate\">login</a> to use this page</em></p>";
  Array.from(document.getElementsByClassName("authrequired")).forEach((arg)=>arg.setAttribute("disabled",""));
}
if(logged){
  //
  var chart=echarts.init(document.getElementById("chart-section"));

  await pullanddraw();	
  

  window.onresize=function(){
    chart.resize();
  }
  let t=Array.from(document.getElementsByClassName("series-control"));
  t[0].onchange=function(){};
  t[1].onchange=function(){};
  document.getElementById("datesubmit").onclick=newDateFetch;
}

