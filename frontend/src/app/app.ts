import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthState } from './core/services/auth/auth-state';

@Component({
  imports: [RouterOutlet],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App implements OnInit {
  protected readonly authService = inject(AuthState);

  ngOnInit(): void {
    this.authService.loadCurrentUser();
  }
}
