# Links
[CyberBrain_Backtracing](https://github.com/laike9m/Cyberbrain)<br>
[PySnooper](https://github.com/cool-RR/PySnooper)<br>
[IceCream](https://github.com/gruns/icecream)<br>
[Hunter](https://github.com/ionelmc/python-hunterq)<br>
[BirdsEye](https://pypi.org/project/birdseye/)<br>
[PySpy](https://github.com/benfred/py-spy)<br>
# Notes
## What is Debugging?
- Finding errors in code, for this talk _why_ program gives the wrong result
- Four types of errors
  - Bytecode (syntax)
  - Logic (bad if/else flow control)
  - Runtime Errors (bad user input)
  - Latent Errors (disk full)
## Types of Debugging
- print 
  - won't change code at runtime
  - OOB on all code
- logging
  - configurable
  - easy to manage output
  - richer context than print, e.g. metadata
- debuggers
  - doesn't require code familiarity
  - rich featuresets like breakpoints, stepthrough, code-insertion
## Issues with Current Models
- Debuggers have heavy programmer overhead due to: 
  - rote tasks/memorization in what/where vars are in logic
  - how artifacts affect each other
  - bytecode issues that aren't exposed in high-level languages
- Print and logging both have heavy config overhead/manual effort to use for debugging
## Helper Tips
- `sys.settrace(callback)` will print the stack to allow you to see what's happening at the CPython level
- Cyberbrain trace decorators allow for backtrace through low-level funcs, generates graph of syscalls and dataflow