import urllib2
import Bio.Phylo as bp
from Bio.Phylo import BaseTree
import os
import tarfile
from taxonomy import Taxonomy


class Itis(Taxonomy):
    name = 'itis'
    
    def main(self, tree_filename, tree_format='newick'):
        col_delimiter = '|'
        url = 'http://www.itis.gov/downloads/itisMySQLTables.tar.gz'
        
        # download the taxonomy archive
        self.download_file(url)
        
        # extract the tables
        for extract in ('taxonomic_units', 'longnames', 'synonym_links'):
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
        print 'Getting names...'
        names = {}
        with open(os.path.join(self.data_dir, 'longnames')) as names_file:
            for line in names_file:
                line = line.strip()
                values = line.split(col_delimiter)
                tax_id, name = values
                names[tax_id] = name
        
        # read all node info from taxonomic_units
        # TODO: synonyms: get (bad_id, good_id) from synonym_links
        print 'Reading taxonomy...'
        nodes = {}
        with open(os.path.join(self.data_dir, 'taxonomic_units')) as nodes_file:
            for line in nodes_file:
                line = line.strip()
                values = line.split(col_delimiter)
                
                (tax_id, usage, parent_id,
                    uncertain_parent) = [values[n] for n in (0, 10, 17, 23)]
                
                #if uncertain_parent: continue
                if not usage in ('accepted', 'valid'): continue
                
                name = names[tax_id]
                this_node = BaseTree.Clade(name=name)
                nodes[tax_id] = this_node
                this_node.parent_id = parent_id
                
        if tree_format == 'cdao':
            # get synonym definitions
            with open(os.path.join(self.data_dir, 'synonym_links')) as synonym_file:
                for line in synonym_file:
                    line = line.strip()
                    values = line.split(col_delimiter)
                    node_id, syn_id, _ = values
                    nodes[node_id] = ('synonym', syn_id, names[node_id])
                
        print 'Found %s OTUs.' % len(nodes)
        nodes['0'] = root_node = BaseTree.Clade()
        
        # create tree from nodes dictionary
        print 'Building tree...'
        for node_id, this_node in nodes.iteritems():
            if node_id == '0': continue
            
            if isinstance(this_node, BaseTree.Clade):
                try:
                    parent_node = nodes[this_node.parent_id]
                    parent_node.clades.append(this_node)
            
                except KeyError: pass
                
                del this_node.parent_id
                
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
