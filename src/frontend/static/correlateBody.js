var logged;
var level;
var timeAB;
var timeBC;
var now=new Date();

var data21;
var data1350;
var data13;

var baseTime21;
var baseTime1350;
var baseTime13;

var chart;

function newDateFetch(){
	now=new Date(document.getElementById("fetchDate").value);
	pullanddraw();
	return
}

async function recalc(){
	await calculateOffsets();
	data21.time=baseTime21.map((value)=>new Date(value).addSeconds(timeAB+timeBC));
	data1350.time=baseTime21.map((value)=>new Date(value).addSeconds(timeBC));
	await draw();
	parseWarnings();

}

async function draw(){
    let t=document.getElementById("temp").checked;
    let o=document.getElementById("oxygen").checked;

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
			    name:"Dissolved Oxygen(ppm)",
			    show:o
		    },
		    {
			    name:"Temperature(°C)",
			    show:t
		    }
	    ],
	    selected:{
		"Dissolved Oxygen(ppm)":o,
		"Temperature(°C)":t
	    },
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
}

async function calculateOffsets(){
	let flowAB,flowBC;
	let distAB,distBC;
	if(document.getElementById("flow").checked){
		flowAB = document.getElementById("flowA").value;
		flowBC = document.getElementById("flowB").value;
	}
	else{
		await getFlow(now).then((value)=>flowBC=flowAB=value);
	}
	if(document.getElementById("dist").checked){
		distAB=document.getElementById("distA").value;
		distBC=document.getElementById("distB").value;
	}
	else{
		//MAKE ENDPOINT FOR DISTANCE SOON
		distAB=5;
		distBC=3;
	}
	if(document.getElementById("levelCheck").checked){
		level=document.getElementById("level").value;
	}
	else{
		await getLevel(now).then((value)=>level=value);
	}
	let smAB=DerwentWidthM*level/flowAB;
	let smBC=DerwentWidthM*level/flowBC;

	timeAB=distAB*smAB;
	timeBC=distBC*smBC;
}


async function pullanddraw(){
  await calculateOffsets();

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

    /* timeoffset math
     * Derwent 21 time:T
     * dist a
     * Derwent 1350 time:T+a
     * dist b
     * Derwent 13 time:T+a+b
     *
     * to allign:
     * 21 time += a+b
     * 1350 time += b
    */

    baseTime21=Array.from(data21["time"]);
    baseTime1350=Array.from(data1350["time"]);
    baseTime13=Array.from(data13["time"]);
    for(let i=0;i<data21["time"].length;i++)data21["time"][i].addSeconds(timeAB+timeBC);
    for(let i=0;i<data1350["time"].length;i++)data1350["time"][i].addSeconds(timeBC);
    
    await draw();
    parseWarnings();
}

await isLoggedIn().then((value)=>logged=value);
if(!logged){
  document.getElementById("warnings").innerHTML+="<p><em>No Authentication, please <a href=\"login?r=/correlate\">login</a> to use this page</em></p>";
  Array.from(document.getElementsByClassName("authrequired")).forEach((arg)=>arg.setAttribute("disabled",""));
}
if(logged){
  chart=echarts.init(document.getElementById("chart-section"));
  document.getElementById("fetchDate").valueAsDate=now;

  await pullanddraw();	

  window.onresize=function(){
    chart.resize();
  }
  let t=Array.from(document.getElementsByClassName("series-control"));
  t[0].onchange=draw;
  t[1].onchange=draw;
  document.getElementById("datesubmit").onclick=newDateFetch;
  document.getElementById("offsubmit").onclick=recalc;
}

