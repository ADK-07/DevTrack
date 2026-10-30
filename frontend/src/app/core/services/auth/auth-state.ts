import { computed, inject, Injectable, signal } from '@angular/core';
import { AuthService } from './authservice';
import { Token } from '../token/token';
import { User } from '../../../types/auth';

@Injectable({
  providedIn: 'root',
})
export class AuthState {
  private readonly authService = inject(AuthService);
  private readonly tokenService = inject(Token);

  private readonly currentUserSignal = signal<User | null>(null);
  private readonly loadingSignal = signal(false);

  readonly currentUser = this.currentUserSignal.asReadonly();
  readonly isLoading = this.loadingSignal.asReadonly();

  readonly isAuthenticated = computed(() => this.currentUserSignal() !== null);

  loadCurrentUser(): void {
    const accessToken = this.tokenService.getAccessToken();

    if (!accessToken) {
      this.currentUserSignal.set(null);
      return;
    }

    this.loadingSignal.set(true);

    this.authService.getCurrentUser().subscribe({
      next: (user) => {
        this.currentUserSignal.set(user);
        this.loadingSignal.set(false);
      },
      error: () => {
        this.currentUserSignal.set(null);
        this.tokenService.clearTokens();
        this.loadingSignal.set(false);
      },
    });
  }

  setCurrentUser(user: User): void {
    this.currentUserSignal.set(user);
  }

  logout(): void {
    this.tokenService.clearTokens();
    this.currentUserSignal.set(null);
  }
}
