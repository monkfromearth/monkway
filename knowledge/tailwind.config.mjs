/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        mt: {
          bg: '#FAF8F5',
          card: '#FFFFFF',
          border: '#E8E4DF',
          text: '#22212B',
          muted: '#6B6560',
          ink: '#322E45',
          accent: '#C96F5A',
          accentLight: '#FBEEE9',
          rose: '#B0708F',
          roseLight: '#FAF0F5',
          lav: '#7E7FBC',
          lavLight: '#F0F0FB',
          blue: '#5E80C9',
          blueLight: '#EEF3FC',
          green: '#4F9D7B',
          greenLight: '#EFF8F2',
          amber: '#C2873B',
          amberLight: '#FBF3E6',
          locked: '#D1CDC8',
        },
      },
      fontFamily: {
        sans: ['Figtree', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
};
