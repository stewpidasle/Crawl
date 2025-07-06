from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, CrawlerMonitor, DisplayMode, MemoryAdaptiveDispatcher
import asyncio

async def crawl_batch():
    browser_config = BrowserConfig(headless=True, verbose=False)
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
            urls_total=0,
            refresh_rate=1.0,
            enable_ui=True,
            max_width=120
        )
  
    )

    urls = [
        "https://www.illinoislottery.com/about-the-games/unpaid-instant-games-prizes",
        "https://www.illinoislottery.com/about-the-games/lottery-players",
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
                await process_result(result)
            else:
                print(f"Failed to crawl {result.url}: {result.error.message}")

async def process_result(result):       
        """
        Process successful crawl result.
        
        Args:
            result: CrawlerResult object containing page data and metadata
        """

        # Extract basic page information
        print(f"\nProcessing: {result.url}")
        print(f"Status Code: {result.status_code}")

        # Extract and process text content
        if result.markdown:
            #Remove extra whitespace and get first 150 characters as preview
            clean_text = ' '.join(result.markdown.split())
            preview = clean_text[:150] + '...' if len(clean_text) > 150 else clean_text
            print(f"Content Preview: {preview}")

        # Process metadata
        if result.metadata:
            print("\nMetadata:")
            for key, value in result.metadata.items():
                print(f"  {key}: {value}")  

        # Process links found on the page
        if result.links:
            internal_links = result.links.get("internal", [])
            external_links = result.links.get("external", [])
            print(f"Found {len(internal_links)} internal links.")
            print(f"Found {len(external_links)} external links.")

        print("-" * 80) # Separator for results

asyncio.run(crawl_batch())
    
              
