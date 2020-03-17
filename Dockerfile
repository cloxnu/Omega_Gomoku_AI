FROM tensorflow/tensorflow:2.0.0-py3

WORKDIR /home

COPY ./requirement.txt ./
RUN pip3 install --no-cache-dir -r requirement.txt

COPY . .
CMD ["bash", "game.sh"]