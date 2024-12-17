FROM node:16-alpine as build-stage

WORKDIR /app/ui

COPY package*.json ./

RUN npm install

COPY . .

#RUN npm run build

# FROM nginx:stable-alpine as production-stage

# COPY --from=build-stage /ui/dist /usr/share/nginx/html

# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]

EXPOSE 3000

CMD [ "npm", "run", "dev", "--", "--host", "0.0.0.0" ]