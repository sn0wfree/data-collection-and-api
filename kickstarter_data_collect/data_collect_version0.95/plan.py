#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by Lin Lu 2016
#-----------------------------------------------------------------------------------------------
'''
this code is for my dissertation.

'''
#version control


__author__='sn0wfree'
__version__='2.3.3.3'



#-----------------------------------------------------------------------------------------------
###

import multiprocessing as mp
import sys
import zipfile
import datetime
import time
import threading
import Queue
import gc
from urllib2 import Request, urlopen, URLError
import urllib2
import requests
from lxml import etree
import pickle
import os
import unicodecsv
import csv
import smtplib
import mimetypes
import email.mime.text
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email import encoders
from email.utils import parseaddr, formataddr
from email.header import Header
from email.Encoders import encode_base64
from email.utils import COMMASPACE
import pandas as pd
import celery





#someurl='https://www.kickstarter.com/projects/399230478/the-horror-of-loon-lake-revealed?ref=category_newest'
def conn_try_again(max_retries=5,default_retry_delay=1):
    def _conn_try_again(function):
        RETRIES = 0
        #重试的次数
        count = {"num": RETRIES}
        def wrapped(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception, err:
                if count['num'] < max_retries:
                    time.sleep(default_retry_delay)
                    count['num'] += 1
                    return wrapped(*args, **kwargs)
                else:
                    status='Error'
                    sel='Error'
                    raise Exception(err)
        return wrapped
    return _conn_try_again

def chunks(item,n):
    lenitem=len(item)
    dic={}
    #split item by n
    for i in xrange(0,lenitem,n):
        if i+n < lenitem:
            dic[i]=item[i:i+n]
        else:
            dic[i]=item[i:]
    return dic


def deco(arg):
    def _deco(func):
        def __deco():
            print("before %s called [%s]." % (func.__name__, arg))
            func()
            print("  after %s called [%s]." % (func.__name__, arg))
        return __deco
    return _deco

@conn_try_again(max_retries=5,default_retry_delay=1)
def pre_update_request_url_process(someurls):

    try:
        content = urllib2.urlopen(someurls).read()
        sel= etree.HTML(content)
        status='Good'

        ##this is for some data without tab.
    except URLError as e:
        if hasattr(e, 'reason'):
            status='Error'
            sel='Error'
            #print 'We failed to reach a server.'
            #print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            status='Error'
            sel='Error'
            #print 'The server couldn\'t fulfill the request.'
            #print 'Error code: ', e.code
        #raise self.retry(exc=e,countdown=1)
    finally:
        return status,sel

#compress process suite
def zipafilefordelivery(file,target):
    with zipfile.ZipFile(file, 'w',zipfile.ZIP_DEFLATED) as z:
        z.write(target)
        z.close
#------------------------------------------------------------------------------
# read or write process suite
def readacsv(file):
    with open(file,'r+') as f:
        w=pd.read_csv(file,skip_footer=1,engine='python')
    return w

def read_url_file(file):
    with open (file,'r') as file_unclear_file:
        file_unclear = []
        file_unclear_list =file_unclear_file.readlines()
        for x in file_unclear_list:
            a=x.split()
            if a!=[]:
                file_unclear.append(a[0])
            else:
                pass
            #print x
            #file_unclear.appen(x)
        return file_unclear

def projetcdata_txt_wholewrite(item,file):
    f= open(file,'a')
    f.write(str(item))
    f.close()


def collected_list_overwrite(item,file):
    f = open (file,'w')
    lenitem=len(item)
    for i in xrange(0,lenitem):
        f.write(item[i]+'\n')
    f.close()

def writeacsvprocess(file,headers,item):
    with open(file,'r+') as project_data:
        project_data_read_csv = unicodecsv.reader(project_data,headers)
        if not headers in project_data_read_csv:
            status=0
        else:
            status=1
    with open(file,'a') as project_data:
        project_data_csv = unicodecsv.DictWriter(project_data,headers)
        if status ==0:
            project_data_csv.writeheader()
        project_data_csv.writerows(item)

def savingcsvforalltaskprocess(rewards,item,total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount):
    if item !={}:
        total_item.append(item)

        (rewards_backers_distribution_dict,rewards_pledge_limit_dict,rewards_pledged_amount_dict)=rewardsseperategenerateprocess(rewards)
        total_rewards_backers_distribution.append(rewards_backers_distribution_dict)
        total_rewards_pledge_limit.append(rewards_pledge_limit_dict)
        total_rewards_pledged_amount.append(rewards_pledged_amount_dict)


    return total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount
    #print list(rewards)
#--------------------------------------------------------------------
#optimal process
def datacollectprocess(someurl,file1):
    global total_item
    global total_rewards_backers_distribution
    global total_rewards_pledge_limit
    global total_rewards_pledged_amount
    global collected

    global counts
    global rewards_headers
    global item_headers
    global rewards_backers_distribution
    global rewards_pledge_limit
    global rewards_pledged_amount
    global saving_file
    f1 = time.time()
    if someurl !=''and someurl!='\n':
        (id,state,sel,the_page1) = compareindexprocess(someurl)
        item={}
        rewards={}
        (item,rewards,ID,state)= datagenerateprocess(someurl,state,sel,the_page1)
        (total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)=savingcsvforalltaskprocess(rewards,item,total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)
        counts = counts + 1
        if item!={}:
            collected.append(someurl)
        time.sleep(1+len(total_item)*y/500)
    if len(total_item)>50:
            #print rewards_backers_distribution
            #print rewards_pledge_limit,rewards_pledged_amount
            #print
        collected_list_overwrite(collected,have_collected_url)
            #projetcdata_txt_wholewrite(item,item_collect)
            #projetcdata_txt_wholewrite(rewards,rewards_collect)
        writeacsvprocess(saving_file,item_headers,total_item)
        writeacsvprocess(rewards_backers_distribution,rewards_headers,total_rewards_backers_distribution)
        writeacsvprocess(rewards_pledge_limit,rewards_headers,total_rewards_pledge_limit)
        writeacsvprocess(rewards_pledged_amount,rewards_headers,total_rewards_pledged_amount)
            #reset list
        total_item=[]
        total_rewards_backers_distribution=[]
        total_rewards_pledge_limit=[]
        total_rewards_pledged_amount=[]
        gc.collect()
        time.sleep(1)
            #time.sleep(1)
    f2 = time.time()
    w=(len(file1)-counts)*(f2-f1)/y
    progress_test(counts,len(file1),f2-f1,w)
            #conditional_insert(cursor, item)
    #sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects and remaining time: %.4f mins" % (counts,f2-f1,w))
    #sys.stdout.write("\rthis spider has already read %d projects" % (counts))
    #sys.stdout.flush()

def rewardsseperategenerateprocess(rewards):
    rewards_backers_distribution_dict={}
    rewards_pledge_limit_dict={}
    rewards_pledged_amount_dict={}
    if rewards!={}:
        rewards_backers_distribution = rewards['rewards_backers_level_distribution']
        rewards_pledge_limit =rewards['pledge_limit']
        rewards_pledged_amount = rewards['rewards_level_divided_by_goal']
        lenrewards_backers_distribution=len(rewards_backers_distribution)
        rewards_backers_distribution_dict['Project_ID']=rewards['Project_ID']
        rewards_pledge_limit_dict['Project_ID']=rewards['Project_ID']
        rewards_pledged_amount_dict['Project_ID']=rewards['Project_ID']
        if lenrewards_backers_distribution<50:
            for i in xrange(lenrewards_backers_distribution):
                if i<len(rewards_backers_distribution):
                    rewards_backers_distribution_dict['%s' %i]=rewards_backers_distribution[i]
                else:
                    rewards_backers_distribution_dict['%s' %i]='0'
                if i<len(rewards_pledge_limit):
                    rewards_pledge_limit_dict['%s' %i]=rewards_pledge_limit[i]
                else:
                    rewards_pledge_limit_dict['%s' %i]='0'
                if i<len(rewards_pledged_amount):
                    rewards_pledged_amount_dict['%s' %i]=rewards_pledged_amount[i]
                else:
                    rewards_pledged_amount_dict['%s' %i]='0'
        else:
            rewards_pledged_amount_dict={}
            rewards_pledge_limit_dict={}
            rewards_backers_distribution_dict={}




    return rewards_backers_distribution_dict,rewards_pledge_limit_dict,rewards_pledged_amount_dict

def datagenerateprocess(url,state,sel,the_page1):
    someurl=''.join(url.split())
    if state != 'Error':
        if state == 'live':
            (item,rewards,ID,state)=webscraper_live(someurl,sel,the_page1)
        else:
            if state == 'successful':
                (item,rewards,ID,state) = webscraper_successed(someurl,sel,the_page1)
            else:
                (item,rewards,ID,state)= webscraper_failorcanceled(someurl,sel,the_page1)
    else:
        #print 'url is empty'
        item ={}
        rewards={}
        ID=0
        state='Error'
    return item,rewards,ID,state

def compareindexprocess(url):

    if url!=[] and type(url)!=float:
        someurl =''.join(url.split())
    else:
        someurl='Error'
    try:
        response = Request(someurl)
        content = urllib2.urlopen(someurl).read()
        sel= etree.HTML(content)
        req = urlopen(response)
        the_page1 = req.readlines()
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            state='Error'
            exist_code=0
            ID=0
            sel=0
            the_page1=0

        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            state='Error'
            exist_code=0
            ID=0
            sel=0
            the_page1=0
        else:
            state='Error'
            exist_code=0
            ID=0
            sel=0
            the_page1=0

    else:
        ID=0
        if len(sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/@data-project-state'))!=0:
            state = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/@data-project-state')[0]
        else:
            state = 'Error'
        for line in the_page1:
            if 'data'  in line:
                words = line.split('" ')
                for word in words:
                    if 'data class="Project' in word:
                        project_ID_str = word.split('Project')[1]
                        ID= ''.join(project_ID_str)

    return ID,state,sel,the_page1

def creator_another_related_project_seek_process(creator_has_built_projects_number,creator_bio_info_url,creator_bio_info_url_sel):
    root_url = 'https://www.kickstarter.com'
    if 'First' in creator_has_built_projects_number:
        creator_another_related_project_urls=[]
    else:
        creator_created_project_list_lastpart=creator_bio_info_url_sel.xpath('//*[@id="bio"]/div/div[2]/div[4]/a[1]/@href')
        creator_created_project_list=root_url+creator_created_project_list_lastpart
        try:
            someurls=creator_created_project_list
            response = Request(someurls)
            content = urllib2.urlopen(someurls).read()
            sel= etree.HTML(content)
              ##this is for some data without tab.
            req = urlopen(response)
            the_page1 = req.readlines()
        except:
            'meet error'
            pass
            creator_another_related_project_urls=[]
        else:
            possible_urls = sel.xpath('//*[@id="main"]/div/ol/li[*]/div/div[*]//@href')
            possible_urls=list(set(possible_urls))
            creator_another_related_project_urls=[]
            for url in possible_urls:
                if '?ref=users' in url:
                    creator_another_related_project_urls.append(url)
    return creator_another_related_project_urls



                                #sel.xpath('//*[@id="bio"]/div/div[2]/div[4]/text()[1]')'
#/profile/mogeesplay/created
#---------------------------------------------------------------------
def justajoke(mail):
    for x in xrange(0,10000):
        dash_r='/'*random.randint(1,1000)
        star_r='*'*random.randint(1,1000)
        wave_r='~'*random.randint(1,1000)
        point_r='.'*random.randint(1,1000)
        bracks_r='()'*random.randint(1,1000)
        A_r='A'*random.randint(1,1000)
        question_r='?'*random.randint(1,1000)
        strrr=dash_r+star_r+wave_r+point_r+bracks_r+A_r+question_r
        symbol=list(strrr)[random.randint(1,len(strrr)-1)]
        for j in xrange(0,10000):
            symbol+=list(strrr)[random.randint(1,len(strrr)-1)]
        sys.stdout.write('/r %s'%symbol)
        sys.stdout.flush()
#main collection process
def webscraper_successed(someurl,a,the_page):
    root_url = 'https://www.kickstarter.com'
    try:
        aasd = someurl.rstrip("ref=category_newest")
        someurls= aasd.rstrip('?')+'/description'
            #print someurls
        response = Request(someurls)
        content = urllib2.urlopen(someurls).read()
        sel= etree.HTML(content)
          ##this is for some data without tab.
        req = urlopen(response)
        the_page1 = req.readlines()
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            item={'Project_ID':0,'project_state':'Error'}
            rewards={}
            ID=0
            state='Error'
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            item={'Project_ID':0,'project_state':'Error'}
            rewards={}
            ID=0
            state='Error'
    else:
        project_name_str = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div[1]/h2/span/a/text()')
        project_name = ''.join(project_name_str).strip('\n')
        for line in the_page1:
            #project_ID_str
            if 'data'  in line:
                words = line.split('" ')
                for word in words:
                    if 'data class="Project' in word:
                        project_ID_str = word.split('Project')[1]
            #created_at/setupdate
            if 'created_at&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'created_at' in word:
                        created_at_str = word.split('&quot;:')[1]
            #state_changed_at
            if 'state_changed_at&quot' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'state_changed_at' in word:
                        state_changed_at_str= word.split('&quot;:')[1]
            if 'launched_at&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'launched_at&quot;:' in word:
                        launched_at_str= word.split('&quot;:')[1]
            #deadline_quot
            if '&quot;deadline&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'deadline&quot;:' in word:
                        deadline_quot_str = word.split('&quot;:')[1]
            if '&quot;goal&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'goal&quot;:' in word:
                        goal_seek =word.split('&quot;:')[1]
        #                            //*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/a[1]/text()


        category_location_str = sel.xpath('//*[@class="NS_projects__category_location ratio-16-9"]//*/text()')
        try:
            location_id_str=category_location_str[0]
        except:
            location_id_str='Error'


        try:
            category_str=category_location_str[1]
        except:
            category_str='Error'



        #print 'location is %s ' %location_id_str
        location_id =''.join(location_id_str).strip('\n')
        category=''.join(category_str).strip('\n')


        launched_at=''.join(launched_at_str)
        project_ID = ''.join(project_ID_str)
        created_at=''.join(created_at_str)
        #category = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/a[2]/text()')
        state_changed_at=''.join(state_changed_at_str)
        deadline_quot=''.join(deadline_quot_str)
        goal=''.join(goal_seek)
        backers_count= sel.xpath('//*[@class="NS_projects__spotlight_stats"]/b/text()')[0]
        pledged_amount = sel.xpath('//*[@class="NS_projects__spotlight_stats"]/span/text()')[0]


        data_percent_rasied = sel.xpath('//*[@id="pledged"]/@data-percent-raised')
        currency = sel.xpath('//*[@id="pledged"]/data/@data-currency')
        data_pool_url = sel.xpath('//*[@id="stats"]/div/div[3]/div/div//@data-poll_url')
        video = sel.xpath('//*[@id="video-section"]/@data-has-video')
        hours_left = sel.xpath('//*[@id="project_duration_data"]//@data-hours-remaining')
        day_left = sel.xpath('//*[@id="stats"]/div/div[3]/div/div/div/text()')
        data_duration = sel.xpath('//*[@id="project_duration_data"]//@data-duration')
        updates = sel.xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[3]/span/text()')
        rewards_level_divided_by_goal = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/h2/span[1]/text()')
        rewards_level_name = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/div[1]/p/text()[1]')
        rewards_backers_level_distribution =sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/div[3]/span[@class="pledge__backer-count"]/text()')
        if data_duration == '':
            data_duration = 0
            hours_left=0
        rewards_level_description =[]
        pledge_limit = []
        #ship_location_info
        ship_location_info = ['0']*len(rewards_level_divided_by_goal)

        for i in xrange(1,len(rewards_level_divided_by_goal)):
            #print i
            c = str(i)
            #rewards_level_description
            rewards_level_description_a= '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            rewards_level_description_b = ']/div[2]/div[1]/p/text()'
            #pledge_limit for each part of pledges
            pledge_limit_a= '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            pledge_limit_b = ']/div[2]/div[3]//span[@class="pledge__limit"]/text()'
            #ship_info
            ship_location_info_a = '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            ship_location_info_b =']/div[2]/div[2]/div[2]/span[2]/text()'
            #combin the xpath for each variable
            pledge_limit_a += c
            pledge_limit_a += pledge_limit_b
            ship_location_info_a += c
            ship_location_info_a += ship_location_info_b
            rewards_level_description_a += c
            rewards_level_description_a += rewards_level_description_b
            #declare the empty list
            rewards_level_description_split_list=[]
            pledge_limit_split_list=[]
            ship_location_info_list=[]
            #split each variable
            #rewards_level_description
            rewards_level_description_split_list = sel.xpath(rewards_level_description_a)
            rewards_level_description_split = rewards_level_description_split_list
            rewards_level_description_split =''.join(rewards_level_description_split)
            rewards_level_description.append(rewards_level_description_split)
            #pledge_limit
            pledge_limit_split_list = sel.xpath(pledge_limit_a)
            pledge_limit_split = pledge_limit_split_list
            pledge_limit_split =''.join(pledge_limit_split)
            pledge_limit.append(pledge_limit_split)
            #ship_location_info
            ship_location_info_split_list = sel.xpath(ship_location_info_a)
            ship_location_info_split = ship_location_info_split_list
            #print ship_location_info_split, ship_location_info_split_list
            ship_location_info_split =''.join(ship_location_info_split)
            ship_location_info_split= str(ship_location_info_split)
            #ship_location_info[i-1] = ship_location_info_split
        deadline_xpath= sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[1]/div/div/p/time/text()')
        #project_description
        description = sel.xpath('/html/head/meta[10]/@content')
        #creator_info_hub
        #creator_short_name
        #creator_short_name = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/h5/a/text()')
        #creator_url


        #creator_bio_info
        creator_bio_info_shorturl_list = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[*]/div[2]/div[1]/div/div[2]/div[1]/a//@href')
        #                                           //*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[1]/a
        #print creator_bio_info_shorturl_list
        #                                sel.xpath('//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[1]/a/@href')
        creator_bio_info_url = root_url + ''.join(creator_bio_info_shorturl_list)
        #print creator_bio_info_url
        #turn to new creator_bio_websites
        comments_count=sel.xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[4]/@data-comments-count')

        try:
            creator_bio_info = urllib2.urlopen(creator_bio_info_url).read()
            creator_bio_info_sel= etree.HTML(creator_bio_info)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
                creator_full_name='Error'
                #creator_personal_url='Error'
                creator_Facebook_url='Error'
                creator_short_name='Error'
                creator_buildhistory_has_built_projects_number='null'
                creator_buildhistory_has_backed_projects_number='null'
                creator_friends__facebook_number = 'Error'
                creator_personal_url_s='Error'
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
                creator_full_name='Error'
                #creator_personal_url='Error'
                creator_Facebook_url='Error'
                creator_short_name='Error'
                creator_buildhistory_has_built_projects_number='null'
                creator_buildhistory_has_backed_projects_number='null'
                creator_friends__facebook_number = 'Error'
                creator_personal_url_s='Error'
        else:

            creator_full_name = creator_bio_info_sel.xpath('//*[@id="main_content"]/header/div/div/div[2]/h1/a/text()')
                    #creator_buildhistory
                    #print creator_full_name
            creator_personal_url = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[1]/div[2]/ul/li/a/@href')
                    #print ccccc
            creator_Facebook_url=creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[*]/span[2]/a/@href')
            if ''.join(creator_personal_url)=='':
                creator_personal_url_s='Error'
            else:
                creator_personal_url_s=''.join(creator_personal_url)
            creator_friends__facebook_number_potential_list = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]//text()')
            creator_friends__facebook_number_potential=[]
            #print creator_friends__facebook_number_potential_list
            for words in creator_friends__facebook_number_potential_list:
                if words !='\n' and words!='\n\n':
                    creator_friends__facebook_number_potential.append(words)
            #print creator_friends__facebook_number_potential
            if not 'Last login' in creator_friends__facebook_number_potential[0]:
                creator_short_name=creator_friends__facebook_number_potential[0]
            else:
                creator_short_name=[]
            creator_buildhistory_has_built_projects_number='null'
            creator_buildhistory_has_backed_projects_number='null'
            creator_friends__facebook_number = 'Not connected'
            for word in creator_friends__facebook_number_potential:
                if 'created' in word:
                    creator_buildhistory_has_built_projects_number=word.split('\n')
                if 'backed' in word:
                    creator_buildhistory_has_backed_projects_number=word.split('\n')
                if 'friend' in word:
                    creator_friends__facebook_number= word
                #creator_friends__facebook_number_potential=str(creator_friends__facebook_number_potential_list)
                #print creator_friends__facebook_number_potential_list,creator_friends__facebook_number_potential,type(creator_friends__facebook_number_potential)

        #new data form
        state_other=sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/@data-project-state')
        #data_structure_change
        deadline_date= ''.join(deadline_xpath)
        backers_count_str = ''.join(backers_count)
        goal_str = ''.join(goal)
        pledged_amount_str =''.join(pledged_amount)
        currency_str = ''.join(currency)
        data_percent_rasied_str = ''.join(data_percent_rasied)
        hours_left_str = ''.join(hours_left)
        item = {}

        item['project_name'] = project_name
        #item[ 'project_name']= project_name
        item[ 'location_ID']= location_id
        item[ 'Project_ID']= project_ID
        item['duration'] =data_duration
        item['has_a_video'] =''.join(video)
        #print 'Project ID', id
        state = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/@data-project-state')[0]

        #print 'Project ID', id
        if state != '':
            item[ 'project_state' ]= state
        else:
            item[ 'project_state' ]=''.join(state_other)


        #item[ 'project_state' ]=''.join(state_other)
        if ''.join(creator_short_name) == '':
            creator_short_name_s = 0
        else:
            creator_short_name_s = ''.join(creator_short_name)
        item['created_at']= created_at
        item['Deadline']=deadline_quot
        #print 'deadline_xpath', deadline_date
        item['state_changed_at']=state_changed_at
        item[ 'backers_count']= backers_count_str
        #print 'backers_count',  dics['backerscount']
        item[ 'Goal']= goal_seek
        item[ 'pledged_amount']=pledged_amount_str
        item[ 'data_percent_rasied']= 0
        item[ 'currency']= currency
        item[ 'hours_left']= 0
        #print 'day_left', day_left

        item[ 'description']=''.join(description).strip('\n')
        item[ 'creator_short_name']= creator_short_name
        item[ 'creator_personal_url']= creator_personal_url_s
        item[ 'creator_bio_info_url']=''.join(creator_bio_info_url)
        item[ 'creator_full_name']=''.join(creator_full_name).strip()
        item[ 'creator_has_built_projects_number']= creator_buildhistory_has_built_projects_number
        item[ 'creator_has_backed_projects_number']=creator_buildhistory_has_backed_projects_number
        item[ 'creator_friends_facebook_number' ]=''.join(creator_friends__facebook_number)
        item[ 'creator_Facebook_url' ]=''.join(creator_Facebook_url)
        item[ 'updates_number']=''.join(updates)
        item[ 'comments_count']= comments_count
        item['url']=someurl
        item['launched_at']=launched_at
        #multi-data
        rewards={}

        rewards[ 'Project_ID']= project_ID
        rewards[ 'rewards_level_divided_by_goal' ]=rewards_level_divided_by_goal
        rewards[ 'rewards_level_name' ]= listleftn(rewards_level_name)
        rewards[ 'rewards_level_description' ]=rewards_level_description
        rewards[ 'rewards_backers_level_distribution']= rewards_backers_level_distribution
        rewards[ 'pledge_limit' ]= listleftn(pledge_limit)
        item['category']= category
    return item, rewards , item[ 'Project_ID'] , item['project_state']

