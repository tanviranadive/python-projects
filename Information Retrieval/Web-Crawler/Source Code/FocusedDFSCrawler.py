from bs4 import BeautifulSoup

import requests
import re
import sys
import codecs
import urllib2
reload(sys)
import time
from urlparse import urljoin
sys.setdefaultencoding('utf-8')

#f = open('DFSUrls.txt','w').close()


seedurl = "https://en.wikipedia.org/wiki/Sustainable_energy"
keyword = "solar"

# Frontier list to keep track of all the urls
frontier=[]
frontier.append(seedurl)

# visited_List maintains a list of urls that have already been visited
visited_List = []

# matched_List maintains a list of urls that match with the given keyword
matched_List = []
urlList = []
#depth = 1

# open output file to write into
f = open('DFSUrls.txt', 'w')

regex = re.compile(r'^/wiki/', re.IGNORECASE)

# Create a list to keep track of urls to crawl
stack = []
stack.append(seedurl)




# crawl function takes a url to be crawled and a depth d

def crawl(url, d):

	# if depth becomes 5 return to the parent node and crawl the next child of that node
	if d == 5:
		print "at depth 5 and returning"
		return
	
	elif len(matched_List) < 1000:
		print "At depth--------" + str(d)
		
		# sleep for 1 second before sending next request. Then get request and check if status code is ok
		# otherwise return back

		time.sleep(1)
		r1  = requests.get(url)
		if r1.status_code == 200:
	
			data1 = r1.text
			soup1 = BeautifulSoup(data1)
			for link1 in soup1.find_all("a"):
				
				# Find all links which are not internal reference or admin links and match the given pattern
				# Also check if number of urls in matched_List has not reached 1000, else break the loop
				if (regex.match(str(link1.get("href")))):
					url1 = link1.get('href')
					if (":" not in url1) and ("#" not in url1) and (link1.get('class')!="img") and (url1 not in visited_List) :
						completeUrl1 = urljoin("http://en.wikipedia.org", url1)

						#add url to visited list and check if it matches with the keyword

						visited_List.append(completeUrl1)
						if ((re.search(keyword, url1, re.IGNORECASE)) or (re.search(keyword, link1.text, re.IGNORECASE))) and (completeUrl1 not in matched_List):
							
							print completeUrl1
							stack.append(completeUrl1)

							# check if matched list has not reached its max and if url is already present in matched list
							# if not, add it to matched list and crawl the children node of that url

							if len(matched_List) < 1000 and (completeUrl1 not in matched_List):
								matched_List.append(completeUrl1)
								time.sleep(1)
								crawl(completeUrl1, d+1)
							else:
								break	
		else:
			return	


# Main function

def main():

	# Crawl main link first
	time.sleep(1)
	r  = requests.get(seedurl)

	# check for connection error, if everything is ok, continue
	if r.status_code == 200:
		data = r.text
		soup = BeautifulSoup(data)

		# Find all links which are not internal reference or admin links and match the given pattern and keyword
		for link in soup.find_all("a"):
			
			if (regex.match(str(link.get("href")))):
						url = link.get('href')
						
						if (":" not in url) and ("#" not in url) and (link.get('class')!="img") and (url not in visited_List):
							completeUrl = urljoin("http://en.wikipedia.org", url)
							
							if (re.search(keyword, url, re.IGNORECASE)) or (re.search(keyword, link.text, re.IGNORECASE)):
								urlList.append(completeUrl)
															
		

		for url in urlList:

			# add url to visited list and crawl the url
			visited_List.append(url)

			if len(matched_List) >= 1000:
				break
			elif (url not in matched_List):
				matched_List.append(url)
				print "Crawling------" + url
				time.sleep(1)
				crawl(url, 2)
			else:
				continue	

		
	else:
		return
		

		print "Visited list count------"
		print len(visited_List)	

		print "Matched list count-------" 
		print len(matched_List)	

		with open("DFSUrls.txt", "a") as DFSFile: 
			print DFSFile   

   		for list in matched_List:
   			print list
   			DFSFile.write("\n" + list)

		DFSFile.close()					

if __name__== '__main__':
    main()
					


	 
