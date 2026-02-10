from pathlib import Path
def createAndWriteFile():
    folderPath = Path("testFolder")
    folderPath.mkdir(exist_ok=True)
    print(f"已创建文件夹: {folderPath}")
    filePath = folderPath / "data.txt"
    with open(filePath, "w", encoding="utf-8") as fileObj:
        fileObj.write("第一行内容\n")
        fileObj.write("第二行内容\n")
    print(f"已写入文件: {filePath}")
def readFileContent():
    filePath = Path("testFolder") / "data.txt"
    if filePath.exists():
        with open(filePath, "r", encoding="utf-8") as fileObj:
            content = fileObj.read()
        print(f"文件内容:\n{content}")
    else:
        print("文件不存在")
def appendToFile():
    filePath = Path("testFolder") / "data.txt"
    with open(filePath, "a", encoding="utf-8") as fileObj:
        fileObj.write("追加的内容\n")
    print("已追加内容到文件")
def listFiles():
    folderPath = Path("testFolder")
    if folderPath.exists():
        print("文件夹内文件:")
        for item in folderPath.iterdir():
            print(f"  - {item.name}")
    else:
        print("文件夹不存在")
def copyFile():
    sourcePath = Path("testFolder") / "data.txt"
    targetPath = Path("testFolder") / "data_backup.txt"
    with open(sourcePath, "r", encoding="utf-8") as sourceFile:
        content = sourceFile.read()
    with open(targetPath, "w", encoding="utf-8") as targetFile:
        targetFile.write(content)
    print(f"已复制文件到: {targetPath}")
def deleteFiles():
    folderPath = Path("testFolder")
    for item in folderPath.iterdir():
        item.unlink()
    folderPath.rmdir()
    print("已删除文件夹及其内容")
def main():
    createAndWriteFile()
    readFileContent()
    appendToFile()
    readFileContent()
    copyFile()
    listFiles()
    deleteFiles()
if __name__ == "__main__":
    main()
