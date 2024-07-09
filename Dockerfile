FROM python:3.8
WORKDIR /app
# Switch to root to perform root actions
USER root

# Remove the lock file
RUN rm -f /var/lib/apt/lists/lock
RUN apt install docker-buildx-plugin
COPY . .
RUN pip install mysql-connector-python pandas
CMD ["python", "app.py"]
