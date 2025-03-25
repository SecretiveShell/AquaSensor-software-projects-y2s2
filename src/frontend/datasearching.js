/*const apiurl = "";
fetch(apiurl)
    .then(response => response.json())
    .then(data => {
        filtersensor(data, targetcords);
    })
    .catch(error => console.error('error fetching data', error));

    const targetcords = {lat:  lng};

    function filtersensor(sensors, targetcords){
        const filtersensor = sensor.filter(sensors => {
            const sensorLat = sensor.latitude;
            const sensorLng = sensor.longitude;
            
            const distance = Math.sqrt(
                Math.pow(sensorLat - targetcords.lat, 2) +
                Math.pow(sensorlng - targetcords.lng, 2)
            );
            return distance < 0.1;
         });
         console.log('filtered sensors', filtersensor);
         return filtersensor;
    }
*/
let myMap = new Map();
myMap.set("941205/derwent21", 53.35604);
myMap.set("sensor022/derwent13", 53.32952);
myMap.set("sensor044/derwent13-50", 53.330086);

let filteredEntries = Array.from(mymap).filter(([Key, value]) => {
  return value < 50;
});

let filteredMap = new map(filteredEntries);
for (let [key, value] of filteredMap) {
  console.log("${key}: ${value}");
}
