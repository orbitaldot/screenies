import dotenv
import ftplib
import os
import sys

from PIL import Image

dotenv.load_dotenv()

def stich(top, bottom, output):
    top_img = Image.open(top)
    bottom_img = Image.open(bottom)

    width, height = top_img.size
    new_width = width
    new_height = height * 2

    new_im = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    new_im.paste(top_img , (0, 0))
    new_im.paste(bottom_img , (int((new_width - bottom_img .size[0])/2), height))
    new_im.save(output)


if __name__ == "__main__":
    try:
        FTP_IP = os.getenv("FTP_IP")
        FTP_PORT = int(os.getenv("FTP_PORT"))
        SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR")
    except KeyError:
        print(".env not set up correctly")
        sys.exit(1)

    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    if out_dir[-1] == "/":
        out_dir = out_dir[:-1]
    if not os.path.exists(out_dir):
        print(f"Output directory {out_dir} does not exist")
        sys.exit(1)
    
    ftp = ftplib.FTP()
    ftp.connect(FTP_IP, FTP_PORT)
    ftp.cwd(SCREENSHOTS_DIR)

    imgs = ftp.nlst()
    images = {} # tuples of (top, bottom)
    for img in imgs:
        name = img.strip("_top.bmp").strip("_bot.bmp")
        if name not in images:
            images[name] = [None, None]
        if "_top.bmp" in img:
            images[name][0] = img
        elif "_bot.bmp" in img:
            images[name][1] = img

    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    try:
        for name in images:
            output_filename = name.replace(SCREENSHOTS_DIR, "") + ".png"
            output_file = out_dir + "/" + output_filename

            if os.path.exists(output_file):
                print(f"Skipping {output_filename}")
                continue

            top, bottom = images[name]
            if top is not None and bottom is not None:
                with open("tmp/top.bmp", "wb") as f:
                    ftp.retrbinary("RETR " + top, f.write)
                with open("tmp/bottom.bmp", "wb") as f:
                    ftp.retrbinary("RETR " + bottom, f.write)
                stich("tmp/top.bmp", "tmp/bottom.bmp", output_file)
    except Exception as e:
        print(e)       
    finally:
        import shutil
        shutil.rmtree("tmp")
    
    ftp.quit()
        