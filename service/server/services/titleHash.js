const crypto = require('crypto');

// first 8 characters of base64 md5 hash
exports.createTitleHash = function(title) {
  return crypto.createHash('md5').update(title.toUpperCase()).digest('base64').substring(0,8);
};