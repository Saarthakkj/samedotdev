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
        'primary': '#fafafa',
        'secondary': '#2a2a29',
        'light-gray': '#ededec',
        'dark': '#141414',
        'accent-light': '#d8d8d7',
        'accent-medium': '#6a6f66',
        'accent-gray': '#a4a5a3',
        'subtle-gray': '#c4bfbc',
        'medium-gray': '#838885',
        'dark-gray': '#494644',
        'highlight-light': '#f3ac6c',
        'highlight-dark': '#c27739',
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'sans-serif'],
        mono: ['var(--font-mono)', 'monospace'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      }
    },
  },
  plugins: [],
}