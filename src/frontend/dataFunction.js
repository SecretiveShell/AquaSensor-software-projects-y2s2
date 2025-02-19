function eSmoothing(x){
			if(x[0]==0 || x[0]>9000 || x[x.length-1]==0 || x[x.length-1]>9000){
				let t=0;
				let n=0;
				for(a=0;a<x.length;a++){
					if(x[a]!=0 && x[a]!=NaN && x[a]<9000){
						t+=Number(x[a]);
						++n;
					}
				}
				let avg=t/n;
				if(x[0]==0)x[0]=avg;
				if(x[x.length-1]==0)x[x.length-1]=avg;
			}
			for(i=1;i<x.length;i++){
				if(x[i]==0 || x[i]>9000){
					let g=0;
					while(x[i+g]==0 || x[i+g]>9000)++g;
					let dif=x[i+g]-x[i-1];
					let d=dif/(g+1);
					while(x[i]==0 || x[i]>9000){
						x[i]=Number(x[i-1])+Number(d);
						++i;
					}
				}
			}
			return x;
		}			
		
		async function call(x){
			let now = new Date();
			let date= now.toISOString().substring(0,10);
			let r = await fetch("{{ base_url }}"+"/api/v1/sensors/sensors/"+x+"/readings?start_date="+date+"&end_date="+date);
			let j = await r.json();
			return j;
		}

		async function load(x,chartvar){
			let res = await call(x);
			chartvar.data.labels=res.dt;

			chartvar.options.scales.x.suggestedMax=moment.min(moment({H:23,m:59}),moment().add(2,'hours'));
			console.log(res.temp)	
			chartvar.data.datasets[0].data=eSmoothing(res.temp);
			chartvar.data.datasets[1].data=eSmoothing(res.diox);

			//chart.data.datasets[0].data=res.temp;
			//chart.data.datasets[1].data=res.diox;
			chartvar.update();
		}

