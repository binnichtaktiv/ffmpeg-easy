import subprocess, os
from pathlib import Path

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

filePath = input("enter your video / audio path:\n")
clearTerminal()

select = int(input("what do you want to do?\n\n"
    "- edit video & audio\n[1] convert video / audio\n[2] cut video / audio\n[3] crop video\n[4] turn and mirror\n"
    "[5] change speed\n[6] create gif from video\n[7] blur a video (part or full video)\n[8] embed or extract subtitles\n"
    "[9] combine several videos into one\n[10] convert image to video (still image video)\n\n- edit audio\n[11] change volume\n"
    "[12] extract audio from a video\n[13] add or replace audio in a video\n[14] change pitch & speed\n\n-effects & filters\n"
    "[15] make video black & white\n[16] add text & watermark\n\n[17] record YouTube livestream\n"))
clearTerminal()

def videoFormat():
    fileFormat = input("enter the file format to which you want to convert your file - e.g. mp4, mp3, mkv \n(to see all supported file formats run 'ffmpeg -codecs' or 'ffmpeg -formats')\n").lower().strip()
    clearTerminal()
    return fileFormat

def getOutputPath():
    downloadLocation = int(input(f"select download location:\n[1] current folder - {os.getcwd()}\n[2] different location\n"))
    clearTerminal()

    if downloadLocation == 2:

        currentDir = os.getcwd()
        count = 0

        print(f"subfolders of {currentDir}:\n")

        folders = [folder for folder in os.listdir(currentDir) if os.path.isdir(os.path.join(currentDir, folder))]
        
        for folder in folders:
            count+=1
            print(f"[{count}]📁 {folder}")


        outputPath = input("\nselect a folder or enter full path to the desired location:\n")

        if outputPath.isdigit() and  outputPath <= str(len(folders)):
            outputPath = os.path.join(currentDir, folders[int(outputPath)-1])
            clearTerminal()
            print(f"download started and will be saved to {outputPath}")

        elif not outputPath.isdigit():
            if os.path.isdir(outputPath):
                outputPath = outputPath
                clearTerminal()
                print(f"download started and will be saved to {outputPath}")
            else:
                print("invalid output folder")
            
        elif outputPath >= str(len(folders)):
            print("invalid output folder!")
    else:
        outputPath = os.getcwd()

    return outputPath

def getFileName():

    fileName = Path(os.path.basename(filePath)).stem
    while (answer := input(f"do you want a different filename? (enter without file extension like .mp4) current filename: {fileName}\n[y/n]\n").lower()) not in ['y', 'n']:
        print("\ninvalid input. please enter 'y' or 'n'.")
        clearTerminal()

    clearTerminal()
    
    if answer == 'y':
        fileName = input("enter new filename:\n")
        clearTerminal()

    return fileName

def copyOrReEncode():
    copy = input("[1] keep original codecs (copy – no quality loss, much faster, but not always supported)\n or\n[2] re-encode?\n")
    
    if copy == 1:
        copy = True
    else:
        copy = False

if select == 1:
    fileName = getFileName()
    fileFormat = videoFormat()
    outputPath = getOutputPath()
    copy = copyOrReEncode()

    cmd = f'ffmpeg -i {filePath} {outputPath}/{fileName}.{fileFormat}'

    if copy == True:
        cmd += "-c copy"

print(cmd)
subprocess.call(cmd, shell=True)
