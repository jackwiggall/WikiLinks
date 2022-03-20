const { logMessage } = require('../discord-bot/log-message.js')
const crypto = require('crypto')

const salt = '3e0c58c7-9267-430c-b2bf-4910c28467f4'
var discordLogger = (req, res, next) => {
  next() // dont caus any delay
  const src = req.body.src
  const dest = req.body.dest
  const id = createHeaderId(req.headers)
  message = `${id}: "${src}" - "${dest}"`
  console.log(message); // log to console
  logMessage("`"+message+"`") // log to discord
}

function createHeaderId(headers) {
  if (headers['x-forwarded-for'] && headers['user-agent']) {
    var generator = crypto.createHash('sha1')
    generator.update(headers['x-forwarded-for'])
    generator.update(headers['user-agent'])
    const hash = generator.digest('hex')
    const id = hash.substring(0,6)
    return id
  }
  return '000000'
}
exports.discordLogger = discordLogger;