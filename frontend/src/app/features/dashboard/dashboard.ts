import { Component, inject } from '@angular/core';
import { AuthState } from '../../core/services/auth/auth-state';
import { Router } from '@angular/router';

@Component({
  imports: [],
  selector: 'app-dashboard',
  styleUrl: './dashboard.css',
  templateUrl: './dashboard.html',
})
export class Dashboard {
  private readonly authState = inject(AuthState);
  private readonly router = inject(Router);

  logout(): void {
    this.authState.logout();
    void this.router.navigate(['/login']);
  }
}
