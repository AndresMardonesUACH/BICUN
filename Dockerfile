# Etapa 1: Construcción de la aplicación
FROM node:18 AS builder

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el package.json y package-lock.json (o yarn.lock) para instalar dependencias
COPY package.json package-lock.json ./

# Instalar las dependencias
RUN npm install

# Copiar el código fuente de la aplicación
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa 2: Imagen final para producción
FROM node:18-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar las dependencias de producción y la aplicación desde la etapa de construcción
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/public /app/public
COPY --from=builder /app/package.json /app/package.json

# Exponer el puerto en el que Next.js servirá la aplicación
EXPOSE 3000

# Comando para iniciar la aplicación en modo producción
CMD ["npm", "start"]
