import os
from pyzbar.pyzbar import decode as qr_decode
from PIL import Image

def rename_files_based_on_qr_code(directory):
    """
    this function read the png or jpg or jpeg files of the input folder and if it finds the qr code in that image rename the file based on the qr code

    :param directory: directory that we want to change the name of file based on the qr code
    """

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
    
        # Check if the file is an image
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Load the image using PIL (Python Imaging Library)
        image = Image.open(file_path)
        try: 
            # Decode the QR codes in the image using pyzbar
            decoded_qr_codes = qr_decode(image)
    
            # if our file have the only one item ,or it has the multi qr code but all of them is the same
            qr_code_data = [item.data.decode('utf-8') for item in decoded_qr_codes]
            sanity = all(item == qr_code_data[0] for item in qr_code_data)
    
            if sanity:
                qr_data = decoded_qr_codes[0].data.decode('utf-8')
                new_filename = f"{qr_data}.png"
                new_file_path = os.path.join(directory, new_filename)
                os.rename(file_path, new_file_path)
                # print(f"Renamed {file_path} to {new_file_path}")
            else:
                print(f"No QR code or multiple QR codes found in {file_path}")
        except Exception as e:
            print(f"Error occurred while processing {file_path}: {str(e)}")
            

if __name__ == '__main__':
    rename_files_based_on_qr_code('../Data/crop_test_image/Raw')