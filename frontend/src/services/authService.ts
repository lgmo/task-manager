import type { LoginResponse } from "@/types/auth";
import api from "@/api/client";

export async function login(): Promise<LoginResponse> {
  const response = await api.post("/accounts/auth/login/");
  return {
    loginUrl: response.data.login_url,
  };
}

export async function checkAuth(): Promise<boolean> {
  try {
    await api.get("/accounts/auth/check/");
    return true;
  } catch {
    return false;
  }
}

export async function refreshTokens(): Promise<void> {
  try {
    await api.post("/accounts/auth/refresh-tokens/");
  } catch (error) {
    console.error("Error refreshing tokens:", error);
    throw error;
  }
}

export async function logout(): Promise<{ logoutUrl: string }> {
  try {
    const response = await api.post("/accounts/auth/logout/");
    return {
      logoutUrl: response.data.logout_url,
    };
  } catch (error) {
    console.error("Error logging out:", error);
    throw error;
  }
}

export async function signUp(
  username: string,
  email: string,
  password: string,
): Promise<void> {
  try {
    await api.post("/accounts/auth/sign-up/", {
      name: username,
      email,
      password,
    });
  } catch (error) {
    console.error("Error signing up:", error);
    throw error;
  }
}

export async function confirmSignUp(
  email: string,
  confirmationCode: string,
): Promise<void> {
  try {
    await api.post("/accounts/auth/confirm-sign-up/", {
      email,
      confirmation_code: confirmationCode,
    });
  } catch (error) {
    console.error("Error confirming sign up:", error);
    throw error;
  }
}
