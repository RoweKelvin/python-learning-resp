import aiohttp
import asyncio
import aiofiles
import tempfile
from pathlib import Path
import hashlib
import shutil

async def downloadWorker(session:aiohttp.ClientSession, url:str,filename:str=None,tempDir:str=tempfile.mkdtemp(),saveDir:str=Path.cwd(),chunkSize:int=1024*5):
    if filename is None:
        filename = url.split('/')[-1] or hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
    tempPath = Path(tempDir) / filename
    savePath = Path(saveDir) / filename
    async with session.get(url) as response:
        async with aiofiles.open(tempPath,'wb') as file:
            async for chunk in response.content.iter_chunked(chunkSize):
                await file.write(chunk)
    await asyncio.to_thread(shutil.move,tempPath,savePath)
    print(f"{filename} 已经下载到 {savePath}目录中")



