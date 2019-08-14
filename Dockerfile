#/* vim: set filetype=dockerfile : */
FROM mint-project/viz_bokeh:gams

RUN apt-get update && apt-get install -y \
    curl \
    zip

RUN mkdir /bokeh
WORKDIR /bokeh
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN ./run

ENTRYPOINT [ "bokeh", "serve",  "--show",  "cycles/cycles_viz.py", "economic/calibration/econ_calib_viz.py", "--allow-websocket-origin=viz.mint.isi.edu"]
