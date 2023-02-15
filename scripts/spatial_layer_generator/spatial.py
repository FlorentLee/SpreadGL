import argparse
from spatial_layer_generator.continuous_space_processor import *
from spatial_layer_generator.discrete_space_processor import *


def main():
    welcome = "Welcome to the spatial layer generator! You can create a spatial layer for a phylogenetic tree to display in Spread.gl."
    parser = argparse.ArgumentParser(description=welcome)
    parser.add_argument('--tree', '-t', required=True,
                        help='Specify the file name of your phylogenetic tree with filename extension.')
    parser.add_argument('--location', '-l', required=True,
                        help='Type in the annotation that stores the location information or coordinates. '
                             'Or type in the two annotations storing latitude and longitude (in this order) with a comma separator.')
    parser.add_argument('--list', '-li',
                        help='Optional, only mandatory in the case of discrete space. '
                             'Specify the file name of your list of coordinates with filename extension. '
                             'This file should be in the csv format with a comma (",") separator, '
                             'and should be comprised of three columns with a specific header of "location,latitude,longitude".')
    parser.add_argument('--format', '-f',  choices=['csv'],
                        help='Optional: Type in "csv" if you would like to inspect your output file in a tabular format.')

    args = parser.parse_args()
    tree = str(args.tree)
    location = str(args.location).split(',')
    location_list = str(args.list)
    extension = str(args.format)

    if location_list == 'None':
        process_continuous_phylogeography(tree, location, extension)
    else:
        process_discrete_phylogeography(tree, location, location_list, extension)


# Run with command line arguments precisely when called directly
# (rather than when imported)
if __name__ == '__main__':
    main()
