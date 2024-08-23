# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Set environment variables
ENV POSTGRES_DB=face_recg_db
ENV POSTGRES_USER=recg_user
ENV POSTGRES_PASSWORD=recg_pass
