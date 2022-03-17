const redis = require('redis');
const { createTitleHash } = require('./titleHash.js');
const { pool } = require.main.require('./pool.js');


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


async function poolQuery(query, data=[]) { // await pool.query dont workie
  return new Promise((resolve, reject) => {
    pool.query(query, data, (err, response) => {
      if (err) {
        reject(err)
      } else {
        resolve(response);
      }
    });
  });
}

function get_path(src, dest, src_visited, dest_visited, intersection) {
  // flip(intersection -> src) -> (intersection -> dest)
  console.log(src,dest);
  var path = []
  path.push(intersection)
  var focus = intersection
  while (focus !== src) {
    focus = src_visited.get(focus)
    path.push(focus)
  }

  path.reverse()

  focus = intersection
  while (focus !== dest) {
    focus = dest_visited.get(focus)
    path.push(focus)
  }

  return path
}

function check_intersection(src_visited, dest_visited) {
  // maybe iterate over smallest map
  for (focus of src_visited.keys()) {
    if (dest_visited.has(focus)) {
      return focus
    }
  }
  return undefined
}


async function findShortestPathSql(src, dest, callback) {
  // const val = await pool.query('SELECT title FROM Page LIMIT 10');
  // console.log(val);
  // const val = await poolQuery('SELECT title FROM Page LIMIT 10')
  const queryStartTime = Date.now()
  
  var srcRow = await poolQuery(`SELECT id FROM Page WHERE title=?`, src)
  var destRow = await poolQuery(`SELECT id FROM Page WHERE title=?`, dest)
  const srcId = srcRow[0].id
  const destId = destRow[0].id

  var src_queue = []
  var dest_queue = []
  src_queue.push(srcId)
  dest_queue.push(destId)

  var src_visited = new Map() // [title, parent]
  var dest_visited = new Map()
  src_visited.set(srcId, -1)
  dest_visited.set(destId, -1)

  var intersection = undefined
  while (intersection == undefined && src_queue.length != 0 && dest_queue.length != 0) {
    // forward bfs and backwards bfs *should* be the exact same but just with a few variable changes
    // forward bfs
    const src_focus = src_queue.shift() // pop
    const src_children = await poolQuery(`SELECT dest FROM Link WHERE src=?`, src_focus);
    for (let i=0; i<src_children.length; i++) {
      if (!src_visited.has(src_children[i].dest)) { // not already visited
        src_visited.set(src_children[i].dest, src_focus)
        src_queue.push(src_children[i].dest)
      }
    }

    // backwards bfs
    const dest_focus = dest_queue.shift() // pop
    const dest_children = await poolQuery(`SELECT src FROM Link WHERE dest=?`, dest_focus);
    for (let i=0; i<dest_children.length; i++) {
      if (!dest_visited.has(dest_children[i].src)) { // not already visited
        dest_visited.set(dest_children[i].src, dest_focus)
        dest_queue.push(dest_children[i].src)
      }
    }

    intersection = check_intersection(src_visited, dest_visited)
  }
  
  const queryEndTime = Date.now();
  const queryTime = queryEndTime - queryStartTime;
  if (intersection) {
    const path = get_path(srcId, destId, src_visited, dest_visited, intersection)
    var titlePath = []
    for (let i=0; i<path.length; i++) {
      const title = await poolQuery(`SELECT title FROM Page where id=?`,path[i]);
      titlePath.push((title[0].title).toString())
    }
    callback(titlePath, queryTime)
  } else {
    console.log("no path found");
    callback([],0)
  }



  // return path
}
exports.findShortestPathSql = findShortestPathSql;