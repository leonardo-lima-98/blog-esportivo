# docker/frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copiar arquivos de dependências primeiro
COPY frontend/package.json frontend/package-lock.json* ./

# Instalar dependências
RUN npm ci

# Copiar o código do frontend
COPY frontend/ .

# Construir o aplicativo React
RUN npm run build

# Servidor de produção
FROM nginx:alpine

# Copiar build do React
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuração do nginx
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]