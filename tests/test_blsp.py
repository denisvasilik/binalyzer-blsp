import os
import io
import pytest
import unittest
import socket
import socketserver
import sys

from binalyzer_blsp import JsonRPCParser


def test_parse_json_rcp_request_add_to_header_field():
    parser = JsonRPCParser()
    parser.parse_character('a')
    assert parser._header_field == 'a'


def test_parse_json_rcp_request_ignore_carriage_return():
    parser = JsonRPCParser()
    parser.parse('abc\r')
    assert parser._header_field == 'abc'


def test_parse_json_rcp_request_first_newline():
    parser = JsonRPCParser()
    message = parser.parse(
        'Content-Length: 40\r\nContent-Type: application/vscode-jsonrpc; charset=utf-8\r\n\r\n{}')
    assert message.header.content_length == 40
    assert message.header.charset == 'utf-8'
    assert message.content == '{}'

@pytest.mark.skip
def test_blsp_server_method_initialize():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as blsp_socket:
        blsp_socket.connect(("localhost", 5000))

        request_data0 = 'Content-Length: 200\r\n\r\n'
        request_data1 = '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"applicationId":"c9274035-bea7-42a4-85d6-019c09e56a46","options":{"timestamp":"2020-12-12T16:39:47.785Z","message":"Custom Options Available"}}}'

        expected_response = b'Content-Length: 43\r\n\r\n{"result": true, "id": 0, "jsonrpc": "2.0"}'

        blsp_socket.sendall(bytes(request_data0, 'utf-8'))
        blsp_socket.sendall(bytes(request_data1, 'utf-8'))
        actual_response = blsp_socket.recv(1024)

        assert expected_response == actual_response
