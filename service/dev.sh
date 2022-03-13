#!/usr/bin/sh
tmux new -c "./server" "npm run dev" ';' split -c "./client" "python2 -m SimpleHTTPServer 8080"
