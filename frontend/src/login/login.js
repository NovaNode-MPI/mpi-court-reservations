import { loginUser } from "../services/authService.js";
import { getRedirectPath, clearRedirectPath } from "../services/authGuard.js";

const loginForm = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const loginButton = document.getElementById("loginButton");
const serverMessage = document.getElementById("serverMessage");

const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");

function clearErrors() {
  emailError.textContent = "";
  passwordError.textContent = "";
  serverMessage.textContent = "";
  serverMessage.classList.remove("success");
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validateLoginForm(email, password) {
  let isValid = true;
  clearErrors();

  if (!email.trim()) {
    emailError.textContent = "Email is required.";
    isValid = false;
  } else if (!isValidEmail(email)) {
    emailError.textContent = "Please enter a valid email address.";
    isValid = false;
  }

  if (!password) {
    passwordError.textContent = "Password is required.";
    isValid = false;
  } else if (password.length < 8) {
    passwordError.textContent = "Password must be at least 8 characters.";
    isValid = false;
  }

  return isValid;
}

function setLoadingState(isLoading) {
  loginButton.disabled = isLoading;
  loginButton.textContent = isLoading ? "Logging in..." : "Login";
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value;

  const isValid = validateLoginForm(email, password);
  if (!isValid) {
    return;
  }

  try {
    setLoadingState(true);

    const response = await loginUser({ email, password });

    localStorage.setItem("access_token", response.access_token);

    serverMessage.textContent = "Login successful.";
    serverMessage.classList.add("success");

    const redirectPath = getRedirectPath();

if (redirectPath) {
  clearRedirectPath();
  window.location.href = redirectPath;
} else {
  window.location.href = "/index.html";
}
  } catch (error) {
    serverMessage.textContent = error.message || "Login failed.";
  } finally {
    setLoadingState(false);
  }
});