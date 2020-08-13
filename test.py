import exifread
from exif import Image

path = './img/DSCF4845.JPG'
#path = './img/DSCF4845.RAF'

f = open(path, 'rb')
exifData = exifread.process_file(f, details=False)
f.close()
print(exifData)


with open(path,  'rb') as file:
    img = Image(file)

print(dir(img))

print(img.focal_length)
print(img.f_number)
print(img.exposure_time)
print(img.photographic_sensitivity)