import scrapy
import calendar
import datetime

class ResultsSpider(scrapy.Spider):
	name = "results"
	
	custom_settings = {
		'DOWNLOAD_DELAY': '6',
	}

	f=open("lastsync.txt","r")
	lastsync=datetime.datetime.strptime(f.readline().rstrip("\n"),"%Y-%m-%d")
	f.close()
	if (lastsync.weekday() == 5):
		drawDate = lastsync + datetime.timedelta(days=1)
	else:
		drawDate = lastsync + datetime.timedelta(days=3)
	start_urls = [
		'https://www.gidapp.com/lottery/singapore/4d/date/%s' % drawDate.strftime("%Y-%m-%d"),
	]

	def parse(self, response):
		
		drawID = response.css("h5.float-right::text").get()
		drawDate = response.url.split("/")[-1] 
		drawDayWeek = calendar.day_abbr[datetime.datetime.strptime(drawDate, "%Y-%m-%d").weekday()]
		results = response.css("td.text-center span:not([class])::text").getall()
		if (len(results) != 23):
			ferr=open("error.txt","a")
			ferr.write(drawDate+"\n")
			ferr.close()
		yield {
			'drawID': drawID,
			'drawDate': drawDate,
			'drawDayWeek': drawDayWeek,
			'results': results,
		}
		
		f=open("lastsync.txt","w")
		f.write(str(drawDate))
		f.close()

		next_page =  response.css("div.col:nth-child(3) > a:nth-child(1)::attr(href)").get()
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)

