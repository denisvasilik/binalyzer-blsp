"""
    binalyzer_blsp.blsp
    ~~~~~~~~~~~~~~~~~~~

    This module implements the BLSP server.
"""
import socketserver
import json
import logging

from jsonrpc import (
    JSONRPCResponseManager,
    dispatcher,
)

from .model import BinalyzerSymbolInformationNode


logger = logging.getLogger('binalyzer.blsp')

stdout_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


@dispatcher.add_method
def initialize(**kwargs):
    return True


@dispatcher.add_method
def binding(**kwargs):
    return json.dumps(BinalyzerSymbolInformationNode().__dict__)


@dispatcher.add_method
def shutdown(**kwargs):
    pass


class JsonRPCHeader(object):

    def __init__(self):
        self.content_length = 0
        self.charset = 'utf-8'

    def __str__(self):
        return f'Content-Length: {self.content_length}\r\n' + \
            f'Content-Type: application/vscode-jsonrpc; charset={self.charset}' + \
            '\r\n\r\n'


class JsonRPCMessage(object):

    def __init__(self, header=None, content=''):
        self.header = header
        if self.header is None:
            self.header = JsonRPCHeader()
        self.content = content


class JsonRPCParser(object):

    def __init__(self):
        self._message = JsonRPCMessage()
        self._header_field = ''
        self._newline = False
        self._header = True

    def parse(self, message):
        for character in message:
            self.parse_character(character)
        return self._message

    def parse_character(self, character):
        if self._header:
            if character == '\n':
                if self._newline:
                    # Two consecutive newlines have been read, which signals
                    # the start of the message content
                    self._header = False
                else:
                    # A single newline ends a header field
                    self._parse_header_field(self._header_field)
                    self._header_field = ''
                self._newline = True
            elif character != '\r':
                # Add the input to the current header field
                self._header_field += character
                self._newline = False
        else:
            self._message.content += character
            if self._message.header.content_length == len(self._message.content):
                return self._message
        return None

    def _parse_header_field(self, header_field):
        separator_position = header_field.find(':')
        key = header_field[:separator_position]
        if key == 'Content-Length':
            value = header_field[separator_position + 1:]
            self._message.header.content_length = int(value)
        elif key == 'Content-Type':
            charset_position = header_field.find('charset=')
            self._message.header.charset = header_field[charset_position + 8:]


class BLSPServer(socketserver.BaseRequestHandler):

    def handle(self):
        json_rpc_parser = JsonRPCParser()
        while True:
            character = self.request.recv(1)
            if not character:
                break
            message = json_rpc_parser.parse_character(str(character, 'utf-8'))
            if message is None:
                continue
            logger.debug(f'JSON-RPC Request: {repr(str(message.header))}')
            response = JSONRPCResponseManager.handle(
                message.content, dispatcher)
            json_rpc_response = 'Content-Length: ' + \
                str(len(response.json)) + '\r\n\r\n'
            json_rpc_response += response.json
            logger.debug(f'JSON-RPC Response: {repr(str(json_rpc_response))}')
            self.request.sendall(bytes(json_rpc_response, "utf-8"))
