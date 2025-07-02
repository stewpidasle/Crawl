from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMo, CrawlerMonitor, DisplayConfig
import asyncio

async def crawl_batch():
    # Configure the crawler
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,  # Use Bypass cache mode
        check_robots_txt=True,  # Check robots.txfs
        stream=False,
        `display_config = DisplayConfig(show_progress=True)
    )

    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval_=1.0,
        max_sessions_permit=10,
        monitor=CrawlerMonitor
            display_mode=DisplayMode.DETAILED
        }
    )  

    urls = [
        "https://www.illinoislottery.com/about-the-games/unpaid-instant-games-prizes",
        "https://www.example.com/another-page"
    ]




    async with AsyncWebCrawler(browser_config=browser_config) as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher
        )
        
        for result in results:
            if result.success:
                print(f"Successfully crawled {result.url}")
            else:
                print(f"Failed to crawl {result.url}: {result.error}")
            
            
            