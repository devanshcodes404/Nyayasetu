/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nyaya: {
          navy: '#0a192f',
          indigo: '#1e293b',
          card: '#0f172a',
          saffron: '#f59e0b',
          saffronDark: '#d97706',
          border: '#334155',
          textMuted: '#94a3b8',
        }
      }
    },
  },
  plugins: [],
}

