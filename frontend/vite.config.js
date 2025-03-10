import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: "/",
  plugins: [react()],
  preview: {
   port: 8080,
   strictPort: true,
  },
  server: {
   port: 8080,
   strictPort: true,
   host: true,
   origin: "http://0.0.0.0:8080",
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/tests/setup.js', // assuming the test folder is in the root of our project
  },
  coverage: {
    include: ['src/**/*.{js,jsx,ts,tsx}'], // specify files to include
    exclude: ['src/generated/**/*.ts'],    // specify files to exclude
    reporter: ['text', 'html']  // customize reporters. don't forget to include 'html' if you use vitest-ui
  }
 });