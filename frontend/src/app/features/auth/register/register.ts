import { Component, signal, inject } from '@angular/core';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { AuthService } from '../../../core/services/auth/authservice';
import { ToastrService } from '@relynn/ngx-toastr';
import { HttpErrorResponse } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';

const passwordMatch: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const password = control.get('password')?.value;
  const confirmPassword = control.get('confirm_password')?.value;

  if (!confirmPassword) {
    return null;
  }

  return password === confirmPassword ? null : { passwordMismatch: true };
};

@Component({
  imports: [ReactiveFormsModule, RouterLink],
  selector: 'app-register',
  styleUrl: './register.css',
  templateUrl: './register.html',
})
export class Register {
  private readonly authService = inject(AuthService);
  private readonly toastr = inject(ToastrService);
  private readonly route = inject(Router);

  protected readonly isSubmitting = signal(false);
  protected readonly showPassword = signal(false);
  protected readonly showConfirm = signal(false);

  registerForm = new FormGroup(
    {
      full_name: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.maxLength(150)],
      }),
      email: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.email],
      }),
      password: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required, Validators.minLength(8)],
      }),
      confirm_password: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required],
      }),
    },
    { validators: passwordMatch },
  );

  onSubmit(): void {
    console.log('clicked');
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    if (this.isSubmitting()) {
      return;
    }

    this.isSubmitting.set(true);

    const { full_name, email, password } = this.registerForm.getRawValue();

    this.authService.register({ full_name, email, password }).subscribe({
      next: (response) => {
        this.toastr.success(response.message, 'Success');
        this.registerForm.reset();
        this.isSubmitting.set(false);
        this.route.navigate(['/login']);
      },

      error: (error: HttpErrorResponse) => {
        const message =
          error.error?.email?.[0] ??
          error.error?.detail ??
          error.error?.message ??
          'Registration failed.';

        this.toastr.error(message, 'Registraion failed');
        this.isSubmitting.set(false);
      },
    });
  }
}
