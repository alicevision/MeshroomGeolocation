from argparse import ArgumentParser
import logging
import generate_north
import log_level

def build_argument_parser() -> ArgumentParser:
    '''Parsing of all arguments'''
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--GPSFile", help="GPSFile", type=str)
    argument_parser.add_argument("--outputPath", help="output", type=str)
    argument_parser.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    argument_parser.add_argument("--outputFolder", help="outputFolder", type=str)
    return argument_parser

def main():
    args = build_argument_parser()
    args = args.parse_args()

    logging.basicConfig(level=log_level.text_to_log_level(args.verboseLevel))

    logging.info("North !")

    generate_north.generate_north(args.outputFolder, args.outputPath)

    logging.info("North generated")


if __name__ == "__main__":
    main()
