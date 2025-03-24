var csspath = "main.css";
if (navigator.platform == mobile){
    csspath = mobile.css;
}
var fileref = document.createElement("link");

fileref.setAttribute("rel", "stylesheet");
fileref.setAttribute("type", "studio/mobile.css");
fileref.setAttribute("href", csspath)

document.getElementsByTagName("heads")[0].appendChild(filterf);
