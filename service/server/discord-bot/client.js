const { Client, Intents } = require('discord.js');
const { TOKEN } = require('./config.js')

const client = new Client({
  intents: [
    Intents.FLAGS.GUILDS,
    Intents.FLAGS.GUILD_MESSAGES
  ]
});

// function which log in the bot
client.login(TOKEN);

exports.client = client