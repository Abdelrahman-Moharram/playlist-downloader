
var vquality = document.getElementById("v-quality");
if (vquality.value === ""){
	vquality.classList.remove("fw-bold");
	vquality.classList.add("t-muted");
}
else{
	vquality.classList.add("fw-bold");
	vquality.classList.remove("t-muted");
}

function fixText(){
	var vquality = document.getElementById("v-quality");
if (vquality.value === ""){
	vquality.classList.remove("fw-bold");
	vquality.classList.add("t-muted");
}
else{
	vquality.classList.add("fw-bold");
	vquality.classList.remove("t-muted");
}
}

function toggleQOptions(){
	var vs_option = document.getElementById("vs-option2");
	var quality = document.getElementById("v-quality");

	if(vs_option.checked){
		quality.classList.add("d-none");
		quality.classList.remove("d-inline-block");
		quality.value="";
		quality.required = false;
	}
	else{
		quality.classList.add("d-inline-block");
		quality.classList.remove("d-none");
		quality.required = true;
	}
}