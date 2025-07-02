from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, CrawlerMonitor, DisplayMode, MemoryAdaptiveDispatcher
import asyncio

async def crawl_batch():
    browser_config = BrowserConfig(headless=True, verbose=True)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS, 
        check_robots_txt=True,  
        stream=False
    )

    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=10,
        monitor=CrawlerMonitor(
            display_mode=DisplayMode.DETAILED
        )
    )

    urls = [
        "https://www.illinoislottery.com/about-the-games/unpaid-instant-games-prizes",
    ]

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Get all results at once
        results = await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher
        )

        # Process all results after crawling
        for result in results:
            if result.success:
                print(f"Successfully crawled {result.url}")
            else:
                print(f"Failed to crawl {result.url}: {result.error}")

    async def process_result(result):       
        """
        Process successful
        
        Args:
            result: CrawlerResult object containing page data and metadata
        """

        # Extract basic page information
        print(f"\nProcessing: {result.url}")
        print(f"Status Code: {result.page_code}")

        # Extract and process text content
        if result.markdown:
            #Remove extra whitespace and get first 150 characters as preview
            clean_text = ' '.join(result.markdown.split())
            preview = clean_text[:150] + '...' if len(clean_text) > 150 else clean_text
            print(f"Preview: {preview}")

        # Process metadata
        if result.metadata:
            print("Metadata:")
            for key, value in result.metadata.items():
                print(f"  {key}: {value}")  

        # Process links found on the page
        if result.links:
            internal_links = result.links.get('internal', [])
            external_links = result.links.get('external', [])
            print(f"Found {len(internal_links)} internal links.")
            print(f"Found {len(external_links)} external links.")

        print("-" * 80) # Separator for results

asyncio.run(crawl_batch())
    
              
