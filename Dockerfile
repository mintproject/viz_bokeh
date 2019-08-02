#/* vim: set filetype=dockerfile : */
FROM mint-project/viz_bokeh:gams

RUN mkdir /bokeh
WORKDIR /bokeh
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "bokeh", "serve",  "--show",  "cycles/cycles_viz.py", "economic/LookupTable/econ_viz.py", "--allow-websocket-origin=viz.mint.isi.edu"]