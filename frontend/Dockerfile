# Estágio de compilação
FROM node:16 AS builder

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app/frontend/

# Copie os arquivos de configuração do projeto
COPY package*.json ./

# Instale as dependências
RUN npm install

# Copie o código do aplicativo
COPY . .

RUN npm run build

# Estágio de produção
FROM nginx:alpine

# Copie os arquivos de compilação do estágio anterior para o diretório do servidor HTTP
COPY --from=builder /app/frontend/dist /usr/share/nginx/html

# Exponha a porta do servidor HTTP
EXPOSE 80

# Inicie o servidor HTTP
CMD ["nginx", "-g", "daemon off;"]