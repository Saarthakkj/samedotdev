/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#fdfeff',
        'secondary': {
          100: '#f9f9f9',
          200: '#262929',
          300: '#0a0b0d',
        },
        'accent': {
          100: '#e6e9e8',
          200: '#aaaba7',
          300: '#cdccca',
        },
        'gray': {
          100: '#868d8f',
          200: '#686868',
          300: '#434341',
        },
        'yellow': {
          100: '#f2af67',
        },
        'green': {
          100: '#928d48',
        },

      },
    },
  },
  plugins: [],
}