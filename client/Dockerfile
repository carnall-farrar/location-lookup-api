# Build dependencies (to cache)
FROM node:16.3.0-alpine3.13 as deps
WORKDIR /usr/src/app
COPY ./package.json .
COPY ./yarn.lock .
RUN yarn

# Build project
FROM node:16.3.0-alpine3.13 as build
WORKDIR /usr/src/app
COPY --from=deps /usr/src/app .
COPY . .
RUN yarn build