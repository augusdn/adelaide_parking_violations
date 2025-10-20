import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/adelaide_parking_violations/', // Updated to match your GitHub repo name
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          maps: ['leaflet', 'react-leaflet'],
          charts: ['chart.js', 'react-chartjs-2']
        }
      }
    }
  },
  server: {
    port: 3000,
    open: true
  }
})