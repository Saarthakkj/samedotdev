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
        'secondary': '#f7faf9',
        'tertiary': '#e4e7e6',
        'dark': '#292a2b',
        'gray-light': '#c8c6c3',
        'gray-dark': '#171717',
        'gray-black': '#000002',
        'gray-mid': '#9ea09d',
        'gray-med': '#737271',
        'gray-darker': '#4c4948',
        'olive': '#8f904a',
        'orange': '#f9ae61',
      },
      fontFamily: {
        'sans': ['ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', '"Noto Sans"', 'sans-serif', '"Apple Color Emoji"', '"Segoe UI Emoji"', '"Segoe UI Symbol"', '"Noto Color Emoji"'],
      },
    },
  },
  plugins: [],
}