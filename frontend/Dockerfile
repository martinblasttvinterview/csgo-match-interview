FROM node:18-alpine AS development

WORKDIR /app/frontend

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "docker-dev"]
