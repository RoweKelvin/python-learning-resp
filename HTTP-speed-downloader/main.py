import asyncio
import hashlib
import shutil
import tempfile
from pathlib import Path
import aiofiles
import aiohttp


async def downloadWorker(url:str, session:aiohttp.ClientSession,fileName:str=None,chunkSize:int=1024*5,saveDir:str=Path.cwd(),tempDir:str=tempfile.mkdtemp()):
    if fileName is None:
        fileName = url.split('/')[-1] or hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
    fileTempPath=Path(tempDir,fileName)
    fileSavePath=Path(saveDir,fileName)
    async with session.get(url) as response:
        async with aiofiles.open(fileTempPath,mode='wb') as file:
            async for chunk in response.content.iter_chunked(chunkSize):
                await file.write(chunk)
    shutil.move(fileTempPath,fileSavePath)
    print(f"{fileName}下载完毕")
async def main():
    async with aiohttp.ClientSession() as session:
        await downloadWorker('https://dldir1v6.qq.com/qqfile/qq/QQNT/Windows/QQ_9.9.27_260205_x64_01.exe',session)
asyncio.run(main())
