import { registerUser } from "../services/authService.js";

const registerForm = document.getElementById("registerForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmPassword");
const registerButton = document.getElementById("registerButton");
const serverMessage = document.getElementById("serverMessage");

const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");
const confirmPasswordError = document.getElementById("confirmPasswordError");

function clearErrors() {
  emailError.textContent = "";
  passwordError.textContent = "";
  confirmPasswordError.textContent = "";
  serverMessage.textContent = "";
  serverMessage.classList.remove("success");
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validateRegisterForm(email, password, confirmPassword) {
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

  if (!confirmPassword) {
    confirmPasswordError.textContent = "Please confirm your password.";
    isValid = false;
  } else if (password !== confirmPassword) {
    confirmPasswordError.textContent = "Passwords do not match.";
    isValid = false;
  }

  return isValid;
}

function setLoadingState(isLoading) {
  registerButton.disabled = isLoading;
  registerButton.textContent = isLoading ? "Creating account..." : "Create account";
}

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;

  const isValid = validateRegisterForm(email, password, confirmPassword);
  if (!isValid) {
    return;
  }

  try {
    setLoadingState(true);

    const response = await registerUser({ email, password });

    serverMessage.textContent = `Account created successfully for ${response.email}. Redirecting to login...`;
    serverMessage.classList.add("success");

    registerForm.reset();

    setTimeout(() => {
    window.location.href = "/login.html";
    }, 1200);
  } catch (error) {
    if (error.fieldErrors) {
      if (error.fieldErrors.email) {
        emailError.textContent = error.fieldErrors.email;
      }

      if (error.fieldErrors.password) {
        passwordError.textContent = error.fieldErrors.password;
      }

      if (error.fieldErrors.confirmPassword) {
        confirmPasswordError.textContent = error.fieldErrors.confirmPassword;
      }
    } else {
      serverMessage.textContent = error.message || "Registration failed.";
    }
  } finally {
    setLoadingState(false);
  }
});