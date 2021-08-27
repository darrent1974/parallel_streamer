import sys
import time
import zmq
import random
import os
import argparse
import tifffile
from pathlib import Path


def tif_writer(file_prefix, data_path):
    ZMQ_WORKER_ADDRESS = os.environ["ZMQ_WORKER_ADDRESS"]
    worker_id = random.randrange(1, 10005)

    print(f"Worker #{worker_id}")

    context = zmq.Context()

    # receive work
    worker_receiver = context.socket(zmq.PULL)
    worker_receiver.connect(ZMQ_WORKER_ADDRESS)

    while True:
        # Receive the serialised python object
        work_message = worker_receiver.recv_pyobj()

        # Extract items
        data = work_message['data']
        frame = work_message['frame']

        # Construct filename
        filename = Path(data_path) 
        filename = filename / f'{file_prefix}{frame: 06}.tif'

        # Write tif file
        tifffile.imwrite(filename, data)

        result = {'worker': worker_id,
                  'data': data.shape, 'filename': filename}

        print(result)


parser = argparse.ArgumentParser()
parser.add_argument('--file_prefix', dest='file_prefix')
parser.add_argument('--data_path', dest='data_path')

args = parser.parse_args()


tif_writer(args.file_prefix, args.data_path)
