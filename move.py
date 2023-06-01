import os
import shutil
import datetime
import exifread

src = r'/Volumes/2tbexternal/tanya_google_drive/Tanya/photo'
dst = r'/Volumes/2tbexternal/tanya_google_drive/Results/'

extensions = ['jpg', 'mov', 'mp4', 'png', 'jpeg', 'gif', 'heic', ]

def move_files(files: list[str]):
    for file in files:
        # If there is no duplicate file present, then move else don't move
        lower_extension = str(file.split('.')[-1]).lower()
        file_name = os.path.basename(file)
        if lower_extension in extensions and file_name[0] != '.':
            path = os.path.join(root, file)
            print("Found a file: "+path)
            # print("Only name of the file: "+file)
            # print("Extension of the file (lower): "+lower_extension)
            move_file(path)

        elif lower_extension == 'json':
            print("Will be deleted: "+os.path.join(root, file))
            try:
                os.remove(os.path.join(root, file))
            except:
                print("Unable to delete: "+os.path.join(root, file))

def move_file(full_file_name:str):
    # source_file_path = os.path.join(source_dir, file_name)
    source_dir = os.path.dirname(full_file_name)
    file_name = os.path.basename(full_file_name)
    print("trying to move: "+full_file_name + " to "+dst)
    try:
        with open(full_file_name, 'rb') as f:
            exif_data = exifread.process_file(f) # type: ignore
            if 'EXIF DateTimeOriginal' not in exif_data:
                timestamp_taken = os.path.getmtime(full_file_name)
                date_taken = datetime.datetime.fromtimestamp(timestamp_taken).strftime('%Y:%m:%d %H:%M:%S')
            else:
                date_taken = exif_data['EXIF DateTimeOriginal'].values
            date_taken_formatted = datetime.datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
            year_folder_path = os.path.join(dst, str(date_taken_formatted.year))
            if not os.path.exists(year_folder_path):
                os.makedirs(year_folder_path)
            month_folder_path = os.path.join(year_folder_path, date_taken_formatted.strftime('%B'))
            if not os.path.exists(month_folder_path):
                os.makedirs(month_folder_path)
            destination_file_path = os.path.join(month_folder_path, file_name)
            print("Will be moved to: "+destination_file_path)
            shutil.move(full_file_name, month_folder_path)
    except Exception as e:
        print("Unable to move: "+full_file_name + "\n error: "+str(e))
        

if __name__ == "__main__":
    for root, subdirs, files in os.walk(src):
        if root != dst:
            move_files(files)
            # dir_move(subdirs)
