#!/usr/bin/python3
#
# A simple function to dump delivered events to stdout and report them
# via web page.

import logging

from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from flask import Flask, request
from typing import Callable, TypeVar, Mapping
import ujson

m = marshaller.NewDefaultHTTPMarshaller()

T = TypeVar('T')

app = Flask(__name__)

def Handle(func: Callable[[object, dict], None]) -> None:
    """Invoke func whenever an event occurs.

    Assumes func is a method which takes two arguments: data and context.
    data: type T, which should be able to be constructed from a string.
    context: a dict containing cloudevents context information.
    """
    def handle():
        event = m.FromRequest(
            v02.Event(),
            request.headers,
            request.stream,  # Maybe request.data?
            ujson.load)
        return f'**{request.headers.get("ce-time")}**\n\n{request.headers}\n\n{func(event.Data(), event)}'
        #return '', 200
    
    app.add_url_rule('/', 'handle', handle, methods=['POST'])

def Get(func: Callable[[], None]) -> None:
    """Invoke the specified func on Get requests.
    """
    app.add_url_rule('/', 'get', func)


_received = []

@Handle
def LogEvent(data :str, context: dict):
    _received.append((data, context))

    out = [str(data)]
    app.logger.info(context.Properties())
    # for k, v in context.Properties().items():
    #     if k == 'data':
    #         continue
    #     out.append(f'  {k}: {v}')
    out.extend((f'  {k}: {v}' for k, v in context.Properties().items() if k != 'data'))
    out.append('-----')
    app.logger.info('\n'.join(out))
    out.append('')
    return '\n'.join(out)

@Get
def ShowEvents():
    out = ['<!DOCTYPE html><html><body>']
    out.append(f'<!--{_received}-->')
    for event, context in _received:
        out.append(f'<!--{event}    {context.__dict__}-->')
        out.append(f'<h2>{context.EventTime()}</h2>')
        out.append(f'<pre>{event}</pre>')
        out.append('<table><tr><th>Context</th><th>Value</th></tr>')
        out.extend((f'<tr><td>{k}</td><td>{v}</td></tr>' for k,v in context.Properties().items() if k != 'data'))
        out.append('</table><hr/>')
    out.append('</body></html>')
    return '\n'.join(out)

if __name__ == '__main__':
    app.run(debug=True)
