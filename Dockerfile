# Use an official Python runtime as the parent image
FROM python:3.11.4-alpine3.18

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install

# Run your_bot_script.py when the container launches
CMD ["poetry", "run", "python", "-u", "strahd.py"]
