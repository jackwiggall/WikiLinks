const express = require('express');
const redis = require('redis');
const { createTitleHash } = require.main.require('./services/titleHash.js');
const { findShortestPath } = require.main.require('./services/shortestPath.js');
var router = express.Router();


router.post('/', (req,res) => {
  const src = req.body.src;
  const dest = req.body.dest;

  if (src && dest) {
    srcTitleUrl = convertWikiTitleUrl(src);
    destTitleUrl = convertWikiTitleUrl(dest);
    checkValidTitle(srcTitleUrl.title, (validSrc) => {
      checkValidTitle(destTitleUrl.title, (validDest) => {
        if (validSrc && validDest) {
          findShortestPath(srcTitleUrl.title, destTitleUrl.title, (titlePath, queryTime) => {
            const steps = titlePath.length-1;
            var path = [];
            for (let i=0; i<titlePath.length; i++) {
              path.push(convertWikiTitleUrl(titlePath[i]));
            }
            res.status(200).send({
              success: true,
              queryTime: queryTime,
              steps: steps,
              src: srcTitleUrl,
              dest: destTitleUrl,
              path: path
            })
          })
        } else {
          res.status(400).send({
            success: false,
            message: 'wikipedia title not found',
            notFoundField: (!validSrc) ? 'src' : 'dest',
            data: {
              src: src,
              dest: dest
            }
          });
        }
      });
    });
  } else {
    res.status(400).send({
      success: false,
      message: 'Error src or dest not specified'
    });
  }
});

function convertWikiTitleUrl(rawTitle) {
  // https://en.wikipedia.org/wiki/Linux > Linux
  const s = rawTitle.split(/(https?:\/\/)?(en\.)?wikipedia\.(org|com)\/wiki\//)
  var title = s[s.length-1]
  title = title.replaceAll('_', ' ') // actual titles not the titles as appearing in url
  var url = 'https://en.wikipedia.org/wiki/'+title.replaceAll(' ', '_')
  return {
    title: title,
    url: url
  }
}

async function checkValidTitle(title, callback) {
  var client = redis.createClient();
  await client.connect();
  const titleHash = createTitleHash(title);
  const found = await client.hExists('titles', titleHash);
  client.disconnect();
  callback(found);
}

exports.router = router;
