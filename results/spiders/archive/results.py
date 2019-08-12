import scrapy
import calendar
import datetime

class ResultsSpider(scrapy.Spider):
	name = "results"
	
	custom_settings = {
		'DOWNLOAD_DELAY': '5',
	}

	f=open("lastsync.txt","r")
	draw=f.readline().rstrip("\n")
	f.close()
	draw=int(draw)+1
	start_urls = [
		'http://sgresult.appspot.com/4d/?draw=%s' % draw,
	]

	def parse(self, response):
		
		drawDateStr = (response.css("td.drawdate::text").get()).split(" ")
		drawD = drawDateStr[0]
		drawM = list(calendar.month_abbr).index(drawDateStr[1])
		drawY = drawDateStr[2]
		drawID = response.url.split("=")[1]
		drawDate = (datetime.date(int(drawY),int(drawM),int(drawD))).isoformat()
		drawDayWeek = drawDateStr[3].strip("()")
		results = response.css("td.results4D::text").getall()
		if (len(results) != 23):
			ferr=open("error.txt","a")
			ferr.write(drawID + "\n")
			ferr.close()
		yield {
			'drawID': drawID,
			'drawDate': drawDate,
			'drawDayWeek': drawDayWeek,
			'results': results,
		}
		
		f.open("lastsync.txt","w")
		f.write(str(drawID))
		f.close()

		next_page = response.css("p:nth-child(4) > a:nth-child(5)::attr(href)").get()
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)

