import os
import sys
import xlrd
#import xlutils
#from xlutils.copy import copy as xlutils_copy
from websocket_server import WebsocketServer

def read(file):
    book = xlrd.open_workbook(file)
    #table = data.sheet_by_index(0)
    tables = book.sheets()
    src = []

    for table in tables:
        nRows = table.nrows
        nCols = table.ncols
        for i in range(nRows):
            for j in range(nCols):
                v = table.cell(i, j).value
                v = v.strip()
                if v != '':
                    src.append(v)                    
                    print(table.cell(i, j).value)

    return src

def translateByChromeExtension(src):
    data = [0, src]

    def sendMessage(server, client):
        server.send_message(client, src[index])
        index += 1

    def new_client(client, server):
        print("New client connected and was given id %d" % client['id'])
        data = new_client.data
        if data[0] < len(data[1]) :
            server.send_message(client, data[1][data[0]])
            data[0] += 1
        else:
            print('finished!')
        #server.send_message_to_all("Hey all, a new client has joined us")

    new_client.data = data

    # Called for every client disconnecting
    def client_left(client, server):
        print("Client(%d) disconnected" % client['id'])


    # Called when a client sends a message
    def message_received(client, server, message):
        #if len(message) > 200:
	    #    message = message[:200]+'..'
        print("<== Client(%d) said: %s" % (client['id'], message))
        data = message_received.data
        print('    ==> ' + data[1][data[0]])
        if data[0] < len(data[1]) :
            server.send_message(client, data[1][data[0]])
            data[0] += 1
        else:
            print('finished!')

    message_received.data = data

    # Called for every client connecting (after handshake)
    PORT = 9001
    server = WebsocketServer(PORT, host='127.0.0.1')#, loglevel=logging.INFO)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()

if __name__ == '__main__':
    file = sys.path[0] + '/' + sys.argv[1]
    source = read(file)
    if len(source) <= 0:
        print('data source out of range.')
    
    translateByChromeExtension(source)
