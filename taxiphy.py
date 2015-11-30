#!/usr/bin/env python
import argparse
import Bio.Phylo as bp
import sys
reload(sys)
sys.setdefaultencoding('latin1')
from itis import Itis
from ncbi import Ncbi
from gbif import Gbif
taxonomies = {
              'itis': Itis, 
              'ncbi': Ncbi,
              'gbif': Gbif,
              'ALL': None,
              }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('taxonomy', help='name of taxonomy to download (%s)' % 
                        ', '.join(sorted(taxonomies.keys())))
    parser.add_argument('-o', '--output', help='path to save tree output', 
                        nargs='?', default=None)
    parser.add_argument('-f', '--format', help='tree format (%s)' %
                        ', '.join(sorted(bp._io.supported_formats.keys())),
                        nargs='?', default='newick')
    parser.add_argument('-i', '--id', help='Use NCBI ids as label',
                    action='store_true')

    args = parser.parse_args()

    if args.taxonomy == 'ALL':
        classes = [x for x in taxonomies.values() if not x is None]
        args.filename = None
    else:
        classes = [taxonomies[args.taxonomy]]
        
    for c in classes:
        taxonomy = c()
        print '** %s **' % taxonomy.name
        filename = ((args.filename if hasattr(args, 'filename') else None) 
                    or ('%s_taxonomy.%s' % (taxonomy.name, args.format)))
        taxonomy.main(filename, tree_format=args.format, ids=args.id)
        
if __name__ == '__main__':
    main()
