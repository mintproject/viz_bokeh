#/* vim: set filetype=dockerfile : */
FROM python:alpine

ARG BOKEH_VERSION
RUN apk add --no-cache g++ wget
RUN mkdir /bokeh
WORKDIR /bokeh
COPY . /bokeh
RUN pip install -r requirements.txt

ENTRYPOINT [ "bokeh serve  --show cycles/cycles_viz.py economic/LookupTable/econ_viz.py" ]