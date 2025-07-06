from unittest import result
from fastapi import FastAPI,  HTTPException
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, CrawlerMonitor, DisplayMode, MemoryAdaptiveDispatcher
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class CrawlResponse(BaseModel):
    url: str
    status_code: int  # Expected status code for successful crawl
    content_preview: str | None = None  # Content preview to return
    metadata: dict | None = None
    internal_links_count: int | None = None
    external_links_count: int | None = None

@app.post("/crawl", response_model=CrawlResponse)
async def crawl_url(url:HttpUrl):
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
            display_mode=DisplayMode.DETAILED
        )
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Get all results at once
        results = await crawler.arun_many(
            url=[str(url)],
            config=run_config,
            dispatcher=dispatcher
        )

        if not results or not results[0].success:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to crawl {url}: {results[0].error.message if results else 'Unknown error'}")
        

        return process_result(results[0])
    
def process_result(results):
    """
    Process successful crawl result.
    
    Args:
        results: CrawlerResult object containing page data and metadata
    """
    content_preview = None
    internal_links_count = None
    external_links_count = None

    if getattr(results, "markdown", None):
        clean_text = ' '.join(results.markdown.split())
        content_preview = clean_text[:150] + "..." if len(clean_text) > 150 else clean_text

    if getattr(results, "links", None):
        internal_links_count = len(results.links.get("internal", []))
        external_links_count = len(results.links.get("external", []))

    return CrawlResponse(
        url=results.url,
        status_code=results.status_code,
        content_preview=content_preview,
        metadata=results.metadata,
        internal_links_count=internal_links_count,
        external_links_count=external_links_count
    )

    