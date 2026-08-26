const API = "/api/auth";

let firebaseReady = false;

function setMsg(el, text, type = "") {
  if (!el) return;
  el.textContent = text;
  el.className = "msg " + type;
}

function parseError(data) {
  if (!data) return "Something went wrong";
  if (typeof data.detail === "string") return data.detail;
  if (Array.isArray(data.detail)) return data.detail.join(", ");
  if (data.email) return data.email.join(", ");
  if (data.password) return data.password.join(", ");
  return JSON.stringify(data);
}

function firebaseMessage(err) {
  const code = err && err.code ? err.code : "";
  const messages = {
    "auth/email-already-in-use": "This email is already registered.",
    "auth/invalid-email": "Please enter a valid email address.",
    "auth/weak-password": "Password must be at least 6 characters.",
    "auth/user-not-found": "No account found with this email.",
    "auth/wrong-password": "Wrong email or password.",
    "auth/invalid-credential": "Wrong email or password.",
    "auth/too-many-requests": "Too many attempts. Try again later.",
    "auth/network-request-failed": "Network error. Check your internet connection.",
    "auth/operation-not-allowed": "Email/password sign-in is not enabled in Firebase.",
  };
  return messages[code] || err.message || "Firebase authentication failed.";
}

async function loadFirebase() {
  const res = await fetch(`${API}/firebase-config/`);
  const config = await res.json();
  if (!config.configured || !config.apiKey || !config.projectId) {
    throw new Error(
      "Firebase is not configured. Add FIREBASE_API_KEY and FIREBASE_PROJECT_ID to .env."
    );
  }
  if (!window.firebase) {
    throw new Error("Firebase SDK failed to load.");
  }
  if (!firebase.apps.length) {
    firebase.initializeApp({
      apiKey: config.apiKey,
      authDomain: config.authDomain,
      projectId: config.projectId,
      appId: config.appId,
      storageBucket: config.storageBucket,
      messagingSenderId: config.messagingSenderId,
    });
  }
  firebaseReady = true;
}

async function syncDjangoSession(idToken) {
  const res = await fetch(`${API}/firebase/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ idToken }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(parseError(data));
  if (!data.access) throw new Error("Login failed. No token received.");
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh || "");
  return data;
}

async function doLogin() {
  const msg = document.getElementById("login-msg");
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value;

  if (!email || !password) {
    setMsg(msg, "Please enter email and password.", "error");
    return;
  }

  setMsg(msg, "Logging in...", "");

  try {
    await loadFirebase();
    const credential = await firebase.auth().signInWithEmailAndPassword(email, password);
    const idToken = await credential.user.getIdToken();
    await syncDjangoSession(idToken);
    setMsg(msg, "Logged in! Redirecting...", "success");
    window.location.href = "/dashboard/";
  } catch (err) {
    setMsg(msg, firebaseMessage(err), "error");
  }
}

async function doRegister() {
  const msg = document.getElementById("register-msg");
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;

  if (!email || !password) {
    setMsg(msg, "Please enter email and password.", "error");
    return;
  }
  if (password.length < 6) {
    setMsg(msg, "Password must be at least 6 characters.", "error");
    return;
  }

  setMsg(msg, "Creating Firebase account...", "");

  try {
    await loadFirebase();
    const credential = await firebase.auth().createUserWithEmailAndPassword(email, password);
    const idToken = await credential.user.getIdToken();
    await syncDjangoSession(idToken);
    setMsg(msg, "Account created! Redirecting...", "success");
    window.location.href = "/dashboard/";
  } catch (err) {
    setMsg(msg, firebaseMessage(err), "error");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const loginBtn = document.getElementById("login-btn");
  if (loginBtn) {
    loginBtn.addEventListener("click", doLogin);
    document.getElementById("login-form")?.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        doLogin();
      }
    });
  }

  const registerBtn = document.getElementById("register-btn");
  if (registerBtn) {
    registerBtn.addEventListener("click", doRegister);
    document.getElementById("register-form")?.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        doRegister();
      }
    });
  }
});
