const mysql = require('mysql');


var mariadbHost = 'mariadb';
if (process.env.NODE_ENV === 'development')
  mariadbHost = '127.0.0.1';

const pool = mysql.createPool({
  host: mariadbHost,
  database: 'wikilinks',
  user: 'wiki',
  password: 'L1nKz',
  connectionLimit: 5
});


exports.pool = pool;