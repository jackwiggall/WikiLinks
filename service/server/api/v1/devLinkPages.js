const express = require('express');
var router = express.Router();


router.post('/', (req,res) => {
  const src = req.body.src;
  const dest = req.body.dest;

  var response = {
    "message": [
      "set src to '1' for default search between two pages, long wait",
      "set src to '2' for default search between two pages, short wait",
      "set src to '3' for same page exception",
      "set src to '4' for path not found exception, will take long time to responde",
      "set src to '5' for src title not found",
      "set src to '6' for dest title not found",
      "set src to '7' for src or dest fields not set",
      "set src to '8' for database error"
    ]
  };
  var delay = 0;
  var status = 200;
  switch (src) {
    case '1':
      response = {
        success: true,
        queryTime: 12345,
        steps: 7,
        src: {
          title: src,
          url: 'https://wikipedia.com/wiki/'+src
        },
        dest: {
          title: dest,
          url: 'https://wikipedia.com/wiki/'+dest
        },
        path: [
          {
            title: src,
            url: 'https://wikipedia.com/wiki/'+src
          },
          {
            title: 'step-1',
            url: 'https://wikipedia.com/wiki/step-1'
          },
          {
            title: 'step-2',
            url: 'https://wikipedia.com/wiki/step-2'
          },
          {
            title: 'step-3',
            url: 'https://wikipedia.com/wiki/step-3'
          },
          {
            title: 'step-4',
            url: 'https://wikipedia.com/wiki/step-4'
          },
          {
            title: 'step-5',
            url: 'https://wikipedia.com/wiki/step-5'
          },
          {
            title: 'step-6',
            url: 'https://wikipedia.com/wiki/step-6'
          },
          {
            title: dest,
            url: 'https://wikipedia.com/wiki/'+dest
          }
        ]
      };
      delay = 10_000;
      status = 200;
      break;
    case '2':
      response = {
        success: true,
        queryTime: 103,
        steps: 2,
        src: {
          title: src,
          url: 'https://wikipedia.com/wiki/'+src
        },
        dest: {
          title: dest,
          url: 'https://wikipedia.com/wiki/'+dest
        },
        path: [
          {
            title: src,
            url: 'https://wikipedia.com/wiki/'+src
          },
          {
            title: '1',
            url: 'https://wikipedia.com/wiki/1'
          },
          {
            title: dest,
            url: 'https://wikipedia.com/wiki/'+dest
          }
        ]
      };
      delay = 100;
      status = 200;
      break;
    case '3':
      response = {
        success: true,
        queryTime: 0,
        steps: 0,
        src: {
          title: 'same page',
          url: 'https://wikipedia.com/wiki/same_page'
        },
        dest: {
          title: 'same page',
          url: 'https://wikipedia.com/wiki/same_page'
        },
        path: [
          {
            title: 'same page',
            url: 'https://wikipedia.com/wiki/same_page'
          }
        ]
      };
      delay = 400;
      status = 200;
      break;
    case '4':
      response = {
        success: false,
        message: 'path not found / exhausted search',
        data: {
          src: {
            title: 'A really obscure thing',
            url: 'https://wikipedia.com/wiki/A_really_obscure_thing'
          },
          dest: {
            title: 'Another really obscure thing',
            url: 'https://wikipedia.com/wiki/Another_really_obscure_thing'
          }
        }
      };
      delay = 30_000;
      status = 200;
      break;
    case '5':
      response = {
        success: false,
        message: 'wikipedia title not found',
        notFoundField: 'src',
        data: {
          src: 'not an actual wikipedia page',
          dest: 'Love'
        }
      };
      delay = 100;
      status = 400;
      break;
    case '6':
      response = {
        success: false,
        message: 'wikipedia title not found',
        notFoundField: 'dest',
        data: {
          src: 'Love',
          dest: 'not an actual wikipedia page'
        }
      };
      delay = 100;
      status = 400;
      break;
    case '7':
      response = {
        success: false,
        message: 'src or dest fields not specified'
      };
      delay = 0;
      status = 400;
      break;
    case '8':
      response = {
        success: false,
        message: 'Internal database error'
      };
      delay = 1_000;
      status = 500;
      break;
  }

  setTimeout(() => {
    res.status(status).send(response);
  }, delay);
});

exports.router = router;
