import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'; // Import the plugin

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    proxy: {
      '/ws': {
        target: "ws://127.0.0.1:8000/", // backend
        ws: true, // enable WebSocket proxying
        changeOrigin: true,
      }
    }
  },
})
