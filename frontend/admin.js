import { db } from "./firebase.js";

import {

collection,
getDocs

}

from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";


async function loadLogs(){

const snapshot=await getDocs(collection(db,"threatLogs"));

let logs=document.getElementById("logs");

snapshot.forEach(doc=>{

let li=document.createElement("li");

li.innerText=doc.data().message+" → "+doc.data().risk+"%";

logs.appendChild(li);

});

}

loadLogs();