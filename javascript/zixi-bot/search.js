const axios = require('axios');

const searchWeb = async (query) => {
    try {
        const response = await axios.get('https://api.bing.microsoft.com/v7.0/search', {
            headers: {
                'Ocp-Apim-Subscription-Key': process.env.BING_API_KEY,
            },
            params: { q: query, count: 3 },
        });

        const results = response.data.webPages.value;
        let responseText = "Berikut hasil pencarian:\n\n";

        results.forEach((result, index) => {
            responseText += `${index + 1}. ${result.name}\n${result.url}\n\n`;
        });

        return responseText;
    } catch (error) {
        console.error("Error during web search:", error);
        return "Maaf, aku tidak bisa mencari sekarang. Coba lagi nanti.";
    }
};

module.exports = { searchWeb };
