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

seedurl = "http://en.wikipedia.org/wiki/Sustainable_energy"

# Frontier list to keep track of all the urls
frontier=[]
frontier.append(seedurl.lower())

# visited_List maintains a list of urls that have already been visited
visited_List = []

# countdepth is an array which keeps track of number of urls at a particular depth
# For depth 1, it is countdepth[0]
countdepth = [0] * 5
depth = 2
countdepth[0] = 1

regex = re.compile(r'^/wiki/', re.IGNORECASE)

# Create a list to keep track of urls to be crawled
queue = []
queue.append(seedurl.lower())
visited_List.append(seedurl.lower())
frontier.append(seedurl.lower())

f = open('CrawledUrls.txt', 'w')



# Main function

def main():
	
	# Call crawl function on seed Url
	crawl(seedurl, depth)

	print "Number of urls visited----" + str(len(visited_List))
	print "Total Number of urls ----" + str(len(frontier))

	#Open file to write urls into it

	with open("CrawledUrls.txt", "a") as f: 
		print f
		for list in visited_List:
			f.write("\n" + str(list))

	f.close()	


# crawl function takes a url to be crawled and a depth
def crawl(url, depth):

	if url == seedurl:
			depth = 2
			queue.pop(0)

	# Depth is more than 5 or matched List max reached		
	elif depth > 5 or len(visited_List) >= 1000:
		"Depth is more than 5 or visited List max reached"
		return
	
	# sleep for 1 second before next request
	time.sleep(1)

	# get the links from url page and check for connection error, if everything is ok, continue
	r  = requests.get(url)
	if r.status_code == 200:
		data = r.text
		soup = BeautifulSoup(data)


		# Find all links which are not internal reference or admin links and match the given pattern
		# Also check if number of urls in visited_List has not reached 1000, else break the loop

		for link in soup.find_all("a"):
			if (regex.match(str(link.get("href")))) and (link.get("href") != "/wiki/Digital_object_identifier"):
				url = link.get('href')
				if (":" not in url) and ("#" not in url):	
					completeUrl = urljoin("http://en.wikipedia.org", url).lower()

					if len(visited_List) < 1000:

						# if url is not in visited list or to be visited list, then add it to to be visited list
						if (completeUrl not in visited_List) and (completeUrl not in queue):						
							
							queue.append(completeUrl.lower())
							frontier.append(completeUrl.lower())
							
							# increment the count of urls at a particular depth
							countdepth[depth-1] = countdepth[depth - 1] + 1

					else:
						break


		# while all the urls at a particular depth are not crawled and visited_List max has not been reached
		# and depth is not more than 5, crawl all the links at that particular depth and then increment 
		# depth counter for further processing
		while countdepth[depth-1] != 0:
			
			if len(visited_List) < 1000 and depth <=5 :

				nextUrl = queue.pop(0)
				print "Now crawling URL ----" + nextUrl
				if nextUrl not in visited_List:
					visited_List.append(nextUrl.lower())
					# Call internal crawler function to crawl this url
					internalCrawler(nextUrl,depth+1)
				countdepth[depth-1] = countdepth[depth-1] - 1
			else:
				break

		# When all the urls at a particular depth have been crawled, increase the depth and crawl the next url
		if countdepth[depth-1] == 0:
			depth = depth + 1
			url = queue.pop()
			print "crawling url --- " + url

			# if url is not already in visited list, add it to visited list and call crawl function on it
			if url.lower() not in visited_List:
				visited_List.append(url.lower())
				crawl(url, depth)	
	else:
		return			

# internal crawler function crawls the next url and keeps track of matched urls.
# Input for function is the url to be crawled, and the depth

def internalCrawler(nextUrl, d):
	
	# sleep for 1 second before next request
	time.sleep(1)
	r1  = requests.get(nextUrl)

	# Check for connection error, if status_code = 200 everything is OK, so continue
	if r1.status_code ==  requests.codes.ok:
		dataInternal = r1.text
		soup1 = BeautifulSoup(dataInternal)

		# Find all links which are not internal reference or admin links and match the given pattern
		# Also check if number of urls in matched_List has not reached 1000, else break the loop
		for link1 in soup1.find_all("a"):
				
			url1 = link1.get('href')
					
			if (regex.match(str(url1))):				
				if (":" not in url1) and ("#" not in url1):
						
					completeUrl1 = urljoin("http://en.wikipedia.org", url1).lower()

					# if visited list and has not reached max, add url to visited list and queue
					if len(visited_List) < 1000:
						if (completeUrl1 not in visited_List) and (completeUrl1 not in queue):
							
							queue.append(completeUrl1.lower())
							frontier.append(completeUrl1.lower())			
							countdepth[d-1] = countdepth[d-1] + 1

					else:
						break
	else:
		return					

if __name__== '__main__':
    main()						