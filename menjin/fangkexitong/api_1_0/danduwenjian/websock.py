# # -*- coding: utf-8 -*-
# # !/usr/bin/env python
#
# import asyncio
# import websockets
# import json
#
#
# async def test_ws_quote():
#     async with websockets.connect('ws://192.168.0.205:8888/quote/quote') as websocket:
#         req = {"protocol": "history_req", 'code': 'XAGODS', 'type': 'MINUTE', 'start_pos': '0', 'pos_num': '10'}
#         await websocket.send(json.dumps(req))
#
#         while True:
#             quote = await websocket.recv()
#             print(quote)
#
#
# asyncio.get_event_loop().run_until_complete(test_ws_quote())