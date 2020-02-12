import argparse
import configparser

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file",
                    help="Specify config file", metavar="FILE")
    args, remaining_argv = parser.parse_known_args()

    config = configparser.SafeConfigParser()
    config.read([args.conf_file])
    defaults = dict(config.items("Defaults"))

    parser.set_defaults(**defaults)
    args = parser.parse_args(remaining_argv)

    #https://parezcoydigo.wordpress.com/2012/08/04/from-argparse-to-dictionary-in-python-2-7/
    return args