def webscraper_failorcanceled(someurl,sel,the_page1):
    root_url = 'https://www.kickstarter.com'
    try:
        creator_bio_info_shorturl_list = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/p/a[1]//@href')
        #                                           //*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[1]/a
        #print creator_bio_info_shorturl_list
        #                                sel.xpath('//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[1]/a/@href')
        creator_bio_info_url = root_url + ''.join(creator_bio_info_shorturl_list)
        #print creator_bio_info_url
        #turn to new creator_bio_websites
        creator_bio_info = urllib2.urlopen(creator_bio_info_url).read()
        creator_bio_info_sel= etree.HTML(creator_bio_info)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            projectitem={'Project_ID':0,'project_state':'Error'}
            rewards={}
            ID=0
            state='Error'
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            projectitem={'Project_ID':0,'project_state':'Error'}
            rewards={}
            ID=0
            state='Error'
    else:
        project_name_str = sel.xpath('//*[@id="content-wrap"]/section/div[1]/div/h2/a/text()')
        project_name = ''.join(project_name_str).strip('\n')
        for line in the_page1:
            #project_ID_str
            if 'data'  in line:
                words = line.split('" ')
                for word in words:
                    if 'data class="Project' in word:
                        project_ID_str = word.split('Project')[1]
            #created_at/setupdate
            if 'created_at&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'created_at' in word:
                        created_at_str = word.split('&quot;:')[1]
            if '&quot;deadline&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'deadline&quot;:' in word:
                        deadline_quot_str = word.split('&quot;:')[1]
            if '&quot;launched_at&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'launched_at' in word:
                        launched_at_str= word.split('&quot;:')[1]
            if '&quot;state_changed_at&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'state_changed_at' in word:
                        state_changed_at_str= word.split('&quot;:')[1]
        #location_id

        category_location_str = sel.xpath('//*[@class="NS_projects__category_location ratio-16-9"]//*/text()')
        try:
            location_id_str=category_location_str[0]
        except:
            location_id_str='Error'


        try:
            category_str=category_location_str[1]
        except:
            category_str='Error'
        #print 'location is %s ' %location_id_str
        location_id =''.join(location_id_str).strip('\n')
        category=''.join(category_str).strip('\n')
        project_ID = ''.join(project_ID_str)
        launched_at=''.join(launched_at_str)
        created_at=''.join(created_at_str)
        state_changed_at=''.join(state_changed_at_str)
        deadline_quot=''.join(deadline_quot_str)
        #backers_count
        backers_count= sel.xpath('//*[@id="backers_count"]/data/text()')
        #goal
        goal = sel.xpath('//*[@id="stats"]/div/div[2]/span/span[1]/text()')
        #pledged_amount
        pledged_amount = sel.xpath('//*[@id="pledged"]/data/text()')

        #data_percent_rasied
        data_percent_rasied = sel.xpath('//*[@id="pledged"]/@data-percent-raised')
        #data-currency
        currency = sel.xpath('//*[@id="pledged"]/data/@data-currency')
        #data_poll_url
        data_pool_url = sel.xpath('//*[@id="stats"]/div/div[3]/div/div//@data-poll_url')

        video = sel.xpath('//*[@id="video-section"]/@data-has-video')
        #backers_count
        hours_left = sel.xpath('//*[@id="project_duration_data"]//@data-hours-remaining')
        #day_left
        day_left = sel.xpath('//*[@id="stats"]/div/div[3]/div/div/div/text()')
        #data-duration
        data_duration = sel.xpath('//*[@id="project_duration_data"]//@data-duration')
        #updates
        updates = sel.xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[3]/span/text()')
        #rewardsstructure
        #rewards
        rewards_level_divided_by_goal = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/h2/span[1]/text()')
        #print rewards_level_name
        rewards_level_name = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/h3/text()')
        rewards_backers_level_distribution =sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/div[3]/span[@class="pledge__backer-count"]/text()')
        #rewards_backers_level_distribution =sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/div[3]/span[3]')
        #print rewards_level.spilt()
        #rewards_level_description
        #print len(rewards_level)
        #rewards_level_description
        state = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/@data-project-state')[0]
        comments_count=sel.xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[4]/@data-comments-count')
        #initialation
        rewards_level_description =[]
        pledge_limit = []
        #ship_location_info
        ship_location_info = ['0']*len(rewards_level_divided_by_goal)
        #print len(rewards_level)
        #rewards_level_description
        #ship_info

        #pledge_limit
        for i in xrange(1,len(rewards_level_divided_by_goal)):
            #print i
            c = str(i)
            #rewards_level_description
            rewards_level_description_a= '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            rewards_level_description_b = ']/div[2]/div[1]/p/text()'
            #pledge_limit for each part of pledges
            pledge_limit_a= '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            pledge_limit_b = ']/div[2]/div[3]//span[@class="pledge__limit"]/text()'
            #ship_info
            ship_location_info_a = '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            ship_location_info_b =']/div[2]/div[2]/div[2]/span[2]/text()'
            #combin the xpath for each variable
            pledge_limit_a += c
            pledge_limit_a += pledge_limit_b
            ship_location_info_a += c
            ship_location_info_a += ship_location_info_b
            rewards_level_description_a += c
            rewards_level_description_a += rewards_level_description_b
            #declare the empty list
            rewards_level_description_split_list=[]
            pledge_limit_split_list=[]
            ship_location_info_list=[]
            #split each variable
            #rewards_level_description
            rewards_level_description_split_list = sel.xpath(rewards_level_description_a)
            rewards_level_description_split = rewards_level_description_split_list
            rewards_level_description_split =''.join(rewards_level_description_split)
            rewards_level_description.append(rewards_level_description_split)
            #pledge_limit
            pledge_limit_split_list = sel.xpath(pledge_limit_a)
            pledge_limit_split = pledge_limit_split_list
            pledge_limit_split =''.join(pledge_limit_split)
            pledge_limit.append(pledge_limit_split)
            #ship_location_info
            #ship_location_info_split_list = sel.xpath(ship_location_info_a)
            #ship_location_info_split = ship_location_info_split_list
            #print ship_location_info_split, ship_location_info_split_list
            #ship_location_info_split =''.join(ship_location_info_split)
            #ship_location_info_split= str(ship_location_info_split)
            #ship_location_info[i-1] = ship_location_info_split
        deadline_xpath= sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[1]/div/div/p/time/text()')
        #project_description
        description = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[1]/div[2]/p/text()')
        #creator_info_hub
        #creator_short_name
        creator_short_name = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/h5/a/text()')
        #creator_url
        creator_personal_url = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/div[3]/div/div[2]/p/a//@href')
        #creator_bio_info

        creator_full_name = creator_bio_info_sel.xpath('//*[@id="main_content"]/header/div/div/div[2]/h1/a/text()')
        #creator_buildhistory
        #print creator_full_name
        creator_personal_url = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[1]/div[2]/ul/li/a/@href')
        #print ccccc
        creator_Facebook_url=creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[*]/span[2]/a/@href')
        #
        if ''.join(creator_personal_url)=='':
            creator_personal_url_s=0
        else:
            creator_personal_url_s=''.join(creator_personal_url)

        comments_count=sel.xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[4]/@data-comments-count')

        creator_friends__facebook_number_potential_list = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]//text()')
        #print creator_friends__facebook_number_potential_list

        creator_friends__facebook_number_potential=[]
        for words in creator_friends__facebook_number_potential_list:
            if words !='\n' and words!='\n\n':
                creator_friends__facebook_number_potential.append(words)
        #print creator_friends__facebook_number_potential
        if not 'Last login' in creator_friends__facebook_number_potential[0]:
            creator_short_name=creator_friends__facebook_number_potential[0]
        else:
            creator_short_name=[]
        creator_buildhistory_has_built_projects_number='null'
        creator_buildhistory_has_backed_projects_number='null'
        creator_friends__facebook_number = 'Not connected'
        for word in creator_friends__facebook_number_potential:
            if 'created' in word:
                creator_buildhistory_has_built_projects_number=word.split('\n')
            if 'backed' in word:
                creator_buildhistory_has_backed_projects_number=word.split('\n')
            if 'friend' in word:
                creator_friends__facebook_number= word

        state_other=sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[3]/div/div[*]/div/h3/text()')

        #print state_changed_at
        deadline_date= ''.join(deadline_quot_str)
        backers_count_str = ''.join(backers_count)
        goal_str = ''.join(goal)
        pledged_amount_str =''.join(pledged_amount)
        currency_str = ''.join(currency)
        data_percent_rasied_str = ''.join(data_percent_rasied)
        hours_left_str = ''.join(hours_left)
        projectitem={}
        rewards={}

        projectitem['has_a_video']= ''.join(video)
        projectitem['project_name'] = project_name
        #projectitem[ 'project_name']= project_name
        projectitem[ 'location_ID']= location_id
        projectitem[ 'Project_ID']= project_ID
        projectitem['duration'] =''.join(data_duration)

        #print 'Project ID', id
        if state != '':
            projectitem[ 'project_state' ]= state
        else:
            projectitem[ 'project_state' ]=''.join(state_other)
        projectitem['created_at']= created_at
        projectitem['Deadline']=deadline_quot
        #print 'deadline_xpath', deadline_date
        projectitem['state_changed_at']= state_changed_at
        projectitem[ 'backers_count']= backers_count_str
        #print 'backers_count',  dics['backerscount']
        projectitem[ 'Goal']= goal_str
        projectitem[ 'pledged_amount']=pledged_amount_str
        #print 'pledged', pledged
        projectitem[ 'data_percent_rasied']= data_percent_rasied_str
        projectitem[ 'currency']= currency_str
        projectitem[ 'hours_left']= hours_left_str
        #print 'day_left', day_left
        projectitem[ 'description']=''.join(description).strip('\n')
        projectitem[ 'creator_short_name']=''.join(creator_short_name)
        projectitem[ 'creator_personal_url']=''.join(creator_personal_url)
        projectitem[ 'creator_bio_info_url']=''.join(creator_bio_info_url)
        projectitem[ 'creator_full_name']=''.join(creator_full_name)
        projectitem[ 'creator_has_built_projects_number']=creator_buildhistory_has_built_projects_number
        projectitem[ 'creator_has_backed_projects_number']=creator_buildhistory_has_backed_projects_number
        projectitem[ 'creator_friends_facebook_number' ]=''.join(creator_friends__facebook_number)
        projectitem[ 'creator_Facebook_url' ]=''.join(creator_Facebook_url)
        projectitem[ 'updates_number']=''.join(updates)
        projectitem[ 'comments_count']= comments_count
        projectitem['url']=someurl
        projectitem['launched_at']=launched_at
        #multi-data


        rewards[ 'Project_ID']= project_ID
        rewards[ 'rewards_level_divided_by_goal' ]=rewards_level_divided_by_goal
        rewards[ 'rewards_level_name' ]= listleftn(rewards_level_name)
        rewards[ 'rewards_level_description' ]=rewards_level_description
        rewards[ 'rewards_backers_level_distribution']= rewards_backers_level_distribution
        rewards[ 'pledge_limit' ]= listleftn(pledge_limit)
        projectitem['category']= category
    return projectitem, rewards , projectitem[ 'Project_ID'] , projectitem['project_state']

