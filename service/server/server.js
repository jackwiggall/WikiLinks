const express = require('express');
const compression = require('compression');
const bodyParser = require('body-parser');
const helmet = require('helmet');
const cors = require('cors');

const limits = require('./middleware/rate-limits');

const app = express();
const port = 3000;


// parsing json and form data
app.use(compression());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());

// security
app.use(helmet());

// Cross Origin Resource Sharing
app.use(cors());



app.use(
  '/api/v1/linkPages',
  // limits.customLimit(2,1), // 6 per minute
  require('./api/v1/linkPages').router
);

app.use(
  '/api/v1/devLinkPages',
  require('./api/v1/devLinkPages').router
)


// error handlers
function notFoundError(req, res, next) {
  res.status(404).send({
    error: 'Not found',
    url: req.url,
    method: req.method
  });
}
function clientErrorHandler (err, req, res, next) {
  if (req.xhr) {
    res.status(500).send({ error: 'Something failed!' });
  } else {
    next(err);
  }
}
function errorHandler(err, req, res) {
  res.status(500).send({ error: 'Server error' });
}

app.use(notFoundError);
app.use(clientErrorHandler);
app.use(errorHandler);

// begin server
app.listen(port, () => {
  console.log('Server listening at http://localhost:%s', port);
});
