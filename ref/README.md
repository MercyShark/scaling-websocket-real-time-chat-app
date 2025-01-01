docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

if container already exists 

docker start redis-stack

docker exec -it redis-stack bash