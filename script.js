
async function predict(){

let maths=document.getElementById("maths").value
let biology=document.getElementById("biology").value
let commerce=document.getElementById("commerce").value
let coding=document.getElementById("coding").value

let res = await fetch("/predict",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({maths,biology,commerce,coding})
})

let data = await res.json()

document.getElementById("result").innerHTML =
"Best Career: "+data.career+" | Score: "+data.score+"%"
}

async function sendChat(){

let msg=document.getElementById("chatInput").value

let res = await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg})
})

let data = await res.json()

document.getElementById("chatBox").innerHTML += "<p><b>You:</b> "+msg+"</p>"
document.getElementById("chatBox").innerHTML += "<p><b>AI:</b> "+data.reply+"</p>"
}
