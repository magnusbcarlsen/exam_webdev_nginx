/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['../views/*.*', '../routes/*.*'],
	theme: {
		extend: {
			colors: {
				accentCol: '#0271ce',
				secondaryCol: '#232528',
				primaryCol: '#EAF6FF',
			},
		},
	},
	plugins: [],
};
