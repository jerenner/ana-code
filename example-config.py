#!/usr/bin/env python
import argparse
import ConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf_file",
                    help="Specify config file", metavar="FILE")
args, remaining_argv = parser.parse_known_args()
defaults = {
    "option1" : "some default",
    "option2" : "some other default",
    }
if args.conf_file:
    config = ConfigParser.SafeConfigParser()
    config.read([args.conf_file])
    defaults = dict(config.items("Defaults"))

parser.set_defaults(**defaults)
parser.add_argument("--option1", help="some option")
parser.add_argument("--option2", help="some other option")
args = parser.parse_args(remaining_argv)
print args
