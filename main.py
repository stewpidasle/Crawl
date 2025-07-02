import asyncio
from crawl4ai import AsyncWebCrawler

async def main():

    async with AsyncWebCrawler() as crawler:
        
        result = await crawler.arun(url="https://www.illinoislottery.com/about-the-games/unpaid-instant-games-prizes")  
        
        print(result.markdown)

asyncio.run(main()) 