def webscraper_live(someurl,sel,the_page1):
    root_url = 'https://www.kickstarter.com'
    try:

        creator_bio_info_shorturl_list = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/p/a[1]//@href')
        creator_bio_info_url = root_url + ''.join(str(x) for x in creator_bio_info_shorturl_list)
        #turn to new creator_bio_websites
        creator_bio_info = urllib2.urlopen(creator_bio_info_url).read()
        creator_bio_info_sel= etree.HTML(creator_bio_info)
    except URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            projectitem={'Project_ID':0,'project_state':'Error'}
            rewards={}
            ID=0
            state='Error'
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            projectitem={'Project_ID':0,'project_state':'Error'}
            rewards={}
            ID=0
            state='Error'
    else:
        project_name_str = sel.xpath('//*[@id="content-wrap"]/section/div[1]/div/h2/a/text()')
        project_name = ''.join(project_name_str).strip('\n')
        for line in the_page1:
            #project_ID_str
            if 'data'  in line:
                words = line.split('" ')
                for word in words:
                    if 'data class="Project' in word:
                        project_ID_str = word.split('Project')[1]
            #created_at/setupdate
            if '&quot;created_at&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'created_at&quot;:' in word:
                        created_at_str = word.split('&quot;:')[1]
            #state_changed_at
            if '&quot;state_changed_at&quot;' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'state_changed_at&quot;:' in word:
                        state_changed_at_str= word.split('&quot;:')[1]
            #deadline_quot
            if '&quot;deadline&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'deadline&quot;:' in word:
                        deadline_quot_str = word.split('&quot;:')[1]
            #if 'ref=category"><span aria-hidden' in line:
            #    words = line.split('"')
            #    for word in words:
            #        if '?ref=category' in word:
            #            discover_category =  word.split('?ref=category')[0]
            #            category = discover_category.rsplit('/discover/categories/')[1]
            if '&quot;launched_at&quot;:' in line:
                words = line.split(',&quot;')
                for word in words:
                    if 'launched_at' in word:
                        launched_at_str= word.split('&quot;:')[1]
        #location_id
        #createddate/set up date
        category_location_str = sel.xpath('//*[@class="NS_projects__category_location ratio-16-9"]//*/text()')
        try:
            location_id_str=category_location_str[0]
        except:
            location_id_str='Error'


        try:
            category_str=category_location_str[1]
        except:
            category_str='Error'
        #print 'location is %s ' %location_id_str
        location_id =''.join(location_id_str).strip('\n')
        #category=''.join(category_str).strip('\n')
        project_ID = ''.join(project_ID_str)
        launched_at=''.join(launched_at_str)
        category = ''.join(category_str).strip('\n')
        created_at=''.join(created_at_str)
        state_changed_at=''.join(state_changed_at_str)
        deadline_quot=''.join(deadline_quot_str)
        video = sel.xpath('//*[@id="video-section"]/@data-has-video')
        #print video
        #backers_count
        backers_count= sel.xpath('//*[@id="backers_count"]/data/text()')
        #goal
        goal = sel.xpath('//*[@id="stats"]/div/div[2]/span/span[1]/text()')
        #pledged_amount
        pledged_amount = sel.xpath('//*[@id="pledged"]/data/text()')

        #data_percent_rasied
        data_percent_rasied = sel.xpath('//*[@id="pledged"]/@data-percent-raised')
        #data-currency
        currency = sel.xpath('//*[@id="pledged"]/data/@data-currency')
        #data_poll_url
        data_pool_url = sel.xpath('//*[@id="stats"]/div/div[3]/div/div//@data-poll_url')
        #setup date
        #setup_date = sel.xpath('')
        #hours_left
        hours_left = sel.xpath('//*[@id="project_duration_data"]//@data-hours-remaining')
        #day_left
        day_left = sel.xpath('//*[@id="stats"]/div/div[3]/div/div/div/text()')
        #data-duration
        data_duration = sel.xpath('//*[@id="project_duration_data"]//@data-duration')
        #updates
        updates = sel.xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[3]/span/text()')
        #rewardsstructure
        #rewards
        rewards_level_divided_by_goal = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/h2/span[1]/text()')
        #print rewards_level_name
        rewards_level_name = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/h3/text()')
        rewards_backers_level_distribution =sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/div[3]/span[@class="pledge__backer-count"]/text()')
        #rewards_backers_level_distribution =sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li[*]/div[2]/div[3]/span[3]')
        #print rewards_level.spilt()
        #rewards_level_description
        #print len(rewards_level)
        #rewards_level_description
        #initialation

        rewards_level_description =[]
        pledge_limit = []
        #ship_location_info
        ship_location_info = ['0']*len(rewards_level_divided_by_goal)
        #print len(rewards_level)
        #rewards_level_description
        #ship_info
        #pledge_limit
        for i in xrange(1,len(rewards_level_divided_by_goal)):
            #print i
            c = str(i)
            #rewards_level_description
            rewards_level_description_a= '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            rewards_level_description_b = ']/div[2]/div[1]/p/text()'
            #pledge_limit for each part of pledges
            pledge_limit_a= '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            pledge_limit_b = ']/div[2]/div[3]//span[@class="pledge__limit"]/text()'
            #ship_info
            ship_location_info_a = '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[2]/div[1]/div/ol/li['
            ship_location_info_b =']/div[2]/div[2]/div[2]/span[2]/text()'
            #combin the xpath for each variable
            pledge_limit_a += c
            pledge_limit_a += pledge_limit_b
            ship_location_info_a += c
            ship_location_info_a += ship_location_info_b
            rewards_level_description_a += c
            rewards_level_description_a += rewards_level_description_b
            #declare the empty list
            rewards_level_description_split_list=[]
            pledge_limit_split_list=[]
            ship_location_info_list=[]
            #split each variable
            #rewards_level_description
            rewards_level_description_split_list = sel.xpath(rewards_level_description_a)
            rewards_level_description_split = rewards_level_description_split_list
            rewards_level_description_split =''.join(rewards_level_description_split)
            rewards_level_description.append(rewards_level_description_split)
            #pledge_limit
            pledge_limit_split_list = sel.xpath(pledge_limit_a)
            pledge_limit_split = pledge_limit_split_list
            pledge_limit_split =''.join(pledge_limit_split)
            pledge_limit.append(pledge_limit_split)
            #ship_location_info
            #ship_location_info_split_list = sel.xpath(ship_location_info_a)
            #ship_location_info_split = ship_location_info_split_list
            #print ship_location_info_split, ship_location_info_split_list
            #ship_location_info_split =''.join(ship_location_info_split)
            #ship_location_info_split= str(ship_location_info_split)
            #ship_location_info[i-1] = ship_location_info_split
        deadline_xpath= sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[1]/div/div/p/time/text()')
        #project_description
        comments_count=sel.xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[4]/@data-comments-count')
        description = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[1]/div[2]/p/text()')
        #creator_info_hub
        #creator_short_name
        creator_short_name = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/h5/a/text()')
        #creator_url
        creator_personal_url = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/div[3]/div/div[2]/p/a//@href')
        #creator_bio_info

        creator_full_name = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[1]/span/span[2]/text()')
        #creator_buildhistory
        creator_personal_url = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[1]/div[2]/ul/li/a/@href')
        #print ccccc
        creator_Facebook_url=creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[*]/span[2]/a/@href')


        creator_friends__facebook_number_potential_list = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]//text()')
        #print creator_friends__facebook_number_potential_list

        creator_friends__facebook_number_potential=[]
        for words in creator_friends__facebook_number_potential_list:
            if words !='\n' and words!='\n\n':
                creator_friends__facebook_number_potential.append(words)
        #print creator_friends__facebook_number_potential
        if not 'Last login' in creator_friends__facebook_number_potential[0]:
            creator_short_name=creator_friends__facebook_number_potential[0]
        else:
            creator_short_name=[]
        creator_buildhistory_has_built_projects_number='null'
        creator_buildhistory_has_backed_projects_number='null'
        creator_friends__facebook_number = 'Not connected'
        for word in creator_friends__facebook_number_potential:
            if 'created' in word:
                creator_buildhistory_has_built_projects_number=word.split('\n')
            if 'backed' in word:
                creator_buildhistory_has_backed_projects_number=word.split('\n')
            if 'friend' in word:
                creator_friends__facebook_number= word
        creator_friends__facebook_number_potential=str(creator_friends__facebook_number_potential_list)
        #print creator_friends__facebook_number_potential_list,creator_friends__facebook_number_potential,type(creator_friends__facebook_number_potential)


         #//*[@id="bio"]/div/div[2]/div[4]/a


        state = sel.xpath('//*[@id="content-wrap"]/div[2]/section[1]/@data-project-state')[0]
        deadline_date= ''.join(deadline_xpath)
        backers_count_str = ''.join(backers_count)
        goal_str = ''.join(goal)
        pledged_amount_str =''.join(pledged_amount)
        currency_str = ''.join(currency)
        data_percent_rasied_str = ''.join(data_percent_rasied)
        hours_left_str = ''.join(hours_left)
        projectitem = {}
        #pledged = ''
        #state_changed_at = ''
        #comments_count = ''
        #id = ''
        projectitem['project_name'] = project_name
        #projectitem[ 'project_name']= project_name
        projectitem[ 'location_ID']= location_id
        projectitem[ 'Project_ID']= project_ID
        #print 'Project ID', id
        if state != '':
            projectitem[ 'project_state' ]= state
        else:
            projectitem[ 'project_state' ]=''.join(state_other)
        projectitem['created_at']= created_at
        projectitem['Deadline']=deadline_quot
        #print 'deadline_xpath', deadline_date
        projectitem['state_changed_at']=state_changed_at
        projectitem[ 'backers_count']= backers_count_str
        #print 'backers_count',  dics['backerscount']
        projectitem[ 'Goal']= goal_str
        projectitem[ 'pledged_amount']=pledged_amount_str
        #print 'pledged', pledged
        projectitem[ 'data_percent_rasied']= data_percent_rasied_str
        projectitem[ 'currency']= currency_str
        projectitem[ 'hours_left']= hours_left_str
        #print 'day_left', day_left
        projectitem['has_a_video'] =''.join(video)
        projectitem[ 'description']=''.join(description).strip('\n')
        projectitem[ 'creator_short_name']=''.join(creator_short_name)
        projectitem[ 'creator_personal_url']=''.join(creator_personal_url)
        projectitem[ 'creator_bio_info_url']=''.join(creator_bio_info_url)
        projectitem[ 'creator_full_name']=''.join(creator_full_name)
        projectitem[ 'creator_has_built_projects_number']=creator_buildhistory_has_built_projects_number
        projectitem[ 'creator_has_backed_projects_number']=creator_buildhistory_has_backed_projects_number
        projectitem[ 'creator_friends_facebook_number' ]=''.join(creator_friends__facebook_number)
        projectitem[ 'creator_Facebook_url' ]=''.join(creator_Facebook_url)
        projectitem[ 'updates_number']=''.join(updates)
        projectitem[ 'comments_count']= comments_count
        projectitem['duration'] =''.join(data_duration)
        projectitem['url']=someurl
        projectitem['launched_at']=launched_at
        #multi-data
        rewards={}

        rewards[ 'Project_ID']= project_ID
        rewards[ 'rewards_level_divided_by_goal' ]=rewards_level_divided_by_goal
        rewards[ 'rewards_level_name' ]= listleftn(rewards_level_name)
        rewards[ 'rewards_level_description' ]=rewards_level_description
        rewards[ 'rewards_backers_level_distribution']= rewards_backers_level_distribution
        rewards[ 'pledge_limit' ]= listleftn(pledge_limit)
        projectitem['category']= category
    return projectitem, rewards , projectitem[ 'Project_ID'] , projectitem['project_state']
#----------------------------------------------------------------

def listleftn(l):
    lenlists =len(l)
    for i in xrange(0,lenlists):
        l[i]=l[i].strip('\n')
    return l
#pre-processs
#loading collected information
def createurl(target_url_file,have_collected_url):
    url_list =read_url_file(target_url_file)
    collected_unclear=read_url_file(have_collected_url)
    collected=list(set(collected_unclear))
    file_lsit=list(set(url_list)-set(collected))
    file = list(set(file_lsit))
    return file,collected

def createurlfromcsv(target_url_file_csv,have_collected_url):
    target_url_file=readacsv(target_url_file_csv)
    url_list =target_url_file['url']
    collected_unclear=read_url_file(have_collected_url)
    collected=list(set(collected_unclear))
    file_lsit=list(set(url_list)-set(collected))
    file = list(set(file_lsit))
    return file,collected
#loading sving path process
def filepathcollection(publicpath,url_file):
    #/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/middle60project/total/collected.txt
    #publicpath='/Users/sn0wfree/Dropbox/BitTorrentSync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/middle60project/total'
    rewards_backers_distribution= publicpath+'/rewards_backers_distribution.csv'
    rewards_pledge_limit= publicpath+'/rewards_pledge_limit.csv'
    rewards_pledged_amount= publicpath+'/rewards_pledged_amount.csv'
        #item_collect='/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/middle60project/slpit/item.txt'
    #rewards_collect=publicpath+'/url%srewards.txt'
    saving_file = publicpath+'/project_data.csv'
        #index_value20='/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/test/index_value.txt',
        #index_keys20='/Users/sn0wfree/Dropbox/BitTorrent Sync/kickstarterscrapy/kickstarterrunopt/reconstruction/data/test/index_keys.txt'
    target_url_file= publicpath+ url_file
    have_collected_url= publicpath+'/collected.txt'
    return rewards_backers_distribution,rewards_pledge_limit,rewards_pledged_amount,saving_file,target_url_file,have_collected_url
#-------------------------------------------------------------
#mail_it_prcess
def getAttachment(attachmentFilePath):
    contentType, encoding = mimetypes.guess_type(attachmentFilePath)

    if contentType is None or encoding is not None:
        contentType = 'application/octet-stream'

    (mainType, subType) = contentType.split('/', 1)
    with open(attachmentFilePath, 'r') as file:
        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(),_subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(),_subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(file.read())

    encode_base64(attachment)

    attachment.add_header('Content-Disposition', 'attachment',filename=os.path.basename(attachmentFilePath))
    return attachment

def sendmailtodelivery(mail_username,mail_password,to_addrs,*attachmentFilePaths):
    from_addr = mail_username
    # HOST & PORT
    HOST = 'smtp.gmail.com'
    PORT = 25
    # Create SMTP Object
    smtp = smtplib.SMTP()
    #print 'connecting ...'

    # show the debug log
    smtp.set_debuglevel(1)

    # connet
    try:
        print smtp.connect(HOST,PORT)
    except:
        print 'CONNECT ERROR ****'
    # gmail uses ssl
    smtp.starttls()
    # login with username & password
    try:
        #print 'loginning ...'
        smtp.login(mail_username,mail_password)
    except:
        print 'LOGIN ERROR ****'
    # fill content with MIMEText's object
    msg = MIMEMultipart()
    for attachmentFilePath in attachmentFilePaths:
        msg.attach(getAttachment(attachmentFilePath))
    msg.attach(email.mime.text.MIMEText('data collecting process has completed at %s and here is the data file'% now,'plain', 'utf-8'))
    msg['From'] = from_addr
    msg['To'] = ';'.join(to_addrs)
    msg['Subject']='data collecion completed'
    #print msg.as_string()
    smtp.sendmail(from_addr,to_addrs,msg.as_string())
    smtp.quit()
