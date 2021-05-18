import socket


def main():

    # Battlenet IP
    BNET_IP = '137.221.105.152'

    # Battlenet Port
    BNET_PORT = 1119

    # Attempt to talk to BattleNet
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((BNET_IP, BNET_PORT))

    except:
        print("Error connecting!")


if __name__ == '__main__':
    main()

