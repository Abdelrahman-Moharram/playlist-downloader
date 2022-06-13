var vquality=document.getElementById("v-quality");function fixText(){var a=document.getElementById("v-quality-input");""===a.value?(a.classList.remove("fw-bold"),a.classList.add("t-muted")):(a.classList.add("fw-bold"),a.classList.remove("t-muted"))}function toggleQOptions(){var b=document.getElementById("vs-option2"),a=document.getElementById("v-quality");b.checked?(a.classList.add("v-hidden"),a.classList.remove("v-visible"),a.value="",a.required=!1):(a.classList.add("v-visible"),a.classList.remove("v-hidden"),a.required=!0)}""===vquality.value?(vquality.classList.remove("fw-bold"),vquality.classList.add("t-muted")):(vquality.classList.add("fw-bold"),vquality.classList.remove("t-muted"))


function hideToast(notifyId){
	var notify = document.getElementById(notifyId).classList.add("hidetoast");
}

function preview() {
	document.getElementById("frame").src = URL.createObjectURL(event.target.files[0]);
}
function clearImage() {
	document.getElementById('formFile').value = null;
	frame.src = "";
}