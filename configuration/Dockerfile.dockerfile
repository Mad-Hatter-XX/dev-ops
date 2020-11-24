# Set the base image to Ubuntu
FROM    python:3.6

# File Author / Maintainer
LABEL Chris G <cgreen@gmail.me>

# Install nodemon
RUN pip install pandas

# Add a /app volume
VOLUME ["/app"]

# TODO: link the current . to /app

# Define working directory
WORKDIR /app

# Expose port
EXPOSE  8080

# Run app using nodemon
CMD ["python","/app/test_trash.py"]