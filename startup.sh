#!/bin/bash

# 启动 PostgreSQL
service postgresql start

# 等待 PostgreSQL 完全启动
echo "Waiting for PostgreSQL to start..."
until pg_isready -h localhost -U postgres; do
  sleep 1
done
echo "PostgreSQL started"

# 启动 Jetty
exec java -jar /opt/jetty/start.jar