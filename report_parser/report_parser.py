from __future__ import print_function

import sys
import argparse
from classifier import Classify
from parsing import Parser
from printer import Print
from graphs.plotter import Plot
from os import walk


def main():
    parser = argparse.ArgumentParser(description="process all JSON files in the given directory"
                                                 "outputting the results in the given filename")
    parser.add_argument("parse_dir", help="enter the directory to parse")
    parser.add_argument("output_file", help="enter the file where the results will be written")
    parser.add_argument("-v", "--verbose", action="store_true", help="set verbose output")
    args = parser.parse_args()

    if args.verbose:
        printer = Print(True)
    else:
        printer = Print(False)

    p_dir = args.parse_dir
    output_file = args.output_file

    printer.standard_output('Chosen directory %s. Wait for file: %s to be generated' % (p_dir, output_file))
    printer.standard_output('verbose is set to: %r' % printer.get_verbose())

    printer.write_file(output_file, '', 'w')

    parsing = Parser(printer)
    parsing.parse_files(p_dir, output_file)

    in_dir = "docs/"
    in_file = "classify.json"
    classifier = Classify(printer)
    classifier.classify(output_file, in_dir, in_file)

    cat_dir = 'docs/randep-binary-maps/categories/'
    grap_dir = 'docs/randep-binary-maps/graphs/'
    plotter = Plot()
    for (dir_path, dir_names, file_names) in walk(cat_dir):
        for i, name in enumerate(file_names):
            if name.endswith('.json'):
                printer.line_comment("Generate graph from json file: " + name)
                api_names, class_names, start_times, end_times = \
                    classifier.get_api_data(dir_path + name)
                plotter.plots(grap_dir + name, api_names, start_times, end_times)


if __name__ == "__main__":
    sys.exit(main())
