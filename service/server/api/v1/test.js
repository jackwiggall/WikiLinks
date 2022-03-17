const express = require('express');
const { findShortestPathSql } = require.main.require('./services/shortestPath');



var router = express.Router();

router.get('/', (req,res) => {
  findShortestPathSql("Death","Greg Davies", (path, queryTime) => {
    console.log(path, queryTime);
  })
  res.status(200).send("test")
});


exports.router = router;
