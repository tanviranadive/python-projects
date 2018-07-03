from bs4 import BeautifulSoup


import requests
import re
import sys
import codecs
import urllib2
reload(sys)
from urlparse import urljoin
sys.setdefaultencoding('utf-8')
import time

seedurl = "https://en.wikipedia.org/wiki/Sustainable_energy"
keyword = "solar"

# Frontier list to keep track of all the urls
frontier=[]
frontier.append(seedurl)

# visited_List maintains a list of urls that have already been visited
visited_List = []

# matched_List maintains a list of urls that match with the given keyword
matched_List = []

# countdepth is an array which keeps track of number of urls at a particular depth
# For depth 1, it is countdepth[0]

countdepth = [0] * 5
depth = 2
countdepth[0] = 1

regex = re.compile(r'^/wiki/', re.IGNORECASE)

# Create a list to keep track of urls to be crawled
queue = []
queue.append(seedurl)
visited_List.append(seedurl)
#matched_List.append(seedurl)
frontier.append(seedurl)

# open output file to write into
f = open('BFSUrls.txt', 'w')



# Main function

def main():
	
	# Call crawl function on seed Url

	print "Crawling ------"

	crawl(seedurl, keyword, depth)

	
	#print "Number of visited urls -----" + str(len(visited_List))
	print "Number of matched urls----" + str(len(matched_List))

	with open("BFSUrls.txt", "a") as f: 
		print f
		for list in matched_List:
			f.write("\n" + str(list))

	f.close()	



# Crawl function takes a url, a keyword to be searched for and max depth 
# to be considered for traversing

def crawl(url, keyword, depth):

	if url == seedurl:
			depth = 2
			queue.pop(0)

	elif depth > 5 or len(matched_List) >= 1000:

		# Depth is more than 5 or matched List max reached
		return
	
	# sleep for 1 second before next request
	time.sleep(1)

	# get the links from url page
	r  = requests.get(url)

	# Check for connection error, if status_code = 200 everything is OK, so continue

	if r.status_code == 200:
		data = r.text
		soup = BeautifulSoup(data)

		# Find all links which are not internal reference or admin links and match the given pattern
		# Also check if number of urls in matched_List has not reached 1000, else break the loop
		for link in soup.find_all("a"):
			if (regex.match(str(link.get("href")))):
				url = link.get('href')
				
				if (":" not in url) and ("#" not in url):	
					completeUrl = urljoin("http://en.wikipedia.org", url)
					
					if len(matched_List) < 1000:

						# Check link if it matches the given keyword. If yes, add it to the matched_List list and queue
						# for further processing
						if ((re.search(keyword, url, re.IGNORECASE)) or (re.search(keyword, link.text, re.IGNORECASE))) and (completeUrl not in matched_List) and (completeUrl not in visited_List):
							
							matched_List.append(completeUrl)
							queue.append(completeUrl)
							frontier.append(completeUrl)						
							countdepth[depth-1] = countdepth[depth - 1] + 1
			
					else:
						break

		# while all the urls at a particular depth are not crawled and matched_List max has not been reached
		# and depth is not more than 5, crawl all the links at that particular depth and then increment 
		# depth counter for further processing

		while countdepth[depth-1] != 0:
			
			if len(matched_List) < 1000 and depth <=5 :

				nextUrl = queue.pop(0)
				print "Now crawling URL ----" + nextUrl

				# Call function internalCrawler to crawl the page and keep a track of the number of urls
				# at the next depth

				internalCrawler(nextUrl,keyword,depth+1)
				visited_List.append(nextUrl)
				countdepth[depth-1] = countdepth[depth-1] - 1
			else:
				break

		# When all the urls at a particular depth have been crawled, increase the depth and crawl the next url

		if countdepth[depth-1] == 0:
			depth = depth + 1
			url = queue.pop()
			print "Crawling url--- " + url
			visited_List.append(url)
			crawl(url, keyword, depth)
	else:
		return		



# internal crawler function crawls the next url and keeps track of matched urls.
# Input for function is the url to be crawled, the keyword and the depth

def internalCrawler(nextUrl, keyword, d):

	time.sleep(1)
	r1  = requests.get(nextUrl)

	if r1.status_code == 200:
		dataInternal = r1.text
		soup1 = BeautifulSoup(dataInternal)

		for link1 in soup1.find_all("a"):

			# Fetching links in internal crawler

			url1 = link1.get('href')
				
			# take only the urls which are not admin links or internal references.
			# Search for given keyword in those urls and add to matched_List as well as queue

			if (regex.match(str(url1))):
				
				if (":" not in url1) and ("#" not in url1):
						
					completeUrl1 = urljoin("http://en.wikipedia.org", url1)
					if len(matched_List) < 1000:
						if ((re.search(keyword, url1, re.IGNORECASE)) or (re.search(keyword, link1.text, re.IGNORECASE))) and (completeUrl1 not in matched_List) and (completeUrl1 not in visited_List):

	
							matched_List.append(completeUrl1)
							queue.append(completeUrl1)
							frontier.append(completeUrl1)			
							countdepth[d-1] = countdepth[d-1] + 1

					else:
						break
	else:
		return					

if __name__== '__main__':
    main()						