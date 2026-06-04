# `.ts` to `.mp4` converter

Converts all `.ts` files in the `source` folder to MP4 in a `converted` folder. It uses `ffmpeg` with stream copy (`-c:v copy -c:a copy`) for fast, lossless conversion and shows a colorful progress bar via `rich`.

## How it works

1. Finds `.ts`/`.TS` files in `../source` (not recursive).  
2. Runs `ffmpeg -i input.ts -c:v copy -c:a copy -movflags +faststart -y output.mp4`.  
3. Saves MP4s to `../converted` (creates it if missing).  
4. Uses `ffmpeg.exe` next to the script

## Installation

1. Clone the repo:

    ```bash
    git clone https://github.com/imAlessas/ts-to-mp4.git
    cd ts-to-mp4
    ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Get the heavy `ffmpeg` executable (not in the repo):
   - Go to the **Releases** page:  
     `https://github.com/imAlessas/ts-to-mp4/releases/tag/ffmpeg`
   - Download the `ffmpeg.exe` asset from the latest release.
   - Place `ffmpeg.exe` in the **same folder as the script**.  

4. Put your `.ts` files in `../source` relative to the script, then double-click on `convert.bat` file: to start the conversion
