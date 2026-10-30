import { Component, inject, signal } from '@angular/core';
import { AuthService } from '../../../core/services/auth/authservice';
import { ToastrService } from '@relynn/ngx-toastr';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Token } from '../../../core/services/token/token';
import { AuthState } from '../../../core/services/auth/auth-state';

@Component({
  imports: [ReactiveFormsModule, RouterLink],
  selector: 'app-login',
  styleUrl: './login.css',
  templateUrl: './login.html',
})
export class Login {
  private readonly authService = inject(AuthService);
  private readonly toastr = inject(ToastrService);
  private readonly tokenService = inject(Token);
  private readonly authState = inject(AuthState);
  private readonly router = inject(Router);

  protected readonly isSubmitting = signal(false);
  protected readonly showPassword = signal(false);

  loginForm = new FormGroup({
    email: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email],
    }),
    password: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required],
    }),
  });

  onSubmit(): void {
    if (this.loginForm.invalid || this.isSubmitting()) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.isSubmitting.set(true);

    this.authService.login(this.loginForm.getRawValue()).subscribe({
      next: (response) => {
        this.tokenService.saveTokens(response.tokens.access, response.tokens.refresh);
        this.authService.getCurrentUser().subscribe({
          next: (user) => {
            this.authState.setCurrentUser(user);
            this.toastr.success('Login successful!', 'Success');
            this.loginForm.reset();
            this.isSubmitting.set(false);
            this.router.navigate(['/dashboard']);
          },
          error: () => {
            this.tokenService.clearTokens();
            this.authState.logout();
            this.toastr.error('Unable to load your account.', 'Login Failed');
            this.isSubmitting.set(false);
          },
        });
      },
    });
  }

  logout(): void {
    this.authState.logout();
    this.toastr.success('You have been logged out.', 'Success');
  }
}
