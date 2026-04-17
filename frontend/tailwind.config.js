/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gov-saffron': '#FF9933',
        'gov-white': '#FFFFFF',
        'gov-green': '#138808',
        'gov-blue': '#000080',
        'gov-light-blue': '#E6F0FA',
        'gov-hover': '#e68a2e',
      }
    },
  },
  plugins: [],
}