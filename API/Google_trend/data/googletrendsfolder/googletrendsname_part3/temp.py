def spe(keywords):
    keywords_sep_list = chunks(keywords, 1003)
    for l in xrange(len(keywords_sep_list)):
        locals()[str(l)] = '%s.txt' % str(l + 1)
        write_txt(keywords_sep_list[l], locals()[str(l)])



def chunks(target, n):
    if isinstance(target, list):
        date1 = [target[i:i + n] for i in xrange(0, len(target), n)]
    else:
        date1 = []
        raise ValueError, "Wrong type,I need a list."
    return date1





def write_txt(fi, targetpath):
    with open(targetpath, 'w') as f:
        for ff in fi:
            f.write(ff + '\n')

def read_ticker(tickerfile):
    tic = []
    with open(tickerfile, 'r') as ticker:
        ticker = ticker.readlines()
        for line in ticker:
            tic.append(line.strip())
    return tic
if __name__ == '__main__':
	tickerfile = '/Users/sn0wfree/Documents/googletrendsfolder/googletrendsname_part1/name.txt'
	t = read_ticker(tickerfile)
	test=['1-800 FLOWERS COM','1ST SOURCE CORP','21ST CENTURY FOX CL A','21ST CENTURY FOX CL B','2U INC']
	keywords_sep_list = chunks(t, 1003)
	spe(t)