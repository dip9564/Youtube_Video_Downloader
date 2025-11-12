import yt_dlp
import sys

def show_formats(url):
    """Fetch and display available formats in a clean way"""
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        print("\n📌 Available formats (simplified):")
        seen = set()
        for f in info.get('formats', []):
            ext = f.get('ext')
            if ext in ["mhtml", None]:  # skip storyboards/thumbnails
                continue

            # Prefer height (so we get 480p, 720p, 1080p etc.)
            if f.get("height"):
                res = f"{f['height']}p"
            else:
                res = "audio only"

            abr = f.get('abr', '')
            key = (res, ext)
            if key in seen:
                continue
            seen.add(key)
            print(f"{f['format_id']:>5} | {res:<10} | {abr if abr else ''} | {ext}")

def main():
    # Ask user for the video URL
    url = input("Enter video URL (YouTube, FB, etc.): ").strip()

    show_formats(url)

# Ask user if they want to continue
    cont = input("\nPress Enter to continue download, or type 'no' to cancel: ").strip().lower()
    if cont == "no" or cont == "n":
        print("❌ Cancelled by user after viewing formats.")
        sys.exit(0)   # exits script


    # Ask user for format
    print("\nChoose output format:")
    print("1. mp4 (video)")
    print("2. mp3 (audio only)")
    print("3. webm (video)")
    format_choice = input("Enter choice (1/2/3): ").strip()

    if format_choice == "1":
        out_format = "mp4"
    elif format_choice == "2":
        out_format = "mp3"
    elif format_choice == "3":
        out_format = "webm"
    else:
        print("Invalid choice, defaulting to mp4.")
        out_format = "mp4"

    # If mp3 chosen, add postprocessor and skip quality selection
    if format_choice == "2":
        ydl_format = "bestaudio/best"
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        # Ask user for quality only if video format
        print("\nChoose video quality:")
        print("1. Best available")
        print("2. 1080p")
        print("3. 720p")
        print("4. 480p")
        quality_choice = input("Enter choice (1-4): ").strip()

        if quality_choice == "1":
            ydl_format = "bestvideo+bestaudio/best"
        elif quality_choice == "2":
            ydl_format = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif quality_choice == "3":
            ydl_format = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif quality_choice == "4":
            ydl_format = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        else:
            print("Invalid choice, defaulting to best available.")
            ydl_format = "bestvideo+bestaudio/best"

        postprocessors = []

    # Download options
    ydl_opts = {
        'format': ydl_format,                # always video+audio if video selected
        'merge_output_format': out_format,   # final file format
        'outtmpl': '/Users/dipmondal/Downloads/Videos/%(title)s.%(ext)s',
        'postprocessors': postprocessors,
    }

    print("\nDownloading...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("\n✅ Download completed!")

if __name__ == "__main__":
    main()
