FROM node:18-alpine

WORKDIR /app

EXPOSE 3000

ENV REACT_APP_API_URL=http://localhost:5000

COPY package*.json ./

RUN npm ci

COPY . .

CMD ["npm", "start"]
