import { auth, db } from "./firebase.js";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import {
    doc,
    setDoc
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

const API_URL = "https://chk-1772786721612-6173-2.onrender.com"; // Point to Flask server running locally

// --- AUTH LOGIC ---
const signupBtn = document.getElementById("signupBtn");
if (signupBtn) {
    signupBtn.addEventListener("click", async () => {
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        try {
            await createUserWithEmailAndPassword(auth, email, password);
            alert("Account created");
            window.location = "login.html";
        } catch (error) {
            alert(error.message);
        }
    });
}

const loginBtn = document.getElementById("loginBtn");
if (loginBtn) {
    loginBtn.addEventListener("click", async () => {
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        try {
            await signInWithEmailAndPassword(auth, email, password);
            window.location = "index.html";
        } catch (error) {
            alert("Invalid email or password");
        }
    });
}

window.logout = async function () {
    await signOut(auth);
    window.location = "login.html";
};

onAuthStateChanged(auth, (user) => {
    if (!user && (window.location.pathname.includes("index.html") || window.location.pathname.includes("dashboard.html"))) {
        // Only redirect if on a protected page
        // window.location = "login.html";
    }
});

// --- SCANNER LOGIC ---

// Detect which page we are on and attach listeners
document.addEventListener("DOMContentLoaded", () => {
    const scanBtn = document.getElementById("scanBtn");
    const loading = document.getElementById("loading");

    // SMS Scanner Logic
    if (document.getElementById("smsInput") && scanBtn) {
        scanBtn.addEventListener("click", async () => {
            const msg = document.getElementById("smsInput").value;
            const resultDiv = document.getElementById("smsResult");
            if (!msg) return alert("Please enter SMS text");

            showLoading(true);
            resultDiv.innerHTML = "";
            console.log("SMS Scan initiated for:", msg);
            try {
                const response = await fetch(`${API_URL}/predict/sms`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: msg })
                });
                console.log("Server response status:", response.status);
                const data = await response.json();
                console.log("Prediction data received:", data);
                displayResult(resultDiv, data.prediction, "SMS");
            } catch (error) {
                console.error("Fetch error:", error);
                displayError(resultDiv);
            } finally {
                showLoading(false);
            }
        });
    }

    // Email Scanner Logic
    if (document.getElementById("emailInput") && scanBtn) {
        scanBtn.addEventListener("click", async () => {
            const msg = document.getElementById("emailInput").value;
            const resultDiv = document.getElementById("emailResult");
            if (!msg) return alert("Please enter email text");

            showLoading(true);
            resultDiv.innerHTML = "";
            console.log("Email Scan initiated for:", msg);
            try {
                const response = await fetch(`${API_URL}/predict/email`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: msg })
                });
                console.log("Server response status:", response.status);
                const data = await response.json();
                console.log("Prediction data received:", data);
                displayResult(resultDiv, data.prediction, "Email");
            } catch (error) {
                console.error("Fetch error:", error);
                displayError(resultDiv);
            } finally {
                showLoading(false);
            }
        });
    }

    // URL Scanner Logic
    if (document.getElementById("urlInput") && scanBtn) {
        scanBtn.addEventListener("click", async () => {
            const url = document.getElementById("urlInput").value;
            const resultDiv = document.getElementById("urlResult");
            if (!url) return alert("Please enter a URL");

            showLoading(true);
            resultDiv.innerHTML = "";
            console.log("URL Scan initiated for:", url);
            try {
                const response = await fetch(`${API_URL}/predict/url`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ url: url })
                });
                console.log("Server response status:", response.status);
                const data = await response.json();
                console.log("Prediction data received:", data);
                displayResult(resultDiv, data.prediction, "URL");
            } catch (error) {
                console.error("Fetch error:", error);
                displayError(resultDiv);
            } finally {
                showLoading(false);
            }
        });
    }
});

function showLoading(show) {
    const loading = document.getElementById("loading");
    const scanBtn = document.getElementById("scanBtn");
    if (loading) loading.style.display = show ? "block" : "none";
    if (scanBtn) scanBtn.style.display = show ? "none" : "block";
}

function displayResult(div, prediction, type) {
    div.style.display = "block";
    div.style.padding = "20px";
    div.style.borderRadius = "12px";
    div.style.marginTop = "20px";
    div.style.fontWeight = "bold";

    if (prediction === "spam") {
        div.innerHTML = `⚠ HIGH RISK ${type.toUpperCase()} DETECTED<br><span style="font-weight:normal; font-size:14px;">Our AI has identified patterns common in phishing and scams.</span>`;
        div.style.background = "rgba(255, 0, 0, 0.2)";
        div.style.border = "1px solid red";
        div.style.color = "#ff4444";
    } else {
        div.innerHTML = `✅ ${type} LOOKS SAFE<br><span style="font-weight:normal; font-size:14px;">No immediate phishing patterns were detected by the AI.</span>`;
        div.style.background = "rgba(0, 255, 0, 0.1)";
        div.style.border = "1px solid #00ff00";
        div.style.color = "#00ff00";
    }
}

function displayError(div) {
    div.style.display = "block";
    div.innerHTML = "❌ Error connecting to backend server. Please ensure the Flask app is running.";
    div.style.background = "rgba(255, 165, 0, 0.2)";
    div.style.color = "orange";
    div.style.border = "1px solid orange";

}
