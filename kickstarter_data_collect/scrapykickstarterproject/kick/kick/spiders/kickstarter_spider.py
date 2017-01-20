# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from urllib2 import Request, urlopen, URLError

import urllib2
import requests
from lxml import etree

import scrapy
from scrapy.selector import Selector
from scrapy.http import  Request
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bbs.items import BbsItem





class kickstarterspider(scrapy.Spiders):
    name = " kickstarter"
    allowed_domains = ["kickstarter.com"]
    start_urls = 'https://www.kickstarter.com/projects/mnbookarts/the-s-helmes-and-w-gaglione-rubber-stamp-archive?ref=category_featured'



#def parse(self, response):
#   sel = Selector(response)

#   items = []

#for site in sel:
#       item = DmozItem()
#       item['name'] = site.xpath('//*[@id="content-wrap"]/section/div[1]/div/h2/a/text()').extract()
#       item['creator_url'] = site.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/h5/a/text()').extract()
#       item['description'] = site.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[1]/div[2]/p/text()').extract()
#       item.append(item)
#       return item




#someurl = 'https://www.kickstarter.com/projects/neliobarros/nixin-typeface?ref=discover_potd'
#someurl = 'https://www.kickstarter.com/projects/1060627644/35000-years-in-the-making-pens-made-from-ancient-k?ref=category_featured'



def parse(self, someurl):

    root_url = 'https://www.kickstarter.com'
    response = urllib2.Request(someurl)
    content = urllib2.urlopen(someurl).read()
    sel= etree.HTML(content)
    ##this is for some data without tab.
    req = urlopen(response)
    the_page1 = req.readlines()
    def OnlyStr(s,oth=''):
        #s2 = s.lower();
        fomart = 'abcdefghijklmnopqrstuvwxyz0123456789:,'
            for c in s:
                if not c in fomart:
                    s = s.replace(c,'');
                        return s;
                    #print(OnlyStr(a))
    #change type of list
    names = locals()
    #project_name
    project_name_str = sel.xpath('//*[@id="content-wrap"]/section/div[1]/div/h2/a/text()')
    project_name = ''.join(project_name_str)
    #projetc_ID
    #created_at/setupdate
    #deadline_quot
    #createddate/set up date
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
        if 'deadline&quot;:' in line:
            words = line.split(',&quot;')
            for word in words:
                if 'deadline' in word:
                    deadline_quot_str = word.split('&quot;:')[1]
        if 'ref=category"><span aria-hidden' in line:
            words = line.split('"')
            for word in words:
                if '?ref=category' in word:
                    discover_category =  word.split('?ref=category')[0]
                    category = discover_category.rsplit('/discover/categories/')[1]
    #location_id
    #createddate/set up date
    location_id_str = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[1]/div[2]/div[1]/div/a[1]/text()')
    location_id =''.join(location_id_str)
    project_ID = ''.join(project_ID_str)
    created_at=''.join(created_at_str)
    #state_changed_at=''.join(state_changed_at_str)
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
    for i in range(1,len(rewards_level_divided_by_goal)):
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

    #deadline
    deadline_xpath= sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[1]/div/div/p/time/text()')
    #project_description
    description = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[1]/div[2]/p/text()')
    #creator_info_hub
    #creator_short_name
    creator_short_name = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/h5/a/text()')
    #creator_url
    creator_personal_url = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/div[3]/div/div[2]/p/a//@href')
    #creator_bio_info
    creator_bio_info_shorturl_list = sel.xpath('//*[@id="content-wrap"]/section/div[2]/div/div[2]/div[6]/div/div[2]/div[2]/p/a[1]//@href')
    creator_bio_info_url = root_url + ''.join(str(x) for x in creator_bio_info_shorturl_list)
    #turn to new creator_bio_websites
    creator_bio_info = urllib2.urlopen(creator_bio_info_url).read()
    creator_bio_info_sel= etree.HTML(creator_bio_info)
    creator_full_name = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[1]/span/span[2]/text()')
    #creator_buildhistory
    creator_buildhistory_has_backed_projects_number = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[4]/a/text()')
    creator_buildhistory_has_built_projects_number = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[4]/text()')
    built_projects_number_list = creator_buildhistory_has_built_projects_number
    backed_projects_number_list = creator_buildhistory_has_backed_projects_number
    creator_buildhistory_has_built_projects_number = "".join(built_projects_number_list).strip()
    creator_buildhistory_has_backed_projects_number = "".join(backed_projects_number_list).strip()
    #facebook information
    creator_friends__facebook_number_potential = str(creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[3]/text()'))
    if 'Not connected' in creator_friends__facebook_number_potential:
        creator_friends__facebook_number = 'Not connected'
        creator_Facebook_url = 'Not connected'
    else:
        creator_Facebook_url= creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[3]/span[2]/a//@href')
        creator_friends__facebook_number_str = creator_bio_info_sel.xpath('//*[@id="bio"]/div/div[2]/div[3]/span[2]/a/text()')
        creator_friends__facebook_number = ''.join(creator_friends__facebook_number_str)

    data_pool_url = sel.xpath('//*[@id="stats"]/div/div[3]/div/div//@data-poll_url')
    data_pool_url = ''.join(str(x) for x in data_pool_url)
    #print data_pool_url
    #turn to new websites
    #new data form
    data_pool_url_websites = urllib2.urlopen(data_pool_url).read()
    data_pool_url_websites = ''.join(str(x) for x in data_pool_url_websites)
    a = data_pool_url_websites#.split(',')
    #print a
    name =[]
    #transfor list to dictionary
    b = OnlyStr(a).strip('project:')
    for i in range(0,len(b.split(','))):
        name.append(b.split(',')[i].split(':'))
    dics = dict(name)
    #print dics
    #print 'value: %s' % dics.items()
    state = dics['state']
    pledged = dics ['pledged']
    state_changed_at = dics['statechangedat']
    comments_count = dics['commentscount']
    id = dics['id']
    #data_structure_change
    deadline_date= ''.join(deadline_xpath)
    backers_count_str = ''.join(backers_count)
    goal_str = ''.join(goal)
    pledged_amount_str =''.join(pledged_amount)
    currency_str = ''.join(currency)
    data_percent_rasied_str = ''.join(data_percent_rasied)
    hours_left_str = ''.join(hours_left)

    item = {}
    level_rewards_by_goal={}
    level_rewards_by_backers_distribution={}
    level_rewards_by_pledge_limit={}
    level_rewards_by_description={}
    level_rewards_by_name={}
    a=[]

    #obb = ['name','pledged','description','pledge_limit','backers_distribution']
    for i in range(1,len(rewards_level_divided_by_goal)+1):
        #print i
        a.append(i)
    #print a
    level_rewards_by_goal=dict(zip(a,rewards_level_divided_by_goal))
    level_rewards_by_backers_distribution=dict(zip(a,rewards_backers_level_distribution))
    level_rewards_by_pledge_limit=dict(zip(a,pledge_limit))
    level_rewards_by_description=dict(zip(a,rewards_level_description))
    level_rewards_by_name=dict(zip(a,rewards_level_name))
    #print rewards
    level_rewards_by_goal["project ID"]= project_ID_str
    level_rewards_by_backers_distribution["project ID"]= project_ID_str
    level_rewards_by_pledge_limit["project ID"]= project_ID_str
    level_rewards_by_description["project ID"]= project_ID_str
    level_rewards_by_name["project ID"]= project_ID_str
    #retuen item

    item['project_name'] = project_name
    #item[ 'project_name']= project_name
    item[ 'location_ID']= location_id
    item[ 'Project ID']= project_ID
    #print 'Project ID', id
    item[ 'projetc_state' ]= state
    item[ 'category']= category
    item[ 'created_at']=created_at
    item[ 'Deadline']=deadline_quot
    #print 'deadline_xpath', deadline_date
    item[ 'state_changed_at']=state_changed_at

    item[ 'backers count']= backers_count_str
    #print 'backers_count',  dics['backerscount']
    item[ 'Goal']= goal_str
    item[ 'pledged_amount']=pledged_amount_str
    #print 'pledged', pledged
    item[ 'data_percent_rasied']= data_percent_rasied_str
    item[ 'currency']= currency_str
    item[ 'hours_left']= hours_left_str
    #print 'day_left', day_left


    item[ 'description']=''.join(description)
    item[ 'creator_short_name']=''.join(creator_short_name)
    item[ 'creator_personal_url']=''.join(creator_personal_url)
    item[ 'creator_bio_info_url']=''.join(creator_bio_info_url)
    item[ 'creator_full_name']=''.join(creator_full_name)
    item[ 'creator_buildhistory_has_built_projects_number']=creator_buildhistory_has_built_projects_number
    item[ 'creator_buildhistory_has_backed_projects_number']=creator_buildhistory_has_backed_projects_number
    item[ 'creator_friends__facebook_number' ]=''.join(creator_friends__facebook_number)
    item[ 'creator_Facebook_url' ]=''.join(creator_Facebook_url)
    item[ 'updates number']=''.join(updates)
    item[ 'comments_count']= comments_count




    #multi-data
    rewards={}

    rewards[ 'rewards_level_divided_by_goal' ]=''.join(rewards_level_divided_by_goal)
    rewards[ 'rewards_level_name' ]=''join(rewards_level_name)
    rewards[ 'rewards_level_description' ]=''join(rewards_level_description)
    rewards[ 'rewards_backers_level_distribution']= rewards_backers_level_distribution
    rewards[ 'pledge_limit' ]= pledge_limit
    #for i in range(0,len(rewards_level)
    #    print rewards_level[i]

    #print 'ship_location_info' , ship_location_info
    return item


#def rewards_backers_webscraper(someurl):
#    x= webscraper(someurl)
#    return level_rewards_by_backers_distribution
#try:
#   response = Request(someurl)
#       content = urllib2.urlopen(someurl).read()
#           sel= etree.HTML(content)
#               ##this is for some data without tab.
#               req = urlopen(response)
#                   the_page1 = req.readlines()
#except URLError as e:
#   if hasattr(e, 'reason'):
#       print 'We failed to reach a server.'
#       print 'Reason: ', e.reason
#   elif hasattr(e, 'code'):
#       print 'The server couldn\'t fulfill the request.'
#       print 'Error code: ', e.code
#else:
#   kickstarter_projetc_data = webscraper(someurl)
#print kickstarter_projetc_data
