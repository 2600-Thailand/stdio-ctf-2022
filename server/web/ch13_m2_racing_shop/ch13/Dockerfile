FROM node:current-buster-slim

RUN mkdir -p /app
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
USER node
EXPOSE 1337

CMD ["node", "index.js"]