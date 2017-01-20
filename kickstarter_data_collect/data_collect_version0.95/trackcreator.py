#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by Lin Lu 2016
#-----------------------------------------------------------------------------------------------
'''
this code is for my dissertation.


@author: Lin Lu(sn0wfree)
@version：1.0

'''
__version__='0.1'
__author__='sn0wfree'
#-----------------------------------------------------------------------------------------------
###
from plan import *
import plan

def creator_another_related_project_seek_process(url,creator_has_built_projects_number,creator_bio_info_url):
    root_url = 'https://www.kickstarter.com'
    if '/creator_bio' in creator_bio_info_url:
        if 'First' in creator_has_built_projects_number:
            creator_another_related_project_urls=[]
        elif creator_has_built_projects_number == 1:
            creator_another_related_project_urls=[]
        else:
            creator_bio_created_url = creator_bio_info_url
            try:
                #response = Request(creator_bio_created_url)
                content = urllib2.urlopen(creator_bio_created_url).read()
                sel= etree.HTML(content)
            except:
                'meet error'
                creator_created_project_list=''
            else:
                creator_info_status_list=sel.xpath('//*[@class="creator-bio-details col col-4 pt2 pb6"]//*[@class="created-projects py1 h5 mb2"]//*/@href')
                for url in creator_info_status_list:
                    if 'created' in url:
                        creator_created_project_list=root_url+url
                    if 'backed' in url:
                        creator_backed_project_list=root_url+url
            try:
                someurls=creator_created_project_list
                content = urllib2.urlopen(someurls).read()
                sel= etree.HTML(content)
            except:
                'meet error'
                creator_another_related_project_urls=[]
                pass
            else:
                possible_urls = sel.xpath('//*[@class="project-card-list NS_user__projects_list list ratio-16-9"]/li[*]//*[@class="project-thumbnail-wrap"]/@href')
                possible_urls=list(set(possible_urls))
                creator_another_related_project_urls=[]
                for url in possible_urls:
                    if '?ref=users' in url:
                        creator_another_related_project_urls.append(url)
    else:
        try:
            #response = Request(creator_bio_created_url)
            content = urllib2.urlopen(url).read()
            sel= etree.HTML(content)
        except:
            'meet error'
            creator_created_project_list=''
        else:
            #successful
            creator_bio_info_shorturl_list = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[*]/div[2]/div[1]/div/div[2]/div[1]/a//@href')
            #failed
            creator_bio_info_shorturl_list = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/p/a[1]//@href')
#//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div/div[1]/div/div/a[1]/text()







    return creator_another_related_project_urls



if __name__=='__main__':

    if plan.__version__=='2.3.3.2':
