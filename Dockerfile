#/* vim: set filetype=dockerfile : */
FROM python:stretch

RUN mkdir /bokeh
WORKDIR /bokeh
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . /bokeh

ENTRYPOINT [ "bokeh", "serve",  "--show", "cycles/cycles_viz.py",  "--allow-websocket-origin=localhost:9099"]