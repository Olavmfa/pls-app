# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

# Set workdir
WORKDIR /app

# Copy files to work dir
COPY . .

# Install dependencies
RUN python -m pip install -r requirements.txt

RUN echo 'alias pls="python cli.py"' >> ~/.bashrc

# Run flask application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]
