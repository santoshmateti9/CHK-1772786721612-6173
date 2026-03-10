import { auth } from "./firebase.js";

import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";


async function signupUser() {

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {

    await createUserWithEmailAndPassword(auth, email, password);

    alert("Signup Successful");

    window.location.href = "login.html";

  } catch (error) {

    alert(error.message);

  }
}


// LOGIN FUNCTION
async function loginUser() {

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {

    await signInWithEmailAndPassword(auth, email, password);

    alert("Login Successful");

    window.location.href = "index.html";

  } catch (error) {

    alert("Invalid email or password");

  }
}


// expose functions to HTML
window.signupUser = signupUser;
window.loginUser = loginUser;