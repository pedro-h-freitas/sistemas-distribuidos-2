FROM node:22-alpine

WORKDIR /app

# Instala as dependências
COPY package.json package-lock.json ./
RUN npm ci

# Copia os arquivos do frontend
COPY . .

EXPOSE 5173

# Inicia o Vite acessível fora do container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
