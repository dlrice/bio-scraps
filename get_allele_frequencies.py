#!/usr/bin/env python
import requests, sys


def update_progress(iteration, total, n=25):
    progress = int(n*(iteration + 1)/float(total))
    left = n - progress
    sys.stdout.write('\r[{}{}]'.format('#'*progress, ' '*left))
    sys.stdout.flush()

def get_allele_frequencies(rsids_file, population, sep='\t'):

    with open(rsids_file) as f:
        rsids = f.readlines()
    rsids = [el.strip() for el in rsids]
    nrsids = len(rsids)
    print '\nFound {} rsids in {}'.format(nrsids, rsids_file)
    print 'Using population {}'.format(population)
    print 'Using seperator [{}]'.format(sep)

    server = "http://rest.ensembl.org"
    header = None
    output = rsids_file + '.af'
    with open(output, 'w') as o:
        for i, rsid in enumerate(rsids):
            update_progress(i, nrsids)
            ext = "/variation/human/{}?pops=1".format(rsid)
            r = requests.get(server + ext, headers={ "Content-Type" : "application/json"})
            if not r.ok:
              r.raise_for_status()
              sys.exit()
            decoded = r.json()
            frequencies = filter(lambda x: x['population'] == population, decoded['populations'])
            frequencies = sorted(frequencies, key=lambda x: x['frequency'], reverse=True)
            for frequency in frequencies:
                if header is None:
                    header = sorted(frequency.keys())
                    header = ['name'] + header
                    line = sep.join(header)
                    o.write(line + '\n')
                    #print line
                frequency['name'] = decoded['name']
                line = sep.join([str(frequency[c]) for c in header])
                #print line
                o.write(line + '\n')
    print '\n\tOutput written to {}\n'.format(output)

if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) in (2, 3):
        get_allele_frequencies(*args)
    else:
        print 'Usage: get_allele_frequencies.py rsidsfile population [separator]'

