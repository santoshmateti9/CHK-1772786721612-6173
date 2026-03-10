import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";

import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";

import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const firebaseConfig = {

    apiKey: "AIzaSyDihZav4hKDBNsgOF94x6X6YTQEwCB8Sus",
    authDomain: "ai-scam-detection.firebaseapp.com",
    databaseURL: "https://ai-scam-detection-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "ai-scam-detection",
    storageBucket: "ai-scam-detection.firebasestorage.app",
    messagingSenderId: "737536303807",
    appId: "1:737536303807:web:0cd38a4bd68d63889bdc0a"

};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export const db = getFirestore(app);