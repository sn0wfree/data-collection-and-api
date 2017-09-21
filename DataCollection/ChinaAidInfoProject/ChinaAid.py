import requests
import requests_cache
import re

import pandas as pd


class APIrequestData():

    def __init__(self):
        self.param_default = ['donor', 'status', 'intent', 'year', 'crs_sector_name',
                              'flow_class', 'recipient_name', 'recipient_iso2', 'recipient_iso3']

    def requestbyapi(self, param='Default'):
        if param == 'Default':
            self.req = requests.get(
                'http://china.aiddata.org/aggregates/projects?get=%s' % (','.join(self.param_default)))
        else:
            self.req = requests.get(
                'http://china.aiddata.org/aggregates/projects?get=%s' % (','.join(param)))

        self.text = self.req.text
        # print ','.join(param)

    def Store(self):

        self.dataframe = pd.DataFrame(
            eval(self.text.replace('null', '"NULL"')))

        self.dataframe.to_hdf('ChinaAid.h5', 'ChinaAid',
                              complevel=9, complib='blosc')
        #

if __name__ == '__main__':
    requests_cache.install_cache(
        cache_name="ChinaAidProjectInfo", backend="sqlite", expire_date=300)

    max_project_id = 2521
    urlpath = 'http://china.aiddata.org/projects/'

    for ident in xrange(max_project_id):
        pass

    rr = requests.get(urlpath + str(2000))
    # print rr.text

    target = r'<h1 class="project-header page-header">'

    print re.search(target, rr.text, re.M | re.I)
