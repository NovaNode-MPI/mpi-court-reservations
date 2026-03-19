export const TOKEN_KEY = "access_token";
export const REDIRECT_KEY = "redirect_after_login";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function isAuthenticated() {
  return Boolean(getToken());
}

export function saveRedirectPath(path) {
  localStorage.setItem(REDIRECT_KEY, path);
}

export function getRedirectPath() {
  return localStorage.getItem(REDIRECT_KEY);
}

export function clearRedirectPath() {
  localStorage.removeItem(REDIRECT_KEY);
}

export function redirectToLogin() {
  window.location.href = "/login.html";
}

export function requireAuth() {
  if (!isAuthenticated()) {
    const currentPath =
      window.location.pathname + window.location.search + window.location.hash;

    saveRedirectPath(currentPath);
    redirectToLogin();
  }
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  clearRedirectPath();
  window.location.href = "/login.html";
}