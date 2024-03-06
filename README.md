# `bd` project by matrikater

## An idea for the logo

The `bd` kind of already looks like an owl. I think we could make it look more like an owl by adding some eyes and a beak.
This would work because owls have some of the best vision in the animal kingdom,
and we want our code to have the best vision too.

## RIGHT NOW THE PROJECT IS A MESS :cry:

As of Friday, 2nd of Feb 2024, I am working on the `./src/tests.py` file.

---

As of Friday, 2nd of Feb 2024, inside this file, I am trying to get the `infoinject` module working.

Once we have the `infoinject` working, we can use it for extensive debugging information which will come in handy since we
do actually want the code to be somewhat reliable.

---

As of Saturday, 3rd of Feb 2024, I am working on the `./src/ptysocket/__init__.py` file.

---

As of Sunday, 4th of Feb 2024, I have done a few things:

>- [X] I think I worked out that the issue of `Error receiving data: Too many values to unpack` or whatever, was caused by the
> supersocket module. It is the `recv` of the `ANetworkManipulator`.

...

>- [X] I made an example app, a simple chat app, which uses the `supersocket` module.

Doing this gave me a better understanding of the `supersocket` module...

I realized that the naming of functions was a bit off.

For example, take this client code:

```python
from supersocket import Client, Packet

client = Client("127.0.0.1", 3000)

client.begin()

client.send(Packet("Hello, World!"))
```

Doesn't this seem to be a bit off? It's written like we're sending a packet to the client, but we're actually sending it to the server.

I think it would be better if we had a `ServerRepresentative` and a `ClientRepresentative` class,
and then once we have a connection, we can:

- If writing server, replace the `server` instance with a `ClientRepresentative` instance for communicating with the client.

- Or, if writing client, replace the `client` instance with a `ServerRepresentative` instance for communicating with the server.

This solution also works out really nicely on the server side since it might want to keep track of multiple clients.

One downside however is that we have to keep two objects in memory.

Another alternative to this is to have a `_send_` and `_recv_` method for the abstract `ANetworkManipulator` class, then inside the `Client`:

```python
def send_to_server(self, packet):
    self._send_(packet)
```

and inside the `Server`:

```python
def send_to_client(self, packet):
    self._send_(packet)
```

etc.

## Going forward

>- [ ] We want to get a unittest of `supersocket` and make sure that all its current features work.

...

>- [ ] More tests - an entire test-suite for all our fancy modules.

...

>- [ ] We want to setup a system so that whenever we run our code, we can run all the automated test-suite at
> once. Then, on closure of our program, it will show the results of the test-suite.

We should use multiprocessing for this, so that the test-suite can run in the background.
