FROM node:14-alpine as build-stage
WORKDIR /react-frontend

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Once the app is built, host it using a simple http-server
FROM node:14-alpine
# To debug and test access to services
RUN apk --no-cache add curl

WORKDIR /react-frontend

RUN npm install -g http-server

COPY --from=build-stage /react-frontend/build .

EXPOSE 8080
CMD ["http-server", "-p", "8080", "-a", "0.0.0.0"]