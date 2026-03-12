import { defineConfig } from 'astro/config';
import solidJs from '@astrojs/solid-js';
import tailwind from '@astrojs/tailwind';

/** @type {import('shiki').ThemeRegistration} */
const monkwayTheme = {
  name: 'monkway-dark',
  type: 'dark',
  colors: {
    'editor.background': '#1E1B29',
    'editor.foreground': '#E7E4EF',
  },
  tokenColors: [
    { scope: ['keyword', 'storage.type', 'storage.modifier'], settings: { foreground: '#E8A08C', fontStyle: 'bold' } },
    { scope: ['entity.name.type', 'support.type'], settings: { foreground: '#B6A8DC' } },
    { scope: ['entity.name.function', 'support.function'], settings: { foreground: '#93B4F0' } },
    { scope: ['string', 'string.quoted'], settings: { foreground: '#9FD8B0' } },
    { scope: ['constant.numeric'], settings: { foreground: '#93B4F0' } },
    { scope: ['comment', 'punctuation.definition.comment'], settings: { foreground: '#6E6A7A', fontStyle: 'italic' } },
    { scope: ['keyword.operator', 'keyword.operator.assignment', 'keyword.operator.arithmetic'], settings: { foreground: '#D9A6C2' } },
    { scope: ['variable', 'variable.other', 'meta.definition.variable', 'variable.other.readwrite'], settings: { foreground: '#E7E4EF' } },
    { scope: ['punctuation', 'meta.brace'], settings: { foreground: '#A8A2B8' } },
  ],
};

export default defineConfig({
  site: 'https://monkfromearth.github.io',
  base: '/monkway/',
  integrations: [solidJs(), tailwind()],
  output: 'static',
  markdown: {
    shikiConfig: {
      theme: monkwayTheme,
    },
  },
});
