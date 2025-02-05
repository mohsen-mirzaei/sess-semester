// src/analytics.js
import { inject } from '@vercel/analytics';

export function initAnalytics() {
  inject();
}