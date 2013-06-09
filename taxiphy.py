#!/usb/bin/env python
import itis_taxonomy
import ncbi_taxonomy
import argparse
import Bio.Phylo as bp
taxonomies = {
              'itis': itis_taxonomy, 
              'ncbi': ncbi_taxonomy,
              }

parser = argparse.ArgumentParser()
parser.add_argument('taxonomy', help='name of taxonomy to download (%s)' % 
                    ', '.join(sorted(taxonomies.keys())))
parser.add_argument('filename', help='file to save tree')
parser.add_argument('format', help='tree format (%s)' %
                    ', '.join(sorted(bp._io.supported_formats.keys())),
                    nargs='?', default='newick')

args = parser.parse_args()

main = taxonomies[args.taxonomy].main
main(args.filename, tree_format=args.format)
