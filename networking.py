import socket

size_header_size = 4
DEBUG = True

def logtcp(dir, byte_data):
    """
    log direction and all TCP byte array data
    return: void
    """
    if dir == 'sent':
        print(f'C LOG:Sent     >>>{byte_data}')
    else:
        print(f'C LOG:Recieved <<<{byte_data}')

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
        data_len = __recv_amount(sock, size_header_size)
        data_len = int(data_len)
        # code handle the case of dappta_len 0
        data = __recv_amount(sock, data_len)
        if DEBUG:
            logtcp('recieved', data)
        if return_type == "string":
            return data.decode()
    except OSError:
        data = '' if return_type == "string" else b''
    return data


def send_by_size(sock, data):
    if len(data) == 0:
        return
    try:
        if type(data) != bytes:
            data = data.encode()
        len_data = str(len(data)).zfill(size_header_size).encode()
        data = len_data + data
        sock.sendall(data)
        if DEBUG:
            logtcp('sent', data)
    except OSError:
        print('ERROR: send_with_size with except OSError')
