const express = require('express')
const { findShortestPath, isIndexedTitle } = require.main.require('./services/shortestPath.js')
var router = express.Router()


router.post('/', (req,res) => {
  const src = req.body.src
  const dest = req.body.dest

  if (src && dest) {
    srcTitleUrl = createPageObject(src)
    destTitleUrl = createPageObject(dest)
    checkValidTitle(srcTitleUrl.title, (validSrc) => { // 'src' valid title
      checkValidTitle(destTitleUrl.title, (validDest) => { // 'dest' valid title
        if (validSrc && validDest) { // valid titles
          findShortestPath(srcTitleUrl.title, destTitleUrl.title, (titlePath, info) => {
            if (titlePath.length === 0) {
              res.status(400).send({
                success: false,
                message: 'Search exhausted',
                data: {
                  src: src,
                  dest: dest
                }
              })
            } else {
              const steps = titlePath.length-1;
              var path = []
              for (let i=0; i<titlePath.length; i++) {
                path.push(createPageObject(titlePath[i]))
              }
              res.status(200).send({
                success: true,
                info: info,
                steps: steps,
                src: srcTitleUrl,
                dest: destTitleUrl,
                path: path
              })
            }
          })
        } else {
          res.status(400).send({
            success: false,
            message: 'Wikipedia title not found',
            notFoundField: (!validSrc) ? 'src' : 'dest',
            data: {
              src: src,
              dest: dest
            }
          })
        }
      })
    })
  } else {
    res.status(400).send({
      success: false,
      message: 'Error src or dest not specified'
    })
  }
})

function createPageObject(rawTitle) {
  // https://en.wikipedia.org/wiki/Linux > Linux
  const s = rawTitle.split(/(https?:\/\/)?(en\.)?wikipedia\.(org|com)\/wiki\//)
  var title = s[s.length-1] // last item in split array
  title = title[0].toUpperCase()+title.substr(1,title.length) // capatilize first letter
  
  // title as its stored in the database
  var dbTitle = title.replaceAll('_', ' ') // actual titles not the titles as appearing in url
  dbTitle = dbTitle.replaceAll('%20', ' ') // encoded spa

  // title as a url
  var urlTitle = title.replaceAll(' ','_')
  var url = 'https://en.wikipedia.org/wiki/'+urlTitle

  // return page object
  return {
    title: dbTitle,
    url: url
  }
}

async function checkValidTitle(title, callback) {
  const valid = await isIndexedTitle(title)
  callback(valid);
}

exports.router = router;
