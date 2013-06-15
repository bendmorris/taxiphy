import urllib2
import Bio.Phylo as bp
from Bio.Phylo import BaseTree
import os
import zipfile
from taxonomy import Taxonomy


class Gbif(Taxonomy):
    name = 'gbif'
    
    def main(self, tree_filename, tree_format='newick'):
        col_delimiter = '\t'
        url = 'http://ecat-dev.gbif.org/repository/export/checklist1.zip'
        
        # download the taxonomy archive
        self.download_file(url)
        
        # extract the tables
        for extract in ('taxon.txt',):
            if os.path.exists(os.path.join(self.data_dir, extract)):
                print 'Using existing copy of %s' % extract
            else:
                print 'Extracting %s from %s...' % (extract, filename)
                archive = tarfile.open(name=filename, mode='r:gz')
                full_extract = [x for x in archive.getnames() if x.split('/')[-1] == extract][0]
                member = archive.getmember(full_extract)
                member.name = extract
                archive.extract(extract, path=self.data_dir)
                archive.close()

        # get names for all ITIS TSNs from longnames table
        print 'Reading taxonomy...'
        nodes = {}
        with open(os.path.join(self.data_dir, 'taxon.txt')) as taxonomy_file:
            for line in taxonomy_file:
                line = line.strip()
                values = line.split(col_delimiter)
                id, parent_id, syn_id, _, name, _, status = values[:7]
                
                # skip incertae sedis taxa
                if id == '0': continue
                
                if syn_id and not 'synonym' in status:
                    continue
                elif syn_id and 'synonym' in status:
                    if tree_format == 'cdao':
                        nodes[id] = ('synonym', name, syn_id)
                elif not syn_id:
                    nodes[id] = BaseTree.Clade(name=name)
                    nodes[id].parent_id = parent_id
        
        print 'Found %s OTUs.' % len(nodes)
        nodes[''] = root_node = BaseTree.Clade()
        
        # create tree from nodes dictionary
        print 'Building tree...'
        for node_id, this_node in nodes.iteritems():
            if not node_id: continue
            
            if isinstance(this_node, BaseTree.Clade):
                try:
                    parent_node = nodes[this_node.parent_id]
                    parent_node.clades.append(this_node)
                    del this_node.parent_id
                except (KeyError, AttributeError): pass
                
            elif this_node[0] == 'synonym':
                _, name, syn_id = this_node
                try:
                    accepted_node = nodes[syn_id]
                except KeyError: continue
                
                if not isinstance(accepted_node, BaseTree.Clade): continue
                
                if not hasattr(accepted_node, 'tu_attributes'):
                    nodes[syn_id].tu_attributes = []
                nodes[syn_id].tu_attributes.append(('<http://www.w3.org/2000/01/rdf-schema#label>', repr(name)))
                print 'Synonym: %s -> %s' % (name, nodes[syn_id].name)
        
        tree = BaseTree.Tree(root=root_node)
        
        # write tree to file
        print 'Writing %s tree to %s...' % (tree_format, tree_filename)
        bp.write([tree], tree_filename, tree_format)
        
        print 'Done!'''
