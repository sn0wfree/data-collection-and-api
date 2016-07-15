#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by Lin Lu 2016
#-----------------------------------------------------------------------------------------------
'''
this code is for my dissertation.
'''
#-----------------------------------------------------------------------------------------------
###
import multiprocessing as mp
import sys
import funcforkick
import time
import pandas as pd
import numpy as np
import threading
import Queue
import gc
import pp

def createurl(target_url_file,have_collected_url):
    url_list =funcforkick.read_url_file(target_url_file)
    collected_unclear=funcforkick.read_url_file(have_collected_url)
    collected=list(set(collected_unclear))
    file_lsit=list(set(url_list)-set(collected))
    file = list(set(file_lsit))
    return file,collected

def filepathcollection(a):
    publicpath='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/middle60project/split'
    rewards_backers_distribution= publicpath+'/url%d/rewards_backers_distribution.csv'%a
    rewards_pledge_limit= publicpath+'/url%d/rewards_pledge_limit.csv'%a
    rewards_pledged_amount= publicpath+'/url%d/rewards_pledged_amount.csv'%a
        #item_collect='/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/middle60project/slpit/item.txt'
    #rewards_collect=publicpath+'/url%srewards.txt'
    saving_file = publicpath+'/url%d/project_data.csv'%a
        #index_value20='/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/test/index_value.txt',
        #index_keys20='/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/test/index_keys.txt'
    target_url_file= publicpath+'/url%d/url%d.txt'%(a,a)
    have_collected_url= publicpath+'/url%d/collected.txt'%a
    return rewards_backers_distribution,rewards_pledge_limit,rewards_pledged_amount,saving_file,target_url_file,have_collected_url



a=input('the beginning collecting subjob is from ath :')
b=input('the gap for I/O is:')
c=input('the subjob will end at Job?( max 112):')
y=input('choose the number of worker for this jobs:')
(rewards_backers_distribution,rewards_pledge_limit,rewards_pledged_amount,saving_file,target_url_file,have_collected_url) = filepathcollection(a)
(file,collected) = createurl(target_url_file,have_collected_url)
gc.enable()

global counts
counts = 0
#setup multicore system
#job_server = pp.Server()
#print 'begin to create/read index file'
def datacollectprocess(someurl):
    global total_item
    global total_rewards_backers_distribution
    global total_rewards_pledge_limit
    global total_rewards_pledged_amount
    global collected
    global counts
    global rewards_headers
    global item_headers
    f1 = time.time()
    if someurl !='':
        (id,state,sel,the_page1) = funcforkick.compareindexprocess(someurl)
        item={}
        rewards={}
        (item,rewards,ID,state)= funcforkick.datagenerateprocess(someurl,state,sel,the_page1)
        (total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)=funcforkick.savingcsvforalltaskprocess(rewards,item,total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)
        counts = counts + 1
        if item!={}:
            collected.append(someurl)
    if len(total_item)>50:
            #print rewards_backers_distribution
            #print rewards_pledge_limit,rewards_pledged_amount
            #print
        funcforkick.collected_list_overwrite(collected,have_collected_url)
            #funcforkick.projetcdata_txt_wholewrite(item,item_collect)
            #funcforkick.projetcdata_txt_wholewrite(rewards,rewards_collect)
            #funcforkick.index_write(index,'/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/test/index_value.txt','/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/test/index_keys.txt')
        funcforkick.writeacsvprocess(saving_file,item_headers,total_item)
        funcforkick.writeacsvprocess(rewards_backers_distribution,rewards_headers,total_rewards_backers_distribution)
        funcforkick.writeacsvprocess(rewards_pledge_limit,rewards_headers,total_rewards_pledge_limit)
        funcforkick.writeacsvprocess(rewards_pledged_amount,rewards_headers,total_rewards_pledged_amount)
            #reset list
        total_item=[]
        total_rewards_backers_distribution=[]
        total_rewards_pledge_limit=[]
        total_rewards_pledged_amount=[]
        gc.collect()
        time.sleep(0.5)
            #time.sleep(1)
    f2 = time.time()
    w=(len(file)-counts)*(f2-f1)/60/y
            #conditional_insert(cursor, item)
    sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects and remaining time: %.4f mins" % (counts,f2-f1,w))
    #sys.stdout.write("\rthis spider has already read %d projects" % (counts))
    sys.stdout.flush()


#for e in xrange(a,c):
    #print '\n   subjobs %s begin!'%e
print 'begin to collecting data'
#ppservers = ()

total_item=[]
total_rewards_backers_distribution=[]
total_rewards_pledge_limit=[]
total_rewards_pledged_amount=[]

#if len(sys.argv) > 1:
#    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
#    job_server = pp.Server(ncpus, ppservers=ppservers)
#else:
    # Creates jobserver with automatically detected number of workers
#    job_server = pp.Server(ppservers=ppservers)




queue = Queue.Queue()
class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            (target) = self.queue.get()
            global collected
            (rewards_backers_distribution,rewards_pledge_limit,rewards_pledged_amount,saving_file,target_url_file,have_collected_url) = filepathcollection(e)
            datacollectprocess(target)
            #time.sleep(1/10)
            self.queue.task_done()



def main(file,y):

    for j in xrange(y):
        t = ThreadClass(queue)
        t.setDaemon(True)
        t.start()
    for someurl in file:

        queue.put(someurl)
    queue.join()


for e in xrange(a,c):
    print '\nsubjobs %s begin!'%e
    rewards_headers=['Project_ID','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89']
    item_headers = ['Project_ID','project_name','Goal','url',
                  'pledged_amount','backers_count','creator_full_name',
                  'creator_personal_url','creator_buildhistory_has_backed_projects_number','creator_built_projects_number',
                  'creator_bio_info_url','creator_Facebook_url','currency','duration','location_ID','state_changed_at','created_at','Deadline','description','category','project_state','has_a_video','comments_count','updates_number','data_percent_rasied','hours_left','creator_short_name','creator_friends_facebook_number']
    (rewards_backers_distribution,rewards_pledge_limit,rewards_pledged_amount,saving_file,target_url_file,have_collected_url) = filepathcollection(e)
    (file,collected) = createurl(target_url_file,have_collected_url)
    main(file,y)
    funcforkick.collected_list_overwrite(collected,have_collected_url)
    #(someurl,total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)=catchup(someurl,total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)
    funcforkick.writeacsvprocess(saving_file,item_headers,total_item)
    funcforkick.writeacsvprocess(rewards_backers_distribution,rewards_headers,total_rewards_backers_distribution)
    funcforkick.writeacsvprocess(rewards_pledge_limit,rewards_headers,total_rewards_pledge_limit)
    funcforkick.writeacsvprocess(rewards_pledged_amount,rewards_headers,total_rewards_pledged_amount)
    counts=0
    print  '\nsubjobs %s completed!'%e
    time.sleep(2)
        #reset list
        #time.sleep(1)
#funcforkick.index_write(index,index_value20,index_keys20)
print 'saving process completed'

#end = time.time()
#print end-start
