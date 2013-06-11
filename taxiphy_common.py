def download_file(data_dir, url):
    filename = os.path.join(data_dir, url.split('/')[-1])
    
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
