# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class kickstarterItem(scrapy.Item):
    # define the fields for your item here like:
    #basic info.
    project_name = scrapy.Field() 
    location_ID  = scrapy.Field()
    Project ID  = scrapy.Field()
    projetc_state = scrapy.Field()
    category  = scrapy.Field()
    created_at = scrapy.Field()
    Deadline = scrapy.Field()
    state_changed_at = scrapy.Field()

    backers count  = scrapy.Field()
    Goal  = scrapy.Field()
    pledged_amount = scrapy.Field()
    data_percent_rasied = scrapy.Field()
    currency = scrapy.Field()
    hours_left = scrapy.Field()


    description  = scrapy.Field()
    creator_short_name = scrapy.Field()
    creator_personal_url = scrapy.Field()
    creator_bio_info_url = scrapy.Field()
    creator_full_name = scrapy.Field()
    creator_buildhistory_has_built_projects_number = scrapy.Field()
    creator_buildhistory_has_backed_projects_number = scrapy.Field()
    creator_friends__facebook_number = scrapy.Field()
    creator_Facebook_url = scrapy.Field()
    updates number = scrapy.Field()
    comments_count  = scrapy.Field()




    pass
