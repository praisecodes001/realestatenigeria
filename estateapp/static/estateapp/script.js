const thumb_input = document.querySelector("#thumb_input");
const secondary_input = document.querySelector("#secondary_input");
const secondary_input_1 = document.querySelector("#secondary_input_1");
const secondary_input_2 = document.querySelector("#secondary_input_2");
const secondary_input_3 = document.querySelector("#secondary_input_3");
const secondary_input_4 = document.querySelector("#secondary_input_4");
const secondary_input_5 = document.querySelector("#secondary_input_5");
const secondary_input_6 = document.querySelector("#secondary_input_6");
var uploaded_image = "";



thumb_input.addEventListener("change", function(){
       const reader = new FileReader();
       reader.addEventListener("load", () =>{
           uploaded_image = reader.result; 
           document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})` ; 
       })
       reader.readAsDataURL(this.files[0]);
})




secondary_input.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () =>{
        uploaded_image = reader.result; 
        document.querySelector("#display_image-1").style.backgroundImage = `url(${uploaded_image})` ; 
    })
    reader.readAsDataURL(this.files[0]);
})

secondary_input_1.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () =>{
        uploaded_image = reader.result; 
        document.querySelector("#display_image-2").style.backgroundImage = `url(${uploaded_image})` ; 
    })
    reader.readAsDataURL(this.files[0]);
})



secondary_input_2.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () =>{
        uploaded_image = reader.result; 
        document.querySelector("#display_image-3").style.backgroundImage = `url(${uploaded_image})` ; 
    })
    reader.readAsDataURL(this.files[0]);
})

secondary_input_3.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () =>{
        uploaded_image = reader.result; 
        document.querySelector("#display_image-4").style.backgroundImage = `url(${uploaded_image})` ; 
    })
    reader.readAsDataURL(this.files[0]);
})


secondary_input_4.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () =>{
        uploaded_image = reader.result; 
        document.querySelector("#display_image-5").style.backgroundImage = `url(${uploaded_image})` ; 
    })
    reader.readAsDataURL(this.files[0]);
})

secondary_input_5.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () =>{
        uploaded_image = reader.result; 
        document.querySelector("#display_image-6").style.backgroundImage = `url(${uploaded_image})` ; 
    })
    reader.readAsDataURL(this.files[0]);
})

secondary_input_6.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", () =>{
        uploaded_image = reader.result; 
        document.querySelector("#display_image-7").style.backgroundImage = `url(${uploaded_image})` ; 
    })
    reader.readAsDataURL(this.files[0]);
})
