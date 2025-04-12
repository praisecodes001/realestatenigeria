const thumb_input = document.querySelector("#thumb_input");
var uploaded_image = "";

thumb_input.addEventListener("change", function(){
       const reader = new FileReader();
       reader.addEventListener("load", () =>{
           uploaded_image = reader.result; 
           document.querySelector("#thumb-image").style.backgroundImage = `url(${uploaded_image})` ; 
       })
       reader.readAsDataURL(this.files[0]);
})




