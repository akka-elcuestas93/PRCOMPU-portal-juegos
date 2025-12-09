# ========= Etapa 1: build de la app Vue =========
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# ========= Etapa 2: servir estáticos con Vite preview =========
FROM node:20-alpine

WORKDIR /app

COPY --from=build /app/dist ./dist

EXPOSE 4173

CMD ["npm", "exec", "vite", "preview", "--", "--host"]
