from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging
#watchdog lib lsns to all the changes in the file system 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#move files from Downloads to respective folders 
src_dir = "C:/Users/Asus/Downloads"
dest_dir_image = "C:/Users/Asus/Downloads/images"
dest_dir_audio = "C:/Users/Asus/Downloads/audio"
dest_dir_video = "C:/Users/Asus/Downloads/video"
dest_dir_doc = "C:/Users/Asus/Downloads/documents"
dest_dir_others = "C:/Users/Asus/Downloads/otherfiles"

#image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
#Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
#Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

#Document types
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

def assign_unique_name(dest,name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
        file_exists = exists(f"{dest}/{name}")
        if file_exists :
                unique_name = assign_unique_name(dest, name)
                old_name = join(dest, name)
                new_name = join(dest, unique_name)
                rename(old_name,new_name)
        move(entry,dest)

class MoveHandler(FileSystemEventHandler):
    #on_modified is an inbuilt function that performs task once file loc modified!
        def on_modified(self,event):
                with scandir(src_dir) as entries: #scandir iterators the file entries in dir at specifies path.
                        for entry in entries:
                                name = entry.name
                                self.checkImage(entry,name)
                                self.checkVideo(entry,name)
                                self.checkAudio(entry,name)
                                self.checkDoc(entry,name)
                                self.otherfiles(entry,name)

        def checkImage(self,entry,name):
                for image_extension in image_extensions:
                        if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                                move_file(dest_dir_image,entry,name)
                                logging.info("Image moved in {name}") #logs msg to help debug
                            

        def checkVideo(self,entry,name):
                for video_extension in video_extensions:
                        if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                                des = dest_dir_video
                                move_file(des,entry,name)
                                logging.info("Video moved in {name}")

        def checkAudio(self,entry,name):
                for audio_extension in audio_extensions:
                        if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                                des = dest_dir_audio
                                move_file(des,entry,name)
                                logging.info("Audio moved in {name}")

        def checkDoc(self,entry,name):
                for document_extension in document_extensions:
                        if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                                des = dest_dir_doc
                                move_file(des,entry,name)
                                logging.info("Document moved in {name}")
                                

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = src_dir
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
