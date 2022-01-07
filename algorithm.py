import sys

from world import log, world, HELLO_MSG

got_hello_from = []
current_parent = None
current_wave = int(world.current_node)
received_neighbors = set()
leader = None

msg_complexity = len(world.neighbors)


def process_wave_msg(src, msg):
    global received_neighbors, current_wave, current_parent, leader, msg_complexity
    log(f"message from {src}: {msg}")

    if msg[0] == "D":
        leader = msg[1:]
        log(f"Leader node is {leader}")
        log(f"Broadcast result to neighbours")
        print(leader)
        msg_complexity += world.send_wave_to_neighbours(current_parent, 'D' + leader)
        log(f"message complexity: {msg_complexity}")
        sys.exit()

    msg = int(msg)

    if current_wave < msg:
        received_neighbors = {src}
        current_wave, current_parent = msg, src
        log(f"current wave:{current_wave}   current_parent:{current_parent}   received neighbors:{received_neighbors}")
        if received_neighbors == set(world.neighbors):
            log("Received from all neighbours except parent. Send this info to parent.")
            msg_complexity += world.send_wave_to_parent(current_parent, current_wave)
        else:
            log("Received new better wave. Send this info to neighbours expect parent.")
            msg_complexity += world.send_wave_to_neighbours(current_parent, current_wave)
    elif current_wave > msg:
        log(f"purge message from {src}: {msg}")
        return
    else:
        received_neighbors.add(src)
        log("same wave\treceived neighbors:" + str(received_neighbors))
        if received_neighbors == set(world.neighbors):
            log("Received message from all neighbours")
            if msg == int(world.current_node):
                log("This is leader. Broadcast this info to neighbours")
                leader = world.current_node
                msg_complexity += world.send_wave_to_neighbours(current_parent, 'D'+world.current_node)
                log(f"Leader node is {leader}")
                print(leader)
                log(f"message complexity: {msg_complexity}")
                sys.exit()
            else:
                log("Received from all neighbours new wave. Send this info to parent.")
                msg_complexity += world.send_wave_to_parent(current_parent, current_wave)

# def process_msg(src, msg):
#     log(f"message from {src}: {msg}")
#
#     if msg == "exit":
#         sys.exit()
#     elif msg == HELLO_MSG:
#         got_hello_from.append(src)
#
#     if set(got_hello_from) == set(world.neighbors):
#         world.send_message(to=world.current_node, msg='exit')  # TODO Maybe you want start your algorithm here!
