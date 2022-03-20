const { pool } = require.main.require('./pool.js')


async function findShortestPath(src, dest, callback) {
  //// start query time ////
  const queryStartTime = Date.now()
  
  var expandedNodes = 0;

  // get database ids for titles
  var srcRow = await poolQuery(`SELECT id FROM Page WHERE title=?`, src)
  var destRow = await poolQuery(`SELECT id FROM Page WHERE title=?`, dest)
  const srcId = srcRow[0].id
  const destId = destRow[0].id

  // search queue
  var src_queue = []
  var dest_queue = []
  src_queue.push(srcId)
  dest_queue.push(destId)


  // visited map for backtracking steps to make path
  var src_visited = new Map() // [title, parent]
  var dest_visited = new Map() // [title, parent]
  src_visited.set(srcId, -1)
  dest_visited.set(destId, -1)

  // iterate until intersection found or search exhausted
  var intersection = undefined
  while (intersection == undefined && src_queue.length != 0 && dest_queue.length != 0) {
    expandedNodes+=2 // 2 nodes are expanded each iteration
    // forward bfs and backwards bfs *should* be the exact same but just with a few variable changes
    //// forward bfs ////
    const src_focus = src_queue.shift() // pop
    const src_children = await poolQuery(`SELECT dest FROM Link WHERE src=?`, src_focus); // get child nodes
    for (let i=0; i<src_children.length; i++) {
      if (!src_visited.has(src_children[i].dest)) { // not already visited
        src_visited.set(src_children[i].dest, src_focus)
        src_queue.push(src_children[i].dest)
      }
    }

    //// backwards bfs ////
    const dest_focus = dest_queue.shift() // pop
    const dest_children = await poolQuery(`SELECT src FROM Link WHERE dest=?`, dest_focus); // get child nodes
    for (let i=0; i<dest_children.length; i++) {
      if (!dest_visited.has(dest_children[i].src)) { // not already visited
        dest_visited.set(dest_children[i].src, dest_focus)
        dest_queue.push(dest_children[i].src)
      }
    }

    // check for intersection
    intersection = check_intersection(src_visited, dest_visited)
  }
  var path = [] // return empty path array if no path found
  if (intersection) {
    // remake path from visited nodes
    path = await get_path(srcId, destId, src_visited, dest_visited, intersection)
  }

  //// end query time ////
  const queryEndTime = Date.now()

  const info = {
    expandedNodes: expandedNodes,
    visitedNodes: src_visited.size + dest_visited.size,
    queryTime: queryEndTime - queryStartTime
  }
  // return
  callback(path, info)
}
exports.findShortestPath = findShortestPath

async function isIndexedTitle(title) {
  const row = await poolQuery(`SELECT id FROM Page WHERE title=?`, title)
  if (row.length === 0) {
    return false
  }
  return true
}
exports.isIndexedTitle = isIndexedTitle

// for some strange reason the program will not wait when using 'await pool.query' on a single line
async function poolQuery(query, data=[]) {
  return new Promise((resolve, reject) => {
    pool.query(query, data, (err, response) => {
      if (err) {
        reject(err)
      } else {
        resolve(response)
      }
    })
  })
}

async function get_path(src, dest, src_visited, dest_visited, intersection) {
  // flip(intersection -> src) -> (intersection -> dest)

  var path = []
  // get path from intersection point to the start of the search
  path.push(intersection)
  var focus = intersection
  while (focus !== src) {
    focus = src_visited.get(focus)
    path.push(focus)
  }
  // reverse path so its now from the start of the search to the intersection point
  path.reverse()

  // append to path the path from the intersection point to the end of the search
  focus = intersection
  while (focus !== dest) {
    focus = dest_visited.get(focus)
    path.push(focus)
  }

  // convert the path of node ids to the actual titles of the wikipedia pages
  var titlePath = []
  for (let i=0; i<path.length; i++) {
    const row = await poolQuery(`SELECT title FROM Page where id=?`,path[i])
    titlePath.push((row[0].title).toString())
  }

  return titlePath
}

function check_intersection(src_visited, dest_visited) {
  for (focus of src_visited.keys()) { // for each key of the src_visited map
    if (dest_visited.has(focus)) { // check if it exists in the dest_visited map
      return focus  // return intersection
    }
  }
  // no intersection
  return undefined
}
