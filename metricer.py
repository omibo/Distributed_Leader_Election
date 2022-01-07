import sys, os
import subprocess


def run_runner_script(round_num):
    for i in range(round_num):
        delete_rabbitmq_queues()
        subprocess.call('python3 runner.py --input input_002.in --stdout --debug', shell=True)
        # subprocess.call('python3 runner.py --graph_type k_regular --k_regular 3 --nodes_num 6 --stdout --debug', shell=True)


def get_n_last_dirs(round_num):
    return sorted([item for item in os.listdir("./output") if os.path.isdir(os.path.join("./output", item))])[-round_num:]


def get_msg_complexity(round_name):
    message_complexity = 0
    path = round_name + '/logs'
    filelist = [item for item in os.listdir(path) if (os.path.isfile(os.path.join(path, item)) and item[-1] != 't')]
    for file_name in filelist:
        with open(path + '/' + file_name, 'r') as f:
            last_line = f.readlines()[-1]
            message_complexity += int(last_line.split(": ", 1)[1])
    return message_complexity


def delete_rabbitmq_queues():
    import pika
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost'))
    channel = connection.channel()
    for i in range(100):
        channel.queue_delete(queue=f'node{str(i)}')
    connection.close()


def get_avg_msg_complexity(complexity_list):
    sum_val = 0
    count = 0
    for k, v in complexity_list.items():
        sum_val += v
        count += 1
    return sum_val/count


if __name__ == '__main__':
    round_num = int(sys.argv[1])
    run_runner_script(round_num)
    dirlist = get_n_last_dirs(round_num)
    runtime_message_complexity = dict()

    for dir_name in dirlist:
        complexity = get_msg_complexity('./output/' + dir_name)
        runtime_message_complexity[dir_name] = complexity

    print(runtime_message_complexity)
    avg_msg_complexity = get_avg_msg_complexity(runtime_message_complexity)
    print(avg_msg_complexity)



