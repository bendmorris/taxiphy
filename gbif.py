import urllib2
import Bio.Phylo as bp
from Bio.Phylo import BaseTree
import os
import zipfile
from taxiphy_common import *
import sys
reload(sys)
sys.setdefaultencoding('latin1')


def main(tree_filename, tree_format='newick'):
    col_delimiter = '\t'
    url = 'http://ecat-dev.gbif.org/repository/export/checklist1.zip'
    data_dir = 'data/gbif/'

    if not os.path.exists(data_dir): os.makedirs(data_dir)

    # download the taxonomy archive
    download_file(data_dir, url)

    # extract the tables
    for extract in ('taxon.txt',):
        if os.path.exists(os.path.join(data_dir, extract)):
            print 'Using existing copy of %s' % extract
        else:
            print 'Extracting %s from %s...' % (extract, filename)
            archive = tarfile.open(name=filename, mode='r:gz')
            full_extract = [x for x in archive.getnames() if x.split('/')[-1] == extract][0]
            member = archive.getmember(full_extract)
            member.name = extract
            archive.extract(extract, path=data_dir)
            archive.close()

    # get names for all ITIS TSNs from longnames table
    print 'Reading taxonomy...'
    nodes = {}
    with open(os.path.join(data_dir, 'taxon.txt')) as taxonomy_file:
        for line in taxonomy_file:
            line = line.strip()
            values = line.split(col_delimiter)
            id, parent_id, _, _, name, _, status = values[:7]
            if status != 'accepted': continue
            
            nodes[id] = BaseTree.Clade(name=name)
            nodes[id].parent_id = parent_id
    
    print 'Found %s OTUs.' % len(nodes)
    nodes[''] = root_node = BaseTree.Clade()
    
    # create tree from nodes dictionary
    print 'Building tree...'
    for node_id, this_node in nodes.iteritems():
        if not node_id: continue
        try:
            parent_node = nodes[this_node.parent_id]
            parent_node.clades.append(this_node)
            del this_node.parent_id
        except KeyError: pass
    
    tree = BaseTree.Tree(root=root_node)
    
    # write tree to file
    print 'Writing %s tree to %s...' % (tree_format, tree_filename)
    bp.write([tree], tree_filename, tree_format)
    
    print 'Done!'''
