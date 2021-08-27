import time
import zmq
import os
import numpy as np
import argparse


def frame_producer(rate, size_x, size_y):
    ZMQ_PRODUCER_ADDRESS = os.environ["ZMQ_PRODUCER_ADDRESS"]
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.connect(ZMQ_PRODUCER_ADDRESS)

    frame = 0

    # Start your result manager and workers before you start your producers
    while True:
        time.sleep(1./rate)

        # generate random numpy array of uint16
        data = np.random.random_integers(0, np.iinfo(
            np.int16).max, (size_x, size_y)).astype(np.uint16)

        # Assemble message
        work_message = {'htype': "array-1.0",
                        'shape': data.shape,
                        'type': data.dtype.name,
                        'frame': frame,
                        'ndattr': {'NumImages': 1},
                        'data': data
                        }

        zmq_socket.send_pyobj(work_message)

        frame += 1


parser = argparse.ArgumentParser()
parser.add_argument('--rate', dest='rate', type=int, default=1)
parser.add_argument('--size_x', dest='size_x', type=int, default=1024)
parser.add_argument('--size_y', dest='size_y', type=int, default=1024)

args = parser.parse_args()

frame_producer(args.rate, args.size_x, args.size_y)
