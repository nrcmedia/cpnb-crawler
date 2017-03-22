from bs4 import BeautifulSoup
import unicodecsv as csv
import datetime
import pickle
import sys
import os
import re

output = []

for file in os.listdir('data'):
    if file.endswith('.html'):
        print 'Processing:', os.path.join('/data', file)

        with open(os.path.join('data', file), 'r') as html_in:
        	soup = BeautifulSoup(html_in, 'html.parser')
        	
        # scores
        scores = range(1,61)
        scores.sort(reverse=True)

        # date
        week_n = file
        week_n = re.sub('-week','',week_n)
        week_n = re.sub('.html', '', week_n)
        week_n = re.sub(',', '-', week_n)
        time_string = [week_n]

        time_list = time_string * 60

    	# get h1
    	h1 = soup.findAll('h1')
    	h1 = [h.text for h in h1]
    	

    	# get h2
    	h2 = soup.findAll('h2')
    	h2 = [h.text for h in h2]

    	# get h3
    	h3 = soup.findAll('h3')
    	h3 = [h.text for h in h3]

    	# get h4
    	h4 = soup.findAll('h4')
    	h4 = [h.text.strip().encode('utf-8') for h in h4]

    	isbn = [h.split('ISBN ')[1] for h in h4]

    	# position
    	pos = [isbn.index(isb) + 1 for isb in isbn]

    	if len(h1) == len(h2) == len(h3) == len(scores) == len(isbn):
    		data = zip(pos, time_list, h1, h2, h3, isbn, scores)
        else:
            print 'Error with data:', file
            continue

        for book in data:
            output.append(book)

with open('boeken.p', 'wb') as pickle_out:
    pickle.dump(output, pickle_out)
    	
with open('boeken.csv', 'w') as csv_out:
	writer = csv.writer(csv_out, delimiter='\t')
	writer.writerow(['Positie', 'Datum', 'Auteur', 'Titel', 'Beschrijving', 'ISBN', 'score'])
	writer.writerows(output)

sys.exit('The end for now')