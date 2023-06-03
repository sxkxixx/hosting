FROM node:20.2.0-alpine3.17 as build

WORKDIR front/

COPY . .

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL ${REACT_APP_API_URL}

RUN npm install
RUN npm run build

FROM nginx:1.23.0-alpine

COPY --from=build /front/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx/default.conf /etc/nginx/conf.d

CMD ["nginx", "-g", "daemon off;"]
