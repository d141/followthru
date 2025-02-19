/** @type {import('tailwindcss').Config} */
export default {
  content: ["./public/index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#3B82F6", // Blue-500
        secondary: "#6366F1", // Indigo-500
        background: "#F3F4F6", // Gray-100
        border: "#E5E7EB", // Gray-200
        text: "#1F2937" // Gray-900
      }
    }
  },
  plugins: [],
};
