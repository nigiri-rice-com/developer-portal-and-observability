/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eafbf5',
          100: '#d0f7e8',
          200: '#a7f0d6',
          300: '#74e3bf',
          400: '#42d1a5',
          500: '#1eb88e',
          600: '#129672',
          700: '#10785d',
          800: '#105f4b',
          900: '#0f4e3f',
        }
      }
    },
  },
  plugins: [],
}
