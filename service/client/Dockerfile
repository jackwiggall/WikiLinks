FROM nginx:stable-alpine

WORKDIR /usr/share/nginx/html

# html
RUN rm -rf /usr/share/nginx/html/*
COPY html /usr/share/nginx/html

# config
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 55533