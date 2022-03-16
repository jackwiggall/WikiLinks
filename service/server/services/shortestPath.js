const redis = require('redis');
const { createTitleHash } = require('./titleHash.js');
const pool = require.main.require('./pool.js');


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


async function findShortestPathSql(src, dest, callback) {
  const val = await pool.query('SELECT COUNT(title) FROM Page;');
  console.log(val);

  return
  const queryStartTime = Date.now();
  

  /*
  srcId = SELECT id FROM Page WHERE title=src
  destId = SELECT id FROM Page WHERE title=dest

  // links
  SELECT dest FROM Link WHERE src=srdId

  // convert back
  title = SELECT title FROM Page WHERE id=srcId
  */

  var front_queue = []
  var back_queue = []
  
  front_queue.push(srcId)
  back_queue.push(destId)

  var front_visited = Map() // [title, parent]
  var back_visited = Map()

  var found = false;
  var direction = 'forward';
  while (front_queue > 0 && back_queue > 0) {
    if (direction == 'forward') { // src
      var front_focus = front_queue.shift()
      // check if intersec
      if (back_visited.has(front_focus)) {
        break
      }
      front_nodes = [1,2,3,4,5] // sql
      for (let i=0; i<front_nodes.length; i++) { // branch of for each node
        if (!front_visited.has(front_nodes[i])) { // prevent looping
          front_visited.set(front_focus, front_nodes[i])
          front_queue.push(front_nodes[i])
        }
      }

    } else { // backwards  dest
      // when adding to visited put in [parent, title]
      var back_focus = back_queue.shift()
      if (visited.has(back_focus)) {

      }
    }

    direction = (direction == 'backwards') ? 'forward' : 'backwards';
  }

  const queryEndTime = Date.now();
  const queryTime = queryEndTime - queryStartTime;

  // return path
  callback(path, queryTime)
}
exports.findShortestPath = findShortestPath;