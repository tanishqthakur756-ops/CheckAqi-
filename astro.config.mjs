// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://aqi-tracker.example.com',
  vite: {
    plugins: [tailwindcss()],
  },
});
