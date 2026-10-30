import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Token } from '../services/token/token';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const tokenService = inject(Token);
  const accessToken = tokenService.getAccessToken();

  const isAuthEndpoint = req.url.includes('/auth/login/') || req.url.includes('/auth/register/');

  if (!accessToken || isAuthEndpoint) {
    return next(req);
  }

  const authenticatedRequested = req.clone({
    setHeaders: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return next(authenticatedRequested);
};
