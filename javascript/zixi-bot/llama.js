const axios = require('axios');

const LLaMA_API_URL = 'http://localhost:5000/completion';

const getResponseFromLLaMA = async (prompt) => {
    try {
        const response = await axios.post(LLaMA_API_URL, {
            prompt,
            max_tokens: 100,
        });

        return response.data.text;
    } catch (error) {
        console.error("Error connecting to LLaMA:", error);
        return "Maaf, aku sedang kesulitan berpikir. Coba lagi nanti!";
    }
};

module.exports = { getResponseFromLLaMA };
