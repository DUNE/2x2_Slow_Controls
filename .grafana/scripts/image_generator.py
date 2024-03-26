import os
import shutil
import time

def move_gif(source_dir, target_dir):
    try:
        gif_files = [f for f in os.listdir(source_dir) if f.endswith('.gif')]
        for gif_file in gif_files:
            source_path = os.path.join(source_dir, gif_file)
            target_path = os.path.join(target_dir, "testplot.gif")
            shutil.copyfile(source_path, target_path)
            print(f"Moved {source_path} to {target_path}")
            time.sleep(10)
            os.remove(target_path)  # Delete the existing file
    except Exception as e:
        print(f"Error moving GIF file: {e}")

def main():
    source_dir = "/home/nfs/minerva/dqmtest_alysia/gmbrowser/www"
    target_dir = "/data/grafana/Mx2"
    move_gif(source_dir, target_dir)

if __name__ == "__main__":
    main()
