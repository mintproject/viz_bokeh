#/* vim: set filetype=dockerfile : */
FROM mint-project/viz_bokeh:latest

RUN mkdir /bokeh
WORKDIR /bokeh
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ADD https://github.com/mintproject/EconVisualizations/archive/master.zip economic
ADD https://github.com/mintproject/CyclesViz/archive/master.zip cycles

ENTRYPOINT [ "bokeh", "serve",  "--show",  "cycles/cycles_viz.py", "economic/calibration/econ_calib_viz.py", "--allow-websocket-origin=viz.mint.isi.edu"]
