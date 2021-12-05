FROM mongo:5.0.3

RUN echo "rs.initiate();" > /docker-entrypoint-initdb.d/replica-init.js

# COPY init.js /docker-entrypoint-initdb.d/