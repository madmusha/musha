import os
import shutil
from PIL import Image
import random

from django.core.files import File


def create_new_thumb(media_path, instance, owner_slug, max_length, max_width):
		filename = os.path.basename(media_path)
		thumb = Image.open(media_path)
		size = (max_length, max_width)
		thumb.thumbnail(size, Image.ANTIALIAS)
		temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, owner_slug)
		if not os.path.exists(temp_loc):
			os.makedirs(temp_loc)
		temp_file_path = os.path.join(temp_loc, filename)
		if os.path.exists(temp_file_path):
			temp_path = os.path.join(temp_loc, "%s" %(random.random()))
			os.makedirs(temp_path)
			temp_file_path = os.path.join(temp_path, filename)

		temp_image = open(temp_file_path, "w")
		thumb.save(temp_image)
		thumb_data = open(temp_file_path, "r")

		thumb_file = File(thumb_data)
		instance.media.save(filename, thumb_file)
		shutil.rmtree(temp_loc, ignore_errors=True)
		return True

def product_post_save_receiver(sender, instance, created, *args, **kwargs):
	if instance.media:
		hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
		sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
		micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

		hd_max = (500, 500)
		sd_max = (350, 350)
		micro_max = (150, 150)

		media_path = instance.media.path
		owner_slug = instance.slug
		if hd_created:
			create_new_thumb(media_path, hd, owner_slug, hd_max[0], hd_max[1])
			# filename = os.path.basename(instance.media.path)
			# thumb = Image.open(instance.media.path)
			# thumb.thumbnail(hd_max, Image.ANTIALIAS)
			# temp_loc = "%s/%s/tmp" %(settings.MEDIA_ROOT, instance.slug)
			# if not os.path.exists(temp_loc):
			# 	os.makedirs(temp_loc)
			# temp_file_path = os.path.join(temp_loc, filename)
			# if os.path.exists(temp_file_path):
			# 	temp_path = os.path.join(temp_loc, "%s" %(random.random()))
			# 	os.makedirs(temp_path)
			# 	temp_file_path = os.path.join(temp_path, filename)

			# temp_image = open(temp_file_path, "w")
			# thumb.save(temp_image)
			# thumb_data = open(temp_file_path, "r")

			# thumb_file = File(thumb_data)
			# hd.media.save(filename, thumb_file)
		
		if sd_created:
			create_new_thumb(media_path, sd, owner_slug, sd_max[0], sd_max[1])

		if micro_created:
			create_new_thumb(media_path, micro, owner_slug, micro_max[0], micro_max[1])








post_save.connect(product_post_save_receiver, sender=Product)