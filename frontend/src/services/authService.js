import { USE_MOCK_API, API_BASE_URL } from "../config.js";

const mockUsers = [
  {
    id: 1,
    email: "existing@example.com",
    password: "password123",
    created_at: new Date().toISOString(),
  },
];
function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
async function mockRegister({ email, password }) {
  await wait(1000);

  const normalizedEmail = email.trim().toLowerCase();
  const existingUser = mockUsers.find(
    (user) => user.email.toLowerCase() === normalizedEmail
  );

  if (!normalizedEmail.includes("@")) {
    throw {
      fieldErrors: {
        email: "Please enter a valid email address",
      },
    };
  }

  if (password.length < 8) {
    throw {
      fieldErrors: {
        password: "Password must be at least 8 characters",
      },
    };
  }

  if (existingUser) {
    throw {
      fieldErrors: {
        email: "Email already registered",
      },
    };
  }

  const newUser = {
    id: mockUsers.length + 1,
    email: normalizedEmail,
    password,
    created_at: new Date().toISOString(),
  };

  mockUsers.push(newUser);

  return {
    id: newUser.id,
    email: newUser.email,
    created_at: newUser.created_at,
  };
}

async function realRegister({ email, password }) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Registration failed");
  }

  return data;
}

async function mockLogin({ email, password }) {
  await wait(1000);

  const normalizedEmail = email.trim().toLowerCase();
  const user = mockUsers.find(
    (item) =>
      item.email.toLowerCase() === normalizedEmail &&
      item.password === password
  );

  if (!user) {
    throw new Error("Invalid credentials");
  }

  return {
    access_token: "mock-access-token-123",
    token_type: "bearer",
  };
}

async function realLogin({ email, password }) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail || "Login failed");
  }

  return data;
}

export async function registerUser(payload) {
  if (USE_MOCK_API) {
    return mockRegister(payload);
  }

  return realRegister(payload);
}

export async function loginUser(payload) {
  if (USE_MOCK_API) {
    return mockLogin(payload);
  }

  return realLogin(payload);
}