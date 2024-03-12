# How to go from here with `PLS`?

## TODO

### Top priority:

- [x] Fix the `InfoInjector.py` to work with the new `PLS` lib.
- [ ] Write a few tests in some other projects to test its usability.

### Some other shits:

- [ ] Add a `PLS` logo.
- [ ] Look at other more popular libs to see how ours stacks up and then add to this list accordingly.
- [ ] I looked at the python built-in `logging` lib and it seems to be a good reference for how to structure the `PLS` lib.

For example, they have it layed out with a `Logger` class that can contain:

- A method of formatting the log messages.
- A method of handling the log messages, i.e. where to send them.
- A method of filtering the log messages, i.e. what to send.

Our `PLS` lib should have a similar structure.

### Once we're happy:

- [ ] Add a detailed documentation.
- [ ] Add a more generalized README.
