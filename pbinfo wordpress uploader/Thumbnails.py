from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import os

WHITE = (255, 255, 255) 

#thumbnail_path = '.\\Thumbnails' # Windows
thumbnail_path = './Thumbnails' # Linux
thumbnail_frame = 'cpp_pbinfo.png'

font_size = 300
#font_path = '.\\Fonts' # Windows
font_path = './Fonts' # Linux
font_name = 'malgunbd.ttf'

save_path = thumbnail_path

#problem_path = '.\\Rezolvari PBInfo' # Windows
problem_path = 'Rezolvari2'  # Linux

# image.size ==> width, height
# width = x
# height = y

def generate_thumbnail_for_problems(problem_files):
	for problem_file in problem_files:
		problem_file = '#' + problem_file.replace('.txt', '')
		problem_tb = Thumbnail_Generator(get_image(thumbnail_path, thumbnail_frame), problem_file, save_path, problem_file, WHITE, get_font(font_path, font_name), font_size)
		problem_tb.create_thumbnail()

def get_image(path, name):
	#return Image.open('{}\\{}'.format(path, name)) # Windows
	return Image.open('{}/{}'.format(path, name)) # Linux

def get_font(path, name):
	#return '{}\\{}'.format(path, name) # Windows
	return '{}/{}'.format(path, name) # Linux

class Thumbnail_Generator:
	def __init__(self, image, file_name, save_path, text, color, font, font_size):
		self.image = image
		self.file_name = file_name
		self.save_path = save_path
		self.text = text
		self.color = color
		self.font = font
		self.font_size = font_size
	
	def center(self):
		x, y = self.image.size
		num_of_letters = len(self.file_name)
		pixels_to_go_left = 60
		if num_of_letters < 3:
			return x // 2 - self.font_size, y // 2 - self.font_size
		else:
			return x // 2 - self.font_size - (num_of_letters - 2) * pixels_to_go_left, y // 2 - self.font_size  
	
	def create_thumbnail(self):
		thumbnail = self.image.copy()
		draw = ImageDraw.Draw(thumbnail)
		font = ImageFont.truetype(self.font, self.font_size)
		draw.text(self.center(), self.text, self.color, font=font)
		#thumbnail.save('{}\\{}.png'.format(self.save_path, self.file_name)) # Windows
		thumbnail.save('{}/{}.png'.format(self.save_path, self.file_name)) # Linux

	def __del__(self):
		self.image.close()


def main():
	generate_thumbnail_for_problems(os.listdir(problem_path))

if __name__ == '__main__':
	main()