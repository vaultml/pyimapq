# pyimapq

This package uses any IMAP server as a python queue, allowing processes in
separate domains to communicate over EMAIL.

All you need is an IMAP account, and you are good to go.

Example usage:

```python
from pyimapq import PyImapQ


mq = PyImapQ(user='my_user', password='very strong password')
assert mq.connected

def flt(subject):
	return subject in ['a', 'list', 'of', 'subjects', 'to', 'accept']

msgs = mq.get_unread_emails(flt, mark_as_read=True)

# msgs will now hold the email itself. You can use mq.get_body(msg) to get the
# body, or msg['Subject'], etc, to access the message meta data
```
