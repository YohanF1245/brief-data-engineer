FROM node:alpine3.22

WORKDIR /api 

COPY package.json /api

RUN npm install

EXPOSE 555

COPY . /api

CMD ["node", "app.js"]
