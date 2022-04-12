import argparse
import socket
from multiprocessing import Process


def scan_port_tcp(host, port):
    '''Создаем сокет для подключения к порту, если удалось подключиться,
    то порт открыт(SOCK_STREAM - соединение типа TCP)'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(0.5)
        sock.connect((host, port))
        print('Tcp Port :', port, ' is open.')
    except:
        pass
    finally:
        sock.close()


def scan_port_udp(host, port):
    '''(SOCK_DGRAM - соединение типа TCP) В Udp нет понятия сооединения, как в Tcp, поэтому, чтобы проверить открыт ли порт,
     надо отправить запрос на этот порт. Если есть ответ, порт открыт, но так как отправляется не действительная команда,
     то время ожидания будет превышать, но порт будет открыт'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(b'', (host, port))
        sock.settimeout(0.5)
        sock.recvfrom(1024)
    except socket.timeout:
         print('Udp Port :', port, ' is open.')
    except:
        pass
    finally:
        sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Сканер TCP и UDP портов')
    parser.add_argument('host', type=str, help='Хост')
    parser.add_argument('start', type=int, help='Начальное значение диапазона')
    parser.add_argument('end', type=int, help='Конечное значение диапазона')
    args = parser.parse_args()
    for i in range(args.start, args.end):
        t = Process(target=scan_port_tcp, args=(args.host, i))
        t2 = Process(target=scan_port_udp, args=(args.host, i))
        t.start()
        t2.start()
