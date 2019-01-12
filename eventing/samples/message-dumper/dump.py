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

T = Typevar('T')

app = Flask(__name__)

def Handle(func: Callable[[T, dict], None]) -> None:
    """Invoke func whenever an event occurs.

    Assumes func is a method which takes two arguments: data and context.
    data: type T, which should be able to be constructed from a string.
    context: a dict containing cloudevents context information.
    """
    def handle():
        event = m.FromRequest(
            v02.Event(),
            request.headers,
            request.data,  # Maybe request.stream?
            T)
        func(event.Data(), event)
        return '', 200
    
    app.add_url_rule('/', 'handle', handle, methods=[method])

def Get(func: Callable[] -> str) -> None:
    """Invoke the specified func on Get requests.
    """
    app.add_url_rule('/', 'get', handle)


_received = []

@Handle
def LogEvent(data, context):
    _received.append((data, context))

    out = [str(data)]
    out.extend((f'  {k}: {v}' for k, v : context.Properties() if k != 'data'))
    out.append('-----')
    logging.info('\n'.join(out))

@Get
def ShowEvents():
    out = ['<!DOCTYPE html><html><body>']
    for event in _received:
        out.append(f'<h2>{event.EventTime()}</h2>')
        out.append(f'<pre>{event.Data()}</pre>')
        out.append('<table><tr><th>Context</th><th>Value</th></tr>')
        out.extend((f'<tr><td>{f}</td><td>{v}</td></tr>' for k,v in context.Properties() if k != 'data'))
        out.append('</table><hr/>')
    out.append('</body></html>')
    return '\n'.join(out)

if __name__ == '__main__':
    app.run(debug=True)
