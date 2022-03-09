import logging
import time
import codecs
from multiprocessing import Queue, Pipe, Process
import select
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the logging file handler
fh = logging.FileHandler('artifacts/hard.log')

formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def process_A(input_queue, output_pipe):
    while True:
        if not input_queue.empty():
            output_pipe.send(input_queue.get().lower())
            time.sleep(5)


def process_B(input_pipe, output_pipe):
    while True:
        output_pipe.put(codecs.encode(input_pipe.recv(), 'rot_13'))


if __name__ == '__main__':
    a_input = Queue()
    a_output, b_input = Pipe()
    # b_output, main_input = Pipe()
    main_input = Queue()

    a_process = Process(target=process_A, args=(a_input, a_output))
    a_process.start()

    b_process = Process(target=process_B, args=(b_input, main_input))
    b_process.start()

    while True:
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            input_str = sys.stdin.readline().strip('\n')
            logger.info(f'recieved message: {input_str}')
            a_input.put(input_str)
        while not main_input.empty():
            message = codecs.decode(main_input.get(), 'rot_13')
            print(message)
            logger.info(f'send message: {message}')
