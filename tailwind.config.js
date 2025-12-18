/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{njk,md,html}", "./_site/**/*.html"],

  theme: {
    extend: {
      colors: {
        primary: {
          500: "#fe53e3",
          600: "#e645c9",
          700: "#c23aaa",
          800: "#9e2f8a",
        },
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
      },
    },
  },

  plugins: [],
};
