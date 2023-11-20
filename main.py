from collections import defaultdict

# Функция для чтения данных из файла
def read_data(file_name):
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip().split(';')
            # Проверка на корректность данных (проверка количества полей и их формата)
            if len(line) == 7:
                data.append(line)
    return data

# Функция для ответа на вопросы
def analyze_traffic(data):
    unique_nodes = set()
    node_info = defaultdict(lambda: {'speed': 0, 'sessions': 0, 'UDP_dest': set(), 'TCP_dest': set()})

    for line in data:
        src_node, _, dest_node, _, is_udp, data_size, transfer_time = line
        data_size = int(data_size)
        transfer_time = float(transfer_time)

        unique_nodes.add(src_node)
        unique_nodes.add(dest_node)

        speed = data_size / transfer_time
        node_info[src_node]['speed'] += speed
        node_info[src_node]['sessions'] += 1
        node_info[dest_node]['speed'] += speed
        node_info[dest_node]['sessions'] += 1

        if is_udp == 'true':
            node_info[src_node]['UDP_dest'].add(dest_node)
        else:
            node_info[src_node]['TCP_dest'].add(dest_node)

    # Q1
    unique_nodes_count = len(unique_nodes)
    print(f"Q1. Количество уникальных узлов в сети: {unique_nodes_count}")

    # Q2
    total_speed = sum(info['speed'] for info in node_info.values())
    total_sessions = sum(info['sessions'] for info in node_info.values())
    avg_network_speed = total_speed / total_sessions if total_sessions > 0 else 0
    print(f"Q2. Средняя скорость передачи данных всей сети: {avg_network_speed} байт/сек")

    # Q3
    udp_speed = sum(info['speed'] for info in node_info.values() if info['UDP_dest'])
    tcp_speed = sum(info['speed'] for info in node_info.values() if info['TCP_dest'])
    print("Q3. ", end="")
    if udp_speed > tcp_speed:
        print("UDP используется для передачи данных с максимальной пиковой скоростью.")
    else:
        print("UDP не используется для передачи данных с максимальной пиковой скоростью.")

    # Q4
    top_10_nodes = sorted(node_info.items(), key=lambda x: x[1]['speed'] / x[1]['sessions'], reverse=True)[:10]
    print("Q4. Топ 10 узлов с самой высокой средней скоростью передачи данных:")
    for node, info in top_10_nodes:
        avg_speed = info['speed'] / info['sessions'] if info['sessions'] > 0 else 0
        print(f"Узел: {node}, Средняя скорость: {avg_speed} байт/сек")

    # Q5
    subnet_sessions = defaultdict(int)
    for node in node_info:
        subnet = '.'.join(node.split(':')[0].split('.')[:3])
        subnet_sessions[subnet] += 1

    top_10_subnets = sorted(subnet_sessions.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Q5. Топ 10 самых активных подсетей /24 по количеству сессий передачи данных:")
    for subnet, sessions in top_10_subnets:
        print(f"Подсеть: {subnet}, Количество сессий: {sessions}")

    # Q6
    proxies = set()
    for node, info in node_info.items():
        udp_dest = info['UDP_dest']
        tcp_dest = info['TCP_dest']
        for dest in udp_dest & tcp_dest:
            if node_info[dest]['UDP_dest'] & node_info[dest]['TCP_dest']:
                proxies.add(node)
                break

    if proxies:
        print("Q6. Узлы, которые могут быть посредниками (PROXY) между другими узлами:")
        for proxy in proxies:
            print(f"Потенциальный PROXY: {proxy}")
    else:
        print("Q6. В сети нет узлов-посредников (PROXY).")

# Чтение данных из файла и анализ
file_data = read_data("traf.txt")
analyze_traffic(file_data)
