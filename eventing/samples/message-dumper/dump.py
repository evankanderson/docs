# Function to execute in decoupled execution mode.
import run
import logging

_received = []

@run.Handle
def LogEvent(data :str, context: dict):
    _received.append((data, context))

    out = [str(data)]
    logging.info(context.Properties())
    # for k, v in context.Properties().items():
    #     if k == 'data':
    #         continue
    #     out.append(f'  {k}: {v}')
    out.extend((f'  {k}: {v}' for k, v in context.Properties().items() if k != 'data'))
    out.append('-----')
    logging.info('\n'.join(out))
    out.append('')
    return '\n'.join(out)

@run.Get
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
