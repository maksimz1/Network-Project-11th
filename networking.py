import socket

size_header_size = 9
def __recv_amount(sock, size=4):
    buffer = b''
    while size:
        new_bufffer = sock.recv(size)
        if not new_bufffer:
            return b''
        buffer += new_bufffer
        size -= len(new_bufffer)
    return buffer


def recv_by_size(sock, return_type="string"):
    try:
        data = b''
        data_len = int(__recv_amount(sock, size_header_size))
        # code handle the case of data_len 0
        data = __recv_amount(sock, data_len)
        if return_type == "string":
            return data.decode()
    except OSError:
        data = '' if return_type == "string" else b''
    return data


def send_with_size(sock, data):
    if len(data) == 0:
        return
    try:
        if type(data) != bytes:
            data = data.encode()
        len_data = str(len(data)).zfill(size_header_size).encode()
        data = len_data + data
        sock.sendall(data)
    except OSError:
        print('ERROR: send_with_size with except OSError')


def __hex(s):
    cnt = 0
    for i in range(len(s)):
        if cnt % 16 == 0:
            print("")
        elif cnt % 8 == 0:
            print("    ", end='')
        cnt += 1
        print("%02X" % int(ord(s[i])), end='')