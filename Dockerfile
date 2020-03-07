FROM python

WORKDIR /home

COPY ./requirement.txt ./
RUN pip3 install --no-cache-dir -r requirement.txt

COPY . .
CMD ["bash", "game.sh"]