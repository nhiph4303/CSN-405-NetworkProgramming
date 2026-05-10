import requests
import time

urls = ["https://example.com", "https://google.com", "https://python.org"] * 2
# import pdb; pdb.set_trace() # cách debug, đặt sau cái muốn debug 
def download_site(url):
    with requests.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

start_time = time.perf_counter()
for url in urls:
    download_site(url)
duration = time.perf_counter() - start_time
print(f"Downloaded {len(urls)} sites in {duration:.2f} seconds")

import asyncio
import aiohttp
import time

async def download_site_async(session, url):
    async with session.get(url) as response:
        content = await response.read()
        print(f"Read {len(content)} from {url}")

async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = [download_site_async(session, url) for url in sites]
        await asyncio.gather(*tasks)

urls = ["https://example.com", "https://google.com", "https://python.org"] * 2
start_time = time.perf_counter()
asyncio.run(download_all_sites(urls))
duration = time.perf_counter() - start_time
print(f"Downloaded {len(urls)} sites in {duration:.2f} seconds")