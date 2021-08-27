A basic 0MQ "streamer" device example to demonstrate the use of multiple/parallel "writer" containers

Derived from:
https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/streamer.html

To start use:

docker-compose up --scale tif_writer=N

Where N equals the number of tif writer containers to create