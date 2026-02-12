import aiohttp
import asyncio
import aiofiles
import tempfile
from pathlib import Path
import hashlib
import shutil
import math


async def probeUrlRange(session: aiohttp.ClientSession, url: str, timeout: int = aiohttp.ClientTimeout(total=10)):
    async with session.head(url) as response:
        acceptRanges = response.headers.get("Accept-Ranges", "").lower()
        contentLength = response.headers.get("Content-Length")
        if acceptRanges == "bytes" and contentLength and contentLength.isdigit():
            return {"supportRange": True,
                    "fileSize": int(contentLength)}
        else:
            return {"supportRange": False}


def getChunkList(concurrency, fileSize):
    if fileSize <= 0:
        return []
    if concurrency <= 0:
        concurrency = 1
    baseChunkSize = fileSize // concurrency
    remainder = fileSize % concurrency
    chunks = []
    start = 0
    for i in range(concurrency):
        chunkSize = baseChunkSize + (1 if i < remainder else 0)
        if chunkSize == 0:
            break
        end = start + chunkSize - 1
        if end > fileSize - 1:
            end = fileSize - 1
        chunks.append((start, end))
        start = end + 1
        if start >= fileSize:
            break
    return chunks


def getRecommendedConcurrency(maxConcurrency, fileSize):
    smallFile = 1 * 1024 * 1024
    mediumFile = 10 * 1024 * 1024
    largeFile = 100 * 1024 * 1024
    veryLargeFile = 1 * 1024 * 1024 * 1024
    if fileSize < smallFile:
        recommended = 1
    elif fileSize < mediumFile:
        recommended = 2
    elif fileSize < largeFile:
        recommended = 4
    elif fileSize < veryLargeFile:
        recommended = 8
    else:
        baseSize = 100 * 1024 * 1024
        dynamicConcurrency = min(16, math.ceil(fileSize / baseSize))
        recommended = dynamicConcurrency
    return min(recommended, maxConcurrency)


async def downloadWorker(session: aiohttp.ClientSession, url: str, fileName: str = None,
                         tempDir: str = tempfile.mkdtemp(), saveDir: str = Path.cwd(), chunkSize: int = 1024 * 5,
                         maxConcurrency: int = 16):
    if fileName is None:
        fileName = url.split('/')[-1] or hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
    tempPath = Path(tempDir) / fileName
    savePath = Path(saveDir) / fileName
    urlRangeResult = await probeUrlRange(session, url)

    if urlRangeResult["supportRange"] is False:
        async with session.get(url) as response:
            async with aiofiles.open(tempPath, 'wb') as file:
                async for chunk in response.content.iter_chunked(chunkSize):
                    await file.write(chunk)
        await asyncio.to_thread(shutil.move, str(tempPath), str(savePath))
        print(f"{fileName} 已经下载到 {savePath}目录中")
    else:
        fileSize = urlRangeResult["fileSize"]
        downloadConcurrency = getRecommendedConcurrency(maxConcurrency, fileSize)
        chunkRanges = getChunkList(downloadConcurrency, fileSize)
        tasks = []
        concurrencyTasks = []

        async def rangeDownloadWorker(workerId, chunkRange, tasksList):
            header = {'Range': f'bytes={chunkRange[0]}-{chunkRange[1]}'}
            chunkTempPath = Path(tempDir) / str(workerId)
            async with session.get(url, headers=header) as response:
                async with aiofiles.open(chunkTempPath, 'wb') as file:
                    async for chunk in response.content.iter_chunked(chunkSize):
                        await file.write(chunk)
                tasksList[workerId]["status"] = "success"

        for index, currentRange in enumerate(chunkRanges):
            subTask = {"id": index, "range": currentRange, "status": None}
            tasks.append(subTask)
            concurrencyTasks.append(rangeDownloadWorker(index, subTask["range"], tasks))

        await asyncio.gather(*concurrencyTasks)

        async with aiofiles.open(tempPath, 'wb') as tempFile:
            for currentId in range(len(chunkRanges)):
                chunkFilePath = Path(tempDir) / str(currentId)
                async with aiofiles.open(chunkFilePath, 'rb') as chunkFile:
                    while True:
                        chunk = await chunkFile.read(chunkSize)
                        if not chunk:
                            break
                        await tempFile.write(chunk)

        shutil.move(str(tempPath), str(savePath))
        print(f"{fileName} 已经分片高速下载到 {savePath}目录中")


async def main():
    async with aiohttp.ClientSession() as session:
        await downloadWorker(session, "https://dldir1v6.qq.com/qqfile/qq/QQNT/Windows/QQ_9.9.27_260205_x64_01.exe")


if __name__ == "__main__":
    asyncio.run(main())