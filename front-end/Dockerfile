# first build stage
FROM node:alpine
WORKDIR /front-end

# get files
COPY public /front-end/public
COPY src /front-end/src
COPY *.json /front-end/

# make the build
RUN ["npm", "ci"]
RUN ["npm", "run", "build"]

# next docker stage
FROM nginx:alpine
WORKDIR /front-end

ARG BUILD_ENV

COPY --from=0 /front-end/build /usr/share/nginx/html
COPY dockerized-nginx-${BUILD_ENV}.conf \
    /etc/nginx/conf.d/default.conf

# exposed port
EXPOSE 80

ENTRYPOINT ["sh", "-c", "nginx -t && nginx -g", "daemon off;"]