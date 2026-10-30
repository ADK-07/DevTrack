import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class Token {
  private readonly accessKey = 'access_token';
  private readonly refreshKey = 'refresh_token';

  saveTokens(access: string, refresh: string): void {
    localStorage.setItem(this.accessKey, access);
    localStorage.setItem(this.refreshKey, refresh);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.accessKey);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.refreshKey);
  }

  clearTokens(): void {
    localStorage.removeItem(this.accessKey);
    localStorage.removeItem(this.refreshKey);
  }
}
