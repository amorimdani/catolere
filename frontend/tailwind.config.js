/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sacred: {
          50: '#fcf8f2',
          100: '#f7eee1',
          200: '#efdbc2',
          300: '#e3c29c',
          400: '#d5a472',
          500: '#c7894d',
          600: '#b06f3e',
          700: '#8e5434',
          800: '#75452f',
          900: '#613a29',
        }
      }
    },
  },
  plugins: [],
}
