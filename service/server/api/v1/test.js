const { findShortestPathSql } = require.main.require('./services/shortestPath');


var router = express.Router();

router.get('/', (req,res) => {
  findShortestPathSql("test","test", (path) => {
    console.log(path);
  })
  res.status(200).send("test")
});


exports.router = router;
