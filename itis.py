import urllib2
import Bio.Phylo as bp
from Bio.Phylo import Newick
import os
import tarfile


def main(tree_filename, tree_format='newick'):
    col_delimiter = '|'
    url = 'http://www.itis.gov/downloads/itisMySQLTables.tar.gz'
    data_dir = 'data/'

    if not os.path.exists(data_dir): os.mkdir(data_dir)

    # download the taxonomy archive
    filename = os.path.join(data_dir, url.split('/')[-1])
    if os.path.exists(filename):
        print 'Using existing copy of %s' % filename
    else:
        print 'Downloading %s...' % filename
        r = urllib2.urlopen(urllib2.Request(url))
        assert r.geturl() == url
        with open(filename, 'wb') as output_file:
            output_file.write(r.read())
        r.close()

    # extract the tables
    for extract in ('taxonomic_units', 'longnames'):
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
    print 'Getting names...'
    names = {}
    with open(os.path.join(data_dir, 'longnames')) as names_file:
        for line in names_file:
            line = line.strip()
            values = line.split(col_delimiter)
            tax_id, name = values
            names[tax_id] = name

    # read all node info from taxonomic_units
    print 'Reading taxonomy...'
    nodes = {}
    with open(os.path.join(data_dir, 'taxonomic_units')) as nodes_file:
        for line in nodes_file:
            line = line.strip()
            values = line.split(col_delimiter)
            
            (tax_id, usage, parent_id,
                uncertain_parent) = [values[n] for n in (0, 10, 17, 23)]
            
            #if uncertain_parent: continue
            if not usage in ('accepted', 'valid'): continue
            
            name = names[tax_id]
            this_node = Newick.Clade(name=name)
            nodes[tax_id] = this_node
            this_node.parent = parent_id
            
    nodes['0'] = root_node = Newick.Clade()

    # create tree from nodes dictionary
    print 'Building tree...'
    for node_id, this_node in nodes.iteritems():
        if node_id == '0': continue
        
        try:
            parent_node = nodes[this_node.parent]
            parent_node.clades.append(this_node)

        except KeyError: pass
        
        del this_node.parent

    tree = Newick.Tree(root=root_node)

    # write tree to file
    print 'Writing %s tree to %s...' % (tree_format, tree_filename)
    bp.write([tree], tree_filename, tree_format)

    print 'Done!'''
