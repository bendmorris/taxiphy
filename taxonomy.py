import os
import urllib2


class Taxonomy:
    def get_data_dir(self):
        return os.path.join('data', self.name)
    data_dir = property(get_data_dir)
    
    def __init__(self):
        if not os.path.exists(self.data_dir): os.makedirs(self.data_dir)
    
    def download_file(self, url):
        filename = os.path.join(self.data_dir, url.split('/')[-1])
        
        if os.path.exists(filename):
            print 'Using existing copy of %s' % filename
        else:
            print 'Downloading %s...' % filename
            r = urllib2.urlopen(urllib2.Request(url))
            assert r.geturl() == url
            with open(filename, 'wb') as output_file:
                data = True
                while data:
                    data = r.read(1024)
                    if data: output_file.write(data)
            r.close()
            
        return filename

    @classmethod
    def format_rdf_string(cls, x):
        return '"%s"' % x.replace('"', '\\"')