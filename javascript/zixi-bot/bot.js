const { default: makeWASocket, useSingleFileAuthState } = require('@adiwajshing/baileys');
const { searchWeb } = require('./search');
const { getResponseFromLLaMA } = require('./llama');
require('dotenv').config();

const { state, saveState } = useSingleFileAuthState('./auth_info.json');

const sock = makeWASocket({
    auth: state,
    printQRInTerminal: true,
});

sock.ev.on('creds.update', saveState);

sock.ev.on('messages.upsert', async (msg) => {
    const message = msg.messages[0];
    if (!message.key.fromMe && message.message?.conversation) {
        const userMessage = message.message.conversation.toLowerCase();

        if (userMessage.startsWith("cari")) {
            const query = userMessage.replace("cari", "").trim();
            const searchResults = await searchWeb(query);
            await sock.sendMessage(message.key.remoteJid, { text: searchResults });
        } else {
            const llamaResponse = await getResponseFromLLaMA(userMessage);
            await sock.sendMessage(message.key.remoteJid, { text: llamaResponse });
        }
    }
});
