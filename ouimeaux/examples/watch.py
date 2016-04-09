#!/usr/bin/env python
import argparse
import sys
import traceback
from ouimeaux.environment import Environment
from ouimeaux.utils import matcher
from ouimeaux.signals import receiver, statechange, devicefound

class Watcher(object):
    def __init__(self):
        self.state = None

    def mainloop(self, name):
        matches = matcher(name)

        @receiver(devicefound)
        def found(sender, **kwargs):
            if matches(sender.name):
                print "Found device:", sender.name
    
        @receiver(statechange)
        def motion(sender, **kwargs):
            if matches(sender.name) and self.state != kwargs.get('state'):
                self.state = kwargs.get('state')
                print "{} state is {state}".format(
                    sender.name, state="on" if kwargs.get('state') else "off")
        env = Environment()
        try:
            env.start()
            env.discover(10)
            env.wait()
        except (KeyboardInterrupt, SystemExit):
            print "Goodbye!"
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Motion notifier")
    parser.add_argument("name", metavar="NAME",
                        help="Name (fuzzy matchable)"
                             " of the Motion to detect")
    args = parser.parse_args()
    w = Watcher()
    w.mainloop(args.name)
