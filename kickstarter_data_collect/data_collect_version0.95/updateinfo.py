
__version__='0.1'
__author__='sn0wfree'
#-----------------------------------------------------------------------------------------------
###



from plan import *
import gc,time,datetime,random


def updateinfo(url,Project_ID,state):
    update_community_dict={}
    if state=='successful':
        url_update=url
    else:
        if '?ref=' in url:
            url_split=url.split('?ref=')[0]
            url_update=url_split+'/updates'
        else:
            url_update=''
    state_update_status,sel=pre_update_request_url_process(url_update)
    if state_update_status !='Error':
        update_datetime =sel.xpath('//*[@class="timeline"]/div[*]//@datetime')

        update_community_dict['update_datetime']=update_datetime

    else:
        update_community_dict['update_datetime']='Error'
    update_community_dict['Project_ID']=Project_ID
    if '?ref=' in url:
        url_community_split=url.split('?ref=')[0]
        url_community=url_community_split+'/community'
    else:
        url_community=''
    state_community_status,sel_community=pre_update_request_url_process(url_community)
    if state_community_status !='Error':
        community_returning_backers=sel_community.xpath('//*[@class="community-block-content clearfix"]/div[@class="existing-backers"]/div[@class="count"]/text()')
        community_new_backers=sel_community.xpath('//*[@class="community-block-content clearfix"]/div[@class="new-backers"]/div[@class="count"]/text()')
        if community_returning_backers !=[]:
            community_returning_backers=community_returning_backers[0].split()[0]
            community_new_backers=community_new_backers[0].split()[0]
        else:
            community_returning_backers=[]
            community_new_backers=[]
    else:
        community_returning_backers='Error'
        community_new_backers='Error'
    update_community_dict['community_returning_backers']=community_returning_backers
    update_community_dict['community_new_backers']=community_new_backers

    return update_community_dict

def updatecollectionprocess(url,Project_ID,project_state,Deadline,launched_at,length):
    global total_project_info
    global counts
    global saving_file
    global accesstime_control


    update_headers=['Project_ID','community_returning_backers','community_new_backers','launched_at(=0)','Deadline','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89']

    #for i in xrange(0,length):
    project_info_single=updateinfo(url,Project_ID,project_state)
    if project_info_single != {}:
        f1 =time.time()
        update_datetime=project_info_single['update_datetime']
        date={}
        if len(update_datetime)<=89:
            for j in xrange(0,len(update_datetime)):
                date['%s'%j]=update_datetime[j]
            date['Project_ID']=Project_ID
            date['launched_at(=0)']=launched_at
            date['Deadline']=Deadline
            date['community_new_backers']=project_info_single['community_new_backers']
            date['community_returning_backers']=project_info_single['community_returning_backers']
            total_project_info.append(date)
            collected.append(url)
            counts+=1
            date={}
            time.sleep(random.uniform(0.1,0.5))
        else:
            pass
        if len(total_project_info)>50:
            total_project_info_w=total_project_info
            total_project_info=[]
            collected_w=collected
            #saving process
            collected_list_overwrite(collected_w,collected_file)
            writeacsvprocess(saving_file,update_headers,total_project_info_w)
            gc.collect()
            time.sleep(random.uniform(0.1,1))
        if accesstime_control >= 30 and accesstime_control%3 ==0 :
            time.sleep(random.uniform(0.5,3))
        elif accesstime_control > 1800:
            #reset
            accesstime_control=0
            time.sleep(10)
        else:
            pass
        f2=time.time()
        w=(length-counts)*(f2-f1)/y
        progress_test(counts,length,f2-f1,w)
        accesstime_control+=f2-f1


    #time.sleep(1)

def mainupdate(tasks,y):

    for task in tasks:
        queue.put(task)
    queue.join()

class ThreadupdateClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while 1:
            task = self.queue.get()
            url=task['url']
            Project_ID=task['Project_ID']
            project_state=task['project_state']
            Deadline=task['Deadline']
            launched_at=task['launched_at']
            updatecollectionprocess(url,Project_ID,project_state,Deadline,launched_at,length)

            #time.sleep(1/10)
            self.queue.task_done()


def chunks(item,n):
    lenitem=len(item)
    dic=[]
    #split item by n
    for i in xrange(0,lenitem,n):
        if i+n < lenitem:
            dic.append(item[i:i+n])
        else:
            dic.append(item[i:])
    return dic


def inputenver(status=0):
    if status !=1000:
        publicpp=input('please enter public path:')
        filepath=input('please enter name of dataset file:')
        saving_file_name=input('saving file name setting for:')

    else:
        publicpp='/Users/sn0wfree/Dropbox/BitTorrentSync/data/update+community/uc1'
        filepath='uc1.csv'
        saving_file_name='ucdata1.csv'

    return publicpp,filepath,saving_file_name

if __name__ == "__main__":

    status=input('setup a status(0-99):')
    y=input('to choose the number of workers for this tasks:')
    mail = input('mail it?(1 or 0):')
    if mail ==1:
        mail_password=input('please enter mail password:')
    (publicpp,filepath,saving_file_name)=inputenver(status)
    file1=publicpp+'/'+filepath
    global collected_file
    collected_file=publicpp+'/collected.txt'
    global saving_file
    saving_file=publicpp+'/'+saving_file_name
    #collected
    global collected
    print 'reading/loading files'
    collected=read_url_file(collected_file)
    projectdataset=readacsv(file1)

    urls=projectdataset['url'].values.tolist()


    length=len(urls)
    tempp=[]
    for i in xrange(0,length):
        if urls[i] in collected:
            tempp.append(i)
    for j in tempp:
        projectdataset=projectdataset.drop(j,axis=0)
    tasks=[]
    urls=projectdataset['url'].values.tolist()
    Project_IDs=projectdataset['Project_ID'].values.tolist()
    project_states=projectdataset['project_state'].values.tolist()
    Deadlines=projectdataset['Deadline'].values.tolist()
    launched_ats=projectdataset['launched_at'].values.tolist()
    global accesstime_control
    accesstime_control=0
    global total_project_info
    global counts
    counts=0
    total_project_info=[]
    print 'pre-handle process begin'
    for j in xrange(0,len(urls)):
        temp={}
        temp['url']=urls[j]
        temp['Project_ID']=Project_IDs[j]
        temp['project_state']=project_states[j]
        temp['Deadline']=Deadlines[j]
        temp['launched_at']=launched_ats[j]
        tasks.append(temp)
    print 'ROM recycle activited'
    gc.enable()
    queue = Queue.Queue()
    print ' begin to crwal'
    print 'there left %d projects'%len(urls)
    update_headers=['Project_ID','community_returning_backers','community_new_backers','launched_at(=0)','Deadline','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89']

    #initial threads
#def initila_thread_process():
    for j in xrange(y):
        t = ThreadupdateClass(queue)
        t.setDaemon(True)
        t.start()
    #tasks_split=chunks(tasks,50)
    #for task in tasks_split:

    mainupdate(tasks,y)
    collected_list_overwrite(collected_w,collected_file)
    writeacsvprocess(saving_file,update_headers,total_project_info_w)

    time.sleep(random.random())
        #print total_project_info

    print 'saving process completed'

    if mail== 1:
        target=  saving_file
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
        print 'collecting process completed'
