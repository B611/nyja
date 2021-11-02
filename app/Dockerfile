FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .
COPY populate.py .
RUN apk add fish bash libmagic tzdata gcc musl-dev g++
RUN pip install -r requirements.txt
RUN mkdir -p ~/.config/fish
RUN printf "set fish_greeting 'Welcome to Nyja ! Run the command \"nyja -h\" to get started '\n" >> ~/.config/fish/config.fish
RUN printf "set PATH /app/bin $PATH\n" >> ~/.config/fish/config.fish
RUN printf "cd /app/user_dir\n" >> ~/.config/fish/config.fish
RUN printf "register-python-argcomplete --shell fish nyja | source\n" >> ~/.config/fish/config.fish
RUN printf "python /app/populate.py" >> ~/.config/fish/config.fish
