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
        'primary': '#fefefe',
        'secondary': '#f7faf9',
        'dark': '#272829',
        'darker': '#0d0d0d',
        'accent-1': '#e1e3e3',
        'accent-2': '#c5c0bd',
        'accent-3': '#989a9a',
        'gray-1': '#66645f',
        'gray-2': '#7e7d7c',
        'gray-3': '#434343',
        'orange': '#efa263',
        'olive': '#929250',

      },
      fontFamily: {
        'sans': ['Arial', 'Helvetica', 'sans-serif'], //Example, adjust as needed
      },
      fontSize: {
        'title': ['3rem', { lineHeight: '1.2' }],
        'subtitle': ['1.5rem', { lineHeight: '1.4' }],
        'section-title': ['2rem', { lineHeight: '1.3' }],
        'body': ['1rem', { lineHeight: '1.5' }],
        'footer': ['0.875rem', { lineHeight: '1.6' }],
      },
      fontWeight: {
        'title': 'bold',
        'section-title': 'bold',

      },

    },
  },
  plugins: [],
}