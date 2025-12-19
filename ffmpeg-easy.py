import os
import json
import subprocess
from pathlib import Path

copyAllowList = [1, 8, 12, 17]


def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


filePath = input("enter your video / audio path:\n")
clearTerminal()

while True:
    select = int(input("what do you want to do?\n\n"
                       "- edit video & audio\n[1] convert video / audio\n[2] cut video / audio\n[3] crop video\n[4] turn and mirror\n"
                       "[5] change speed\n[6] create gif from video\n[7] blur a video (part or full video)\n[8] embed or extract subtitles\n"
                       "[9] combine several videos into one\n[10] convert image to video (still image video)\n\n- edit audio\n[11] change volume\n"
                       "[12] extract audio from a video\n[13] add or replace audio in a video\n[14] change pitch & speed\n\n-effects & filters\n"
                       "[15] make video black & white\n[16] add text & watermark\n\n[17] record YouTube livestream\n"))

    if select in range(1, 18):
        break
    clearTerminal()
    print("[!] enter a valid option!")

clearTerminal()


def videoFormat():
    fileFormat = input("enter the file format to which you want to convert your file\n"
                       "e.g. mp4, mp3, mkv\n"
                       "(to see all supported file formats run 'ffmpeg -codecs' or 'ffmpeg -formats')\n").lower().strip()
    clearTerminal()
    return fileFormat


def getStartEndT():
    startTime = input("use hh:mm:ss format!\nenter time where the video should start:\n")
    endTime = input("enter time where the video should end:\n")
    clearTerminal()
    return startTime, endTime


def timeToSec(time):
    h, m, s = time.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def getOutputPath():
    downloadLocation = int(input(f"select download location:\n[1] current folder - {os.getcwd()}\n[2] different location\n"))
    clearTerminal()

    if downloadLocation == 2:

        currentDir = os.getcwd()
        count = 0

        print(f"subfolders of {currentDir}:\n")

        folders = [folder for folder in os.listdir(currentDir) if os.path.isdir(os.path.join(currentDir, folder))]

        for folder in folders:
            count += 1
            print(f"[{count}]📁 {folder}")

        outputPath = input("\nselect a folder or enter full path to the desired location:\n")

        if outputPath.isdigit() and outputPath <= str(len(folders)):
            outputPath = os.path.join(currentDir, folders[int(outputPath) - 1])
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
    hi = input("[1] keep original codecs (copy - no quality loss, much faster, but not always supported)\n or\n[2] re-encode?\n")
    clearTerminal()
    if hi == "1":
        copy = " -c copy"
    else:
        copy = ""
    return copy

# maybe unnecessary but ignore pls


fileName = getFileName()

# very custom but yea ignore too
if select != 6:
    fileFormat = videoFormat()
else:
    fileFormat = "gif"

outputPath = getOutputPath()

if select in copyAllowList:
    copy = copyOrReEncode()

fullOutputPath = os.path.join(outputPath, f'{fileName}.{fileFormat}')

cmd = f'ffmpeg -i {filePath} '

if select == 1:

    cmd += f'{filePath} {copy}'

if select == 2:

    startTime, endTime = getStartEndT()
    clearTerminal()

    cmd += f'-ss {startTime} -to {endTime}'

if select == 3:
    x = input("enter the aspect ratio width (e.g., 9 for 9:16):\n")
    y = input("enter the aspect ratio height (e.g., 16 for 9:16):\n")

    cmd += f'-vf "crop=in_h*{x}/{y}:in_h"'

if select == 4:
    while (q := int(input(f"what do you want to do?\n"
                          "[1] rotate 90° clockwise\n"
                          "[2] rotate 90° counterclockwise\n"
                          "[3] rotate 180° clockwise\n"
                          "[4] rotate 180° counterclockwise\n"
                          "[5] rotate 270° clockwise\n"
                          "[6] rotate 270° counterclockwise\n"
                          "[7] flip horizontally\n"
                          "[8] flip vertically\n"))) not in range(1, 9):
        clearTerminal()
        print("[!] enter a valid option!")
    clearTerminal()

    if q == "1":
        cmd += '-vf "transpose=2"'
    if q == "2":
        cmd += '-vf "transpose=1"'
    if q == "3":
        cmd += '-vf "rotate=-PI"'
    if q == "4":
        cmd += '-vf "rotate=PI"'
    if q == "5":
        cmd += '-vf "rotate=-3*PI/2"'
    if q == "6":
        cmd += '-vf "rotate=3*PI/2"'
    if q == "7":
        cmd += '-vf "hflip"'
    if q == "8":
        cmd += '-vf "vflip"'

if select == 5:
    q = int(input(f"Enter playback speed:\n"
                  "- Negative values slow down the video (e.g. -4 means 4x slower or 0.25x speed)\n"
                  "- Positive values speed up the video (e.g. 3 means 3x faster)\n"
                  "- Zero is not allowed\n"
                  "Your choice: "))
    clearTerminal()

    if q > 0:
        setptsFilter = f"setpts=PTS/{q}"
    else:
        setptsFilter = f"setpts=PTS*{abs(q)}"

    audioFactor = q if q > 0 else 1 / abs(q)

    atempoFilter = ""
    tempFactor = audioFactor

    while tempFactor > 2:
        atempoFilter += "atempo=2,"
        tempFactor /= 2

    while tempFactor < 0.5:
        atempoFilter += "atempo=0.5,"
        tempFactor *= 2

    tempFactor = round(tempFactor, 3)
    atempoFilter += f"atempo={tempFactor}"

    cmd += f'-filter:v "{setptsFilter}" -filter:a "{atempoFilter}"'

if select == 6:
    while (q := int(input(f"[1] use only part of the video as a GIF\nor\n[2] use a whole short video as a GIF\n"))) not in range(1, 3):
        clearTerminal()
        print("[!] enter a valid option!")
    clearTerminal()

    if q == 1:
        startTime, endTime = getStartEndT()
        cmd += f'-ss {startTime} -to {endTime} -vf "fps=15,scale=600:-1:flags=lanczos"'

    if q == 2:
        cmd += f'-vf "fps=15,scale=600:-1:flags=lanczos"'

if select == 7:
    while (q := int(input(f"[1] only blur a part of the video (from minute x to y)\nor\n[2] blur full video\n"))) not in range(1, 3):
        clearTerminal()
        print("[!] enter a valid option!")
    clearTerminal()

    while (q2 := int(input(f"[1] only blur a specific area of the video\nor\n[2] fullscreen blur\n"))) not in range(1, 3):
        clearTerminal()
        print("[!] enter a valid option!")
    clearTerminal()

    while (q3 := int(input(f"enter blur strength:\n"
                           "3-5    = very light   | soften noise, subtle smoothing\n"
                           "8-12   = moderate     | soften ui elements, mild anonymizing\n"
                           "15-20  = strong       | hide text, clear anonymizing\n"
                           "25-35  = very strong  | hide faces or license plates\n"
                           "40-60  = extreme      | full anonymization\n"
                           "80-120 = massive      | shapes only, no details left\n"))) not in range(3, 121):
        clearTerminal()
        print("[!] enter a valid option!")
    clearTerminal()

    if q == 1:
        startTime, endTime = getStartEndT()
        startTime = timeToSec(startTime)
        endTime = timeToSec(endTime)

    if q2 == 1:
        ffprobeCmd = f"ffprobe -v quiet -print_format json -show_streams {filePath}"
        probe = subprocess.run(ffprobeCmd, shell=True, stdout=subprocess.PIPE, text=True)
        data = json.loads(probe.stdout)

        for s in data["streams"]:
            if s.get("codec_type") == "video":
                width, height = s["width"], s["height"]
                break

        print("video resolution:", width, "x", height,
              "\nif you don't know how to to enter the coordinates for the blur area you want ask ChatGPT:\n"
              "i need the correct crop coordinates for an FFmpeg rectangular blur.\n"
              "video resolution is [WIDTHxHEIGHT]. blur should be at [POSITION] and roughly [SIZE].\n"
              "give me an extremely short answer with only the correct values like this: w = .. h = .. x = .. y = ..\n"
              "after ChatGPT answered hit return")
        w = input("w coordinate: ")
        h = input("h coordinate: ")
        x = input("x coordinate: ")
        y = input("y coordinate: ")

    cmd += '-filter_complex '

    if q == 2 and q2 == 2:
        cmd += f'"boxblur={q3}:1"'

    if q == 1 and q2 == 2:
        cmd += f'"boxblur={q3}:1:enable=\'gte(t,{startTime})*lte(t,{endTime})\'" '

    if q == 2 and q2 == 1:
        cmd += f'"[0:v]crop={w}:{h}:{x}:{y},boxblur={q3}:1[b]; [0:v][b]overlay={x}:{y}"'

    if q == 1 and q2 == 1:
        cmd += f'"[0:v]crop={w}:{h}:{x}:{y},boxblur={q3}:1:enable=\'gte(t,{startTime})*lte(t,{endTime})\'[b]; [0:v][b]overlay={x}:{y}"'

if select == 8:
    while (q := int(input(f"[1] extract subtitles\n"
                          "[2] add subtitles inside the video as a selectable subtitle track\n"
                          "[3] add subtitles directly into the video image\n"))) not in range(1, 4):
        clearTerminal()
        print("[!] enter a valid option!")
    clearTerminal()

    if q == 1:
        while (q2 := int(input(f"[1] use the first subtitle track (default)\n"
                               "[2] choose a different subtitle track\n"
                               "[3] export all subtitle tracks\n"))) not in range(1, 4):
            clearTerminal()
            print("[!] enter a valid option!")
    clearTerminal()

    if q2 == 1:
        cmd += f'-map 0:s:0 subtitle.srt'

    if q2 == 2:
        probe = subprocess.run(
            f"ffprobe -v error -select_streams s -show_entries stream=index,codec_name:stream_tags=language {filePath}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        print(probe.stdout)


cmd += " " + fullOutputPath

print(cmd)
subprocess.call(cmd, shell=True)
