const { client } = require('./client.js')

var logChannel;
function findLogChannel() {
  logChannel = client.channels.cache.find(
    channel => channel.name.toLowerCase() === "logs"
  )
}

if (client.isReady()) { // client already ready
  findLogChannel()
} else {
  client.on('ready', () => { // wait for ready
    findLogChannel()
  });
}

logMessage = (string) => {
  logChannel.send(string)
}

exports.logMessage = logMessage