#-------------------------------------------------------------------------
#multiprocessing
def main(file,y):

    for j in xrange(y):
        t = ThreadClass(queue)
        t.setDaemon(True)
        t.start()
    for someurl in file:

        queue.put(someurl)
    queue.join()

class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            (target) = self.queue.get()
            global collected
            datacollectprocess(target,file1)
            #time.sleep(1/10)
            self.queue.task_done()
#progress_bar
def progress_test(counts,lenfile,speed,w):
    bar_length=20
    eta=time.time()+w
    precent =counts/float(lenfile)

    ETA=datetime.datetime.fromtimestamp(eta)
    hashes = '#' * int(precent * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|read %d projects|Speed : %.4f |ETA: %s """ % (precent*100,hashes + spaces,counts,speed,ETA))

    #sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects" % (counts,f2-f1))

    #sys.stdout.write("\rPercent: [%s] %d%%,remaining time: %.4f mins"%(hashes + spaces,precent,w))
    sys.stdout.flush()
  #time.sleep()


#def mainbody():
#def sn0wfree_s_demo:






if __name__ == '__main__':
    global y
    print '***********************************************************'
    y=input('1) choose the number of workers for this jobs:')
    print '***********************************************************'
    publicpath=input('2) please enter the document path for saving file:')
    print '=============================================================='
    #publicpath='/Users/sn0wfree/Dropbox/BitTorrentSync/data/sample folder'
    url_file=input ('3) please enter the target url file for starting,need add /:')
    print '________________________________________________________________'
    mail = input('mail it?(1 or 0):')
    if mail ==1:
        mail_password=input('please enter mail password:')
    #if mail !=0 or mail !=1:
    elif mail<0:
        confirm=input('confirm?:yes or no')
        if confirm == 'yes':
            justajoke(mail)
            print ''
        else:
            pass
    else:
        pass
    #url_file='/allleftofdataset.csv'
    gc.enable()
    global counts
    counts = 0
    global total_item
    global total_rewards_backers_distribution
    global total_rewards_pledge_limit
    global total_rewards_pledged_amount
    #global y
    total_item=[]
    total_rewards_backers_distribution=[]
    total_rewards_pledge_limit=[]
    total_rewards_pledged_amount=[]
    print '\nsubjobs  begin!'
    (rewards_backers_distribution,rewards_pledge_limit,rewards_pledged_amount,saving_file,target_url_file,have_collected_url) = filepathcollection(publicpath,url_file)

    rewards_headers=['Project_ID','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89']
    item_headers = ['Project_ID','project_name','Goal','url',
                  'pledged_amount','backers_count','creator_full_name',
                  'creator_personal_url','creator_has_backed_projects_number','creator_has_built_projects_number',
                  'creator_bio_info_url','creator_Facebook_url','currency','duration','location_ID','state_changed_at','created_at','launched_at','Deadline','description','category','project_state','has_a_video','comments_count','updates_number','data_percent_rasied','hours_left','creator_short_name','creator_friends_facebook_number']
    global file1
    global collected
    (file1,collected) = createurlfromcsv(target_url_file,have_collected_url)
    print 'begin to collecting data'
    queue = Queue.Queue()
    main(file1,y)
    collected_list_overwrite(collected,have_collected_url)
    #(someurl,total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)=catchup(someurl,total_item,total_rewards_backers_distribution,total_rewards_pledge_limit,total_rewards_pledged_amount)
    writeacsvprocess(saving_file,item_headers,total_item)
    writeacsvprocess(rewards_backers_distribution,rewards_headers,total_rewards_backers_distribution)
    writeacsvprocess(rewards_pledge_limit,rewards_headers,total_rewards_pledge_limit)
    writeacsvprocess(rewards_pledged_amount,rewards_headers,total_rewards_pledged_amount)
    counts=0
    print  '\nsubjobs completed!'
    #time.sleep(0.1)

    if mail == 1:
        print 'saving process completed'
        target=  publicpath +'/project_data.csv'
        now =  datetime.datetime.today()
        pathfile=publicpath+ '/%s.zip' % now
        print 'compress process completed'
        zipafilefordelivery(pathfile,target)

        print 'begin sending email'
        mail_username='linlu19920815@gmail.com'

        to_addrs="snowfreedom0815@gmail.com"
        attachmentFilePaths=pathfile
        sendmailtodelivery(mail_username,mail_password,to_addrs,attachmentFilePaths)
        print 'email sent'
    else:
        print 'TAT, coding is tough job for non-computer science students'





        #sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects" % (counts,f2-f1))

        #sys.stdout.write("\rPercent: [%s] %d%%,remaining time: %.4f mins"%(hashes + spaces,precent,w))

      #time.sleep()
