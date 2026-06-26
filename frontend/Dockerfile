FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

ENV NEXT_PUBLIC_API_BASE=https://cccmahir-cccmahirapi-xo8obl.76-13-211-119.sslip.io/v1

RUN npm run build

CMD ["npm", "start"]
