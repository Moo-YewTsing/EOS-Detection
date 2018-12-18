from Unet_box.point_label_creator import point_label_creator
from Unet_box.point_to_maskor import point2mask
from Unet_box.tile_creator import creat_tiles
from os.path import join
from sys import argv
from clear_name import clear

def from_point_to_tiles(imgs_p, labels_p, dst):
    junk_p = join(dst, 'junk')
    clear(imgs_p, junk_p)
    clear(labels_p, junk_p)
    print('Clear Name Done! Begin to Create Point Labels!')
    point_labels_p = join(dst, 'point_labels')
    point_label_creator(imgs_p, labels_p, point_labels_p)
    print('Point Labels Creation Done! Begin to Create Masks!')
    masks_p = join(dst, 'created_masks')
    point2mask(imgs_p, point_labels_p, masks_p)
    print('Creating Masks Done! Begin to Create tiles!')
    tiles_p = join(dst, 'tiles')
    creat_tiles(imgs_p, masks_p, tiles_p)
    print('All Done!')
    
if __name__ == "__main__":
    imgs_p, labels_p, dst = argv[1], argv[2], argv[3]
    from_point_to_tiles(imgs_p, labels_p, dst)