/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    fontFamily: {
      "sans-serif": ["Fira Sans", "ui-serif"],
      "mono": ["Fira Code", "ui-monospace"],
    },
  },
  plugins: [
      require("@tailwindcss/typography"),
      require("@tailwindcss/forms"),
      require("@tailwindcss/aspect-ratio"),
      require('@tailwindcss/line-clamp'),
      require("daisyui"),
  ],
    daisyui: {
    themes: ["dark", "night"],
  },
};