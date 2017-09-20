# <span id = "README">Google Trends Download Tool</span>

This [READ.ME](#README) is to describe the usage of **Google Trends Download Tool**


## 0. <span id = "QuickStart">Quick Start</span>

1. Store the execuateble file and the [keywords.txt](#FLE) into same folder.
2. Double tick the execuatable file.
3. (Option) Change the parameters
4. Tick `Go!` botton
5. Leave it alone
6. Repeat step 4-6 in the next day until finish the work
7. Find the result in the data folder (same path of [keywords.txt](#FLE))



## 1. <span id = "Content">Content</span>
0. [Quick Start](#QuickStart)
1. [Content](#Content)
2.  [Getting Started](#GettingStarted)
  2.1. [Google Trends Download Tool with the Executable Program](#GTDTEP)
  2.2. [Google Trends Download Tool with the Source Code](#GTDTSC)
3.  [Parameters Explanation](#PE)
4.  [File Format/Location Explanation](#FLE)
5.  [Precautions](#Precautions)
6.  [Authors](#Authors)
7.  [License](#License)

## 1.1. WorkFlow

```flow



st=>start: Getting Started


op1=>operation: Google Trends Download Tool with the Source Code
op2=>operation: Google Trends Download Tool with the Executable Program

op3=>operation: Run Program
e=>end:
check1=>operation: Check Python:> #installpython
check2=>operation: Check PIP

sub1=>subroutine: Install Python
sub2=>subroutine: Install PIP/Packages
cond=>condition: Python installed Yes or No?
cond2=>condition: PIP/Packages installed Yes or No?

io=>inputoutput: Catch Result...

st->op1->check1->cond

cond(yes)->check2->cond2

cond2(yes)->op3->op2->io
cond2(no)->sub2->op3->op2->io
cond(no)->sub1->check2



```

## 2. <span id = "GettingStarted">Getting Started</span>

Here are two way to use the **Google Trends Download Tool**:
1. [Google Trends Download Tool with the Executable Program](#GTDTEP)
2. [Google Trends Download Tool with the Source Code](#GTDTSC)



## 2.1. <span id = "GTDTEP">Google Trends Download Tool with the Executable Program</span>

This instructions will tell you the usage of Google Trends Download Tool with the Executable Program.
And the usage of it is very simple:

* Keep the Executable file(normally call `gui.exe` for windows and `gui` for macOS) and [keywords.txt](#FLE) file in one same folder(call [**Folder**](#FLE) hereafter). 

* And double tick the Executable file to run.  

* And the Following Instruction please see the **Step 3** and **Step 4** in the [Running code](#RunningCode)



## 2.2. <span id = "GTDTSC">Google Trends Download Tool with the Source Code</span>

If you choose to use this way to download Google Search Volume Data, then you need  prepare the Source Code environment: [Python 2.7](https://www.python.org) and install related packages. Please see [Installation](#installation)

### 2.2.1.<span id = "installation">Installation</span>

* <span id = "checkpython">Check Python and PIP version or Download Python/PIP</span>.

  >This Source Code is developed via the [Python 2.7](https://www.python.org). Thus if to use Source code, make sure the computer install the [Python 2.7](https://www.python.org)
  
  >Thus, first thing is to check the Installation of Python. 
  
  >>For Mac OS X or OSX or macOS, the [Python 2.7](https://www.python.org) have already installed. But you still can check it whether is available.
  >For Windows, [Python 2.7](https://www.python.org) environment normally is not installed. So Windows Users must download [Python 2.7](https://www.python.org) and related packages.
* <span id = "checkpip">Check the installation of Package management tool and required packages or install them</span>
  > pip is the python package management tool, which is to fast install packages and deploy the code environment.
---

####  <span id = "ForMac">For Mac</span>
>Mac users are easy to start, because the python normally is already installed. Thus, the Mac users can skip the [Install Python](#installpython) Step and driectly see [Install pip](#installpip) Step.

##### <span id = "installpython">Install Python</span>
  For checking Python installation in the Macbook /Pro/Air, you may follow this instruction:
  1. Open the [Terminal](), which is located in the Utilities folder within the Applications folder. 
  2. Type the following command:
  > ```
  >python -V
  >```
  3. Press Return. Normally, you will recevie:  `Python 2.7.X :: XXXXXXXXXXXXXX(x86_64)`. `XXXXXXXXXXXXXX(x86_64)` is the brenchname of Python, which is unnecessary in this case. if not, you may follow [the instruction of Python.org](https://www.python.org/about/gettingstarted/) to install [Python 2.7](https://www.python.org)



  
##### <span id = "installpip">Install pip</span>  
  To check installation of Package management tool (`pip`) and Packages 
  1. As the same with [last step](#checkpython), you should open the [Terminal]() firstly.
  2.  Type the command:
  >```
  >bash <(curl -s https://raw.githubusercontent.com/sn0wfree/data-collection-and-api/master/Tool/install-requirments.sh)
  >```
  3. You may receive the following symbol and the output with `Requirement already satisfied` labels or `Successfully installed XXXX` labels:
  
  >```
  > % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current Dload  Upload   Total   Spent    Left  Speed
  >100 1558k  100 1558k    0     0  3453k      0 --:--:-- --:--:-- --:--:-- 3524k
 > ....
 > ```
   
  > That means the `pip` and required packages are already installed in your Mac.
---



  
####  <span id = "ForWindow">For Window</span>
  > Windows Users need a fully step of installation Python and PIP, becasue Windows do not bind the python as the default component.
  
 * To install [Python 2.7](https://www.python.org) and `pip`, please follow [the instruction of Python.org](https://www.python.org/about/gettingstarted/) and [pip](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation).
 
 * After installation of Python and PIP, please type into the following commands:
>```
>pip install requests
>pip install requests_cache
>pip install pandas
>```
* When finish these commands, the Environment and packages should be installed.


* Then you can go through and [Running code](#RunningCode).

 
 

---

###  2.2.2. <span id = "RunningCode">Running code</span>
  1. Then you should be ready to use the Source Code.
  
  * The Source Code includes two files: [gui.py](https://raw.githubusercontent.com/sn0wfree/data-collection-and-api/master/API/Google_trend/Source/gui.py) and  [GoogleTrendsCollectionToolWithGui.pyc](https://raw.githubusercontent.com/sn0wfree/data-collection-and-api/master/API/Google_trend/Source/GoogleTrendsCollectionToolWithGui.pyc). I recommand to put them in one empty folder (let's call it as [**Folder**](#FLE) hereafter) and one [keywords.txt](#FLE) file as well（see [File Format/Location Explanation](#FLE)）. 
  * And then you can use the [Terminal]() (for Windows user is called Command-line,see  [CMD](https://www.computerhope.com/issues/chusedos.htm)) to jump to the **Folder** by typing the following command into [Terminal]() (for Windows user is called Command-line,see  [CMD](https://www.computerhope.com/issues/chusedos.htm)):
  
      >```
      >cd /path/to/yourfolder
      >```

  * Here, `/path/to/yourfolder` is the path of your folder: [**Folder**](#FLE) . It might requires your password, that password is your login passwrod, normally. 

  2. And last step, type the following command into [Terminal]() (for Windows user is called Commandline,see  [CMD](https://www.computerhope.com/issues/chusedos.htm)) to run the Source Code:
      >```
      >python gui.py
      >```
  
  3. Just wait several seconds, you may see a window with **_a commandable console_**. The window like this:
  ![Screen Shot 2017-09-19 at 14.28.24.png](resources/11F6DFB1896D34CEB9A38DDE6BFFAA7C.png =450x188)

* This is the Interface of Download Tool. 
* If the [keywords.txt](#FLE) file has been put into correct loaction (same loaction with code or execuatable file), see [File Format/Location Explanation](#FLE). The program may automatically detect the path of it. If not,it will show "Not Found". You may need to manually choose the path by ticking the "Browse" button, or type in the full path by hands.

* And the parameters have been pre-set completely. You can change these paremeters as you need. Except the **Start Year** and **Keywords** (the first and second parameters), other parameters are not well tested and debuged, thus do not recommand to change it. See [Parameters Explanation](#PE)
  
4. If all have been set. Then you need is just to tick '**Go!**' bottun to start running program and wait it to grab the results.
  >> Attention: Because of Google Policy, each IP only can request 500-1500 requests per day (about 20-75 projects,depend on the recent request frequency). Hence, this program can collect max 75 projects information per day. It will automatically stop when the quota limit is reach and print out the status ("**Quota limit Reach**") in the **_commandable console_**. Then you can tick '**Quit**' botton to exit or leave it alone. And re-run it in the Next Time
5. Result will be stored in the data folder which own the same path of [keywords.txt](#FLE) file.
  >> The [keywords.txt](#FLE) also will be amend for the continue function. The number of keywords in this file will reduce with the process continuing. That means when the have completed the task, the [keywords.txt](#FLE) should be the empty file.
---





---


## 3. <span id = "PE">Parameters Explanation</span>


This program requires 4 parameters, and all own the per-set value.


These parameters include: 
  * (1) **_Start Year or Period/Date_**; 
  * (2) **_Keywords_**; 
  * (3) **_Category_**  
  * (4) **_~~Geography~~_**.

### Explanation

> * **_Start Year or Period/Date_**: is the Start year of your period. And it will include the date from the first day of start year to Now, if the data is avaiable. You can change to others like 2010 or 2014,please do type in the future year.
>>  Futhermore, you also can type date like 20141015, but it only recevies the month (10) and ingore the day (15). In this case: 20141015, the program will create the request with the date from  2014/Oct/01 to now.

>* **_Keywords_** : is the path of the keywords file, which includes the keywords you want to search. The file format is `.txt` and requires one keyword in one line. 
>>Detail/example please see [example](https://raw.githubusercontent.com/sn0wfree/data-collection-and-api/master/API/Google_trend/Source/keywords.txt)

>* **_Category_**: the searching industry, has been pre-set to 7, that is the symbol for the Financial Industry. 
>>You also can change it to others, please find the Category code in the [GoogleTrendsPage](https://trends.google.com/trends/explore?cat=3&q=s) by changing label of category and inspect the number change in the webaddress after `?cat=`.



>* **_~~Geography~~_**: is the searching region/area, has been pre-set into the World-Wide.(malfunctional) 
>>**Attention**: This function has been disabled for reducing bugs. Thus, this parameter is waiting further development and please leave it alone. 


## 4. <span id = "FLE">File Format/Location Explanation</span>

This part will explain the [keywords.txt](#Keywordsfile) file format/location and output/result file format/location.

### 4.1. <span id = "Keywordsfile">Keywords File</span>

The keywords file requires:
  * **Location**: you can put the keywords.txt file into any where you want, but it is recommanded to put the same location of code file or excuatable file. 
  * **Format**: A `txt` file format 
  * And the data format is one keyword one line. 

    >You can find the example [here](https://raw.githubusercontent.com/sn0wfree/data-collection-and-api/master/API/Google_trend/Source/keywords.txt).

### 4.2. <span id = "output/resultfile">Output/Result File</span>

The Output/Result file will be generated as:
  * **Location**: _stored at the location which is same with the location of keywords file._ 
    >>The output/result will be stored in the location same with the path of keywords file.
 
  * **Format**: `csv` file in the **One Folder called data**, one cache file for Backup (ingore it)
    >>  Each keyword with the target period will generate one `csv` file in the data folder and also will be backup into the `sqlite` database
 



## 5. <span id = "Precautions">Precautions</span>

This program is currently still in the beta test. Hence, there might be some unexpected errors happen. For most errors, it will automatically ingore and try again with sleep 30 seconds. All information will print out in the **console**. However, there might be some situations triggering the Flash Crash. If you unfortunately meet the Flash Crash, please contact me by [email me](mailto:snowfreedom0815@gmail.com) or submit a commit in the [this repository](https://github.com/sn0wfree/data-collection-and-api/tree/master/API/Google_trend)






## 6. <span id = "Authors">Authors</span>

* **sn0wfree** -  - [![GitHub-Mark-32px.png](resources/F87561B8BB354EF83B09A66E54F70E08.png =32x32)](https://github.com/sn0wfree); [Email](mailto:snowfreedom0815@gmail.com)



## 7. <span id = "License">License</span>

This project is licensed under the GPL-2.0 License - 