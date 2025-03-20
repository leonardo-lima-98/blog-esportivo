# Use uma imagem base do Nginx
FROM nginx:alpine

# Remova a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copie a configuração do Nginx personalizada
COPY nginx.conf /etc/nginx/conf.d/

# Copie os arquivos estáticos do frontend (React build)
COPY --from=frontend /app/dist /usr/share/nginx/html

# Copie os arquivos estáticos do backend (FastAPI static files, se houver)
# Exemplo: COPY --from=backend /app/static /usr/share/nginx/html/static

# Exponha a porta 80
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]