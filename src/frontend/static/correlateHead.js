//daily mean flow
const flowApi = "https://environment.data.gov.uk/hydrology/id/measures/cad502d9-12f9-4449-a1e5-568b9f7d32e6-flow-m-86400-m3s-qualified/readings?";
//daily min level
const levelApi = "https://environment.data.gov.uk/hydrology/id/measures/cad502d9-12f9-4449-a1e5-568b9f7d32e6-level-min-86400-m-qualified/readings?";
const DerwentWidthM = 6;
/*
flow=m3/s
level=m
width=m
l*w/f=s/m

distance=m
s*m/m = s
*/

var warnList={'flowError':false,'levelError':false};

async function getFlow(d){
	let s=d.toISOString().substring(0,10);
	let url=flowApi+"mineq-date="+s+"&maxeq-date="+s;
	let r = await fetch(url);
	let j = await r.json();
	if(j["items"].length==0){
		url=flowApi+"latest";
		r= await fetch(url);
		j= await r.json();
		warnList['flowError']=true;
	}
	return j["items"][0]["value"];
}
async function getLevel(d){
	let s=d.toISOString().substring(0,10);
	let url=levelApi+"mineq-date="+s+"&maxeq-date="+s;
	let r = await fetch(url);
	let j = await r.json();
	if(j["items"].length==0){
		url=levelApi+"latest";
		r= await fetch(url);
		j= await r.json();
		warnList['levelError']=true;
	}
	return j["items"][0]["value"];
}
async function parseWarnings(){
	let warn=document.getElementById("warnings");
	let c=0;
	warn.innerHTML="";
	if(warnList['flowError']){
		warn.innerHTML+="<p><em>Issues retreiving requested flow rate, latest reading used instead</em></p>"
		warnList['flowError']=false;
		c++;
	}
	if(warnList['levelError']){
		warn.innerHTML+="<p><em>Issues retrieving requested river level, latest reading used instead</em></p>"
		warnList['levelError']=false;
		c++;
	}
	return c;
}

async function dataRequest(id,start,till){
	console.log("api/v1/sensors/"+id+"/readings?start_date="+start.toISOString()+"&end_date="+till.toISOString());
	return fetch("api/v1/sensors/"+id+"/readings?start_date="+start.toISOString()+"&end_date="+till.toISOString(),{
		headers: {
			Accept: "appication/json",
			"AquaSensor-Login-Token": window.sessionStorage["AquaSensorToken"]
		}
	});
}
