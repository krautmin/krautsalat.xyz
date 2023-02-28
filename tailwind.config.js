/** @type {import('tailwindcss').Config} */
module.exports = {
    mode: 'jit',
    content: [
        './app/templates/*.{html,htm}',
        './app/home/templates/*.{html,htm}',
    ],
    theme: {
        fontFamily: {
            'sans': ['Fira Sans', 'ui-sans-serif', 'system-ui'],
            'mono': ['Fira Code', 'ui-monospace', 'SFMono-Regular'],
        },
        extend: {},
    },
    plugins: [
        require('@tailwindcss/typography'),
        require('@tailwindcss/forms'),
        require('@tailwindcss/aspect-ratio'),
        require('@tailwindcss/line-clamp'),
        require('daisyui')],
}
