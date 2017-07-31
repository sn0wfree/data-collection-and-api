# https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1090710000&period2=1501369200&interval=1d&events=history&crumb=r.RAw21SwQ.
# https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1091142000&period2=1501369200&interval=1d&events=history&crumb=r.RAw21SwQ.
#
import os


def ImportListInfobyFile(locals_file_path, target=False, GUI=False):
    keywords = []
    scan_files = os.listdir(locals_file_path)
    if target != False:

        with open(target, 'r') as ticker:
            ticker = ticker.readlines()
            for line in ticker:
                keywords.append(line.strip())
    else:

        if 'keywords.txt' in scan_files:
            fi = read_a_file('keywords.txt')
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif 'keywords2.txt' in scan_files:
            fi = read_a_file('keywords2.txt')
            for f in fi:
                keywords.extend(f.split()[0].split(','))
        elif 'keywords.csv' in scan_files:
            fi = pd.read_csv('keywords.csv')
            keywords = fi['tinker']
        else:
            keywords = 0

    return keywords

def write_txt_change(ticker, targetpath):
    Errorkeywords=[]
    fi=[]

    if isinstance(ticker,str):
        fi .append(ticker)
    elif isinstance(ticker,list):
        fi =ticker
    else:
        pass


    with open(targetpath, 'r') as f:
        ticker =f.readlines()
        for line in ticker:
                Errorkeywords.append(line.strip())
    errorticker =list(set(Errorkeywords) | set(fi))

    with open(targetpath, 'w') as f:
        for ff in errorticker:
            f.write(ff + '\n')
if __name__ == '__main__':
    locals_file_path = os.path.split(os.path.realpath(__file__))[0]
    #print ImportListInfobyFile(locals_file_path, '1.txt')

    with open('error.txt', 'w') as f:
        pass
        
    

    #write_txt_change('XRa', 'error.txt')



    
