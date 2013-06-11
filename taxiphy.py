#!/usb/bin/env python
import itis
import ncbi
import argparse
import Bio.Phylo as bp
taxonomies = {
              'itis': itis, 
              'ncbi': ncbi,
              }

parser = argparse.ArgumentParser()
parser.add_argument('taxonomy', help='name of taxonomy to download (%s)' % 
                    ', '.join(sorted(taxonomies.keys())))
parser.add_argument('filename', help='file to save tree', 
                    nargs='?', default=None)
parser.add_argument('format', help='tree format (%s)' %
                    ', '.join(sorted(bp._io.supported_formats.keys())),
                    nargs='?', default='newick')

args = parser.parse_args()
if args.filename is None:
    args.filename = args.taxonomy + '_taxonomy.new'

main = taxonomies[args.taxonomy].main
main(args.filename, tree_format=args.format)
