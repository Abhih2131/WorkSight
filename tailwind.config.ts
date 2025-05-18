import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/@tremor/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f5ff',
          100: '#e6edff',
          200: '#bfd3ff',
          300: '#99b9ff',
          400: '#4d84ff',
          500: '#004fff',
          600: '#0047e6',
          700: '#003bbf',
          800: '#002f99',
          900: '#00267d',
        },
      },
    },
  },
  plugins: [],
}
export default config