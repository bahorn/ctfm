#!/usr/bin/env python3

# Generic instance type for the more specific ones to inherit from.

## Generic interface all Instances must expose.
class Instance:
    def __init__(self, config):
        self.config = config
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def command(self):
        pass
