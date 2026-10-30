export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
}

export type UserRole = 'admin' | 'manager' | 'developer';

export interface User {
  id: number;
  full_name: string;
  email: string;
  role: UserRole;
}

export interface RegisterResponse {
  message: string;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  message: string;
  user: User;
  tokens: AuthTokens;
}
