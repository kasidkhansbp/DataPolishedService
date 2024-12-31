# Use the official AWS Lambda Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt to the container and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your Lambda function code into the container
COPY . /app/

# The Lambda function handler (e.g., app.lambda_handler) is required
CMD ["index.lambda_handler"]