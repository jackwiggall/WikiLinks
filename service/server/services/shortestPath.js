const redis = require('redis');
const { createTitleHash } = require('./titleHash.js');

async function findShortestPath(src, dest, callback) {
  const queryStartTime = Date.now();
  const client = redis.createClient();
  await client.connect();


  var visited = new Map(); // value, parent
  var queue = [];

  const search_src_hash = createTitleHash(src);
  const search_dest_hash = createTitleHash(dest);

  queue.push(search_src_hash)
  
  var focus = search_src_hash;
  while (queue.length > 0) {
    focus = queue.shift();

    var focusNodes = await client.sMembers(focus);
    if (focusNodes.includes(search_dest_hash)) {
      visited.set(search_dest_hash, focus)
      break;
    }
    for (let i=0; i<focusNodes.length; i++) {
      if (!visited.has(focusNodes[i])) {
        queue.push(focusNodes[i]);
        visited.set(focusNodes[i], focus)
      }
    }
  }

  var hashPath = []
  var lastParent = search_dest_hash
  // find path
  hashPath.push(lastParent)
  while (lastParent != search_src_hash) {
    lastParent = visited.get(lastParent)
    hashPath.push(lastParent)
  }

  var path = []
  for (let i=hashPath.length-1; i>=0; i--) {
    const title = await client.hGet("titles", hashPath[i])
    path.push(title)
  }
  await client.disconnect();

  const queryEndTime = Date.now();
  const queryTime = queryEndTime - queryStartTime;

  // return path
  callback(path, queryTime)
}
exports.findShortestPath = findShortestPath;