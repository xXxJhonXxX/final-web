let modal = document.getElementById("myModal");

let btn = document.getElementById("buyModal");

let span = document.getElementsByClassName("close")[0];

btn.onclick = function(){

    let plantName = document.querySelector(".name").innerText;
    let plantPrice = document.querySelector(".price").innerText;

    
    document.getElementById("plant").value = plantName;
    document.getElementById("price").value = plantPrice;

    modal.style.display = "block";
}

span.onclick = function(){
    modal.style.display = "none";
}

window.onclick = function(event){
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


let btn1 = document.getElementById("submitModal");
btn1.onclick = function(){
    alert("Thank You For Buying!")
}