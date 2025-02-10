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
			let date="";
			date+=String(now.getDate()).padStart(2, '0')+"-";
			date+=String(now.getMonth() + 1).padStart(2, '0')+"-";
			date+=String(now.getFullYear()).slice(2);
			let r = await fetch("api.php?sensor="+x+"&date="+date);
			let j = await r.json();
			return j;
		}

		async function load(x){
			let res = await call(x);
			if(res.dt===-1){
				alert("bad response");
				return;
			}
			chart.data.labels=res.dt;

			chart.options.scales.x.suggestedMax=moment.min(moment({H:23,m:59}),moment().add(2,'hours'));
			
			chart.data.datasets[0].data=eSmoothing(res.temp);
			chart.data.datasets[1].data=eSmoothing(res.diox);

			//chart.data.datasets[0].data=res.temp;
			//chart.data.datasets[1].data=res.diox;
			chart.update();
		}