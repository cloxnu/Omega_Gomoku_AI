FROM tensorflow/tensorflow:2.0.0-py3

WORKDIR /home

COPY ./Omega_Gomoku_AI .
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["bash", "game.sh"]