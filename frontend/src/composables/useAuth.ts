import {
  checkAuth,
  login,
  logout,
  signUp,
  confirmSignUp,
} from "@/services/authService";

export function useAuth() {
  return {
    login: async () => {
      const response = await login();
      return response;
    },

    isAuthenticated: async () => {
      return await checkAuth();
    },

    logout: async (): Promise<{ logoutUrl: string }> => {
      const response = await logout();
      return response;
    },

    signUp: async (username: string, email: string, password: string) => {
      const response = await signUp(username, email, password);
      return response;
    },

    confirmSignUp: async (email: string, confirmationCode: string) => {
      const response = await confirmSignUp(email, confirmationCode);
      return response;
    },
  };
}
