import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from render import SCENE_GROUPS, QUALITY_DIRS

def stitch_videos(video_paths: list[Path], output_filename: str):
    if not video_paths:
        print("No videos to stitch!")
        return

    missing = [p for p in video_paths if not p.exists()]
    if missing:
        print("Error: The following videos are missing. Render them first!")
        for m in missing:
            print(f" - {m}")
        sys.exit(1)

    print(f"\n--- Stitching {len(video_paths)} videos into {output_filename} ---\n")
    list_file = ROOT / "concat_list.txt"
    
    with open(list_file, "w", encoding="utf-8") as f:
        for vp in video_paths:
            vp_safe = str(vp.resolve()).replace("\\", "/")
            f.write(f"file '{vp_safe}'\n")
    
    cmd = [
        "ffmpeg", "-y", 
        "-f", "concat", 
        "-safe", "0", 
        "-i", str(list_file), 
        "-c", "copy", 
        output_filename
    ]
    
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print(f"\nDONE! Full video is ready at: {ROOT / output_filename}\n")
    else:
        print(f"\nFFmpeg stitching failed for {output_filename}\n")
        
    if list_file.exists():
        list_file.unlink()

def main():
    parser = argparse.ArgumentParser(description="Stitch rendered scenes into a full video")
    parser.add_argument(
        "--video", 
        choices=["1", "2", "3", "4", "all"], 
        required=True,
        help="Which video group to stitch"
    )
    quality_group = parser.add_mutually_exclusive_group()
    quality_group.add_argument("-ql", dest="quality_flag", action="store_const", const="-ql", help="Low quality.")
    quality_group.add_argument("-qm", dest="quality_flag", action="store_const", const="-qm", help="Medium quality.")
    quality_group.add_argument("-qh", dest="quality_flag", action="store_const", const="-qh", help="High quality.")
    parser.add_argument("--output", help="Output filename (e.g., Tutorial_Part3.mp4)")
    args = parser.parse_args()

    quality_flag = args.quality_flag or "-qm"
    quality_dir = QUALITY_DIRS[quality_flag]
    
    scene_pool = SCENE_GROUPS[args.video]
    
    video_paths = []
    for file_name, scene_name in scene_pool:
        if "video_01" in file_name:
            media_dir = "video_01"
        elif "video_02" in file_name:
            media_dir = "video_02"
        elif "video_03" in file_name:
            media_dir = "video_03"
        elif "video_04" in file_name:
            media_dir = "video_04"
        else:
            media_dir = ""
            
        stem = Path(file_name).stem
        path = ROOT / "media" / media_dir / "videos" / stem / quality_dir / f"{scene_name}.mp4"
        video_paths.append(path)
        
    output_filename = args.output or f"Full_Video_{args.video}_{quality_dir}.mp4"
    stitch_videos(video_paths, output_filename)

if __name__ == "__main__":
    main()
