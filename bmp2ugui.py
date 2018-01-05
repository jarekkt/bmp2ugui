from PIL import Image
import argparse

def load_image(filename, resize_width, resize_height):

    image = Image.open(filename, 'r')
    image = image.convert('RGB')

    if resize_width != 0 or resize_height != 0:
        if resize_width == 0 :
            resize_width = image.size[0]
        if resize_height == 0 :
            resize_height = image.size[1]
        image = image.resize((resize_width, resize_height), Image.NEAREST)
    image_data = image.load()

    return image.size[0], image.size[1], image_data



def convert_pixel(image,x,y,colors):
    if colors == 'RGB565':
        r, g, b = image[x, y]
        return ((r >> 3)<<11) | ((g >> 2)<<5) | ((b >> 3))
    else:
        return 0
    return 0

def c_array(filename,name,byte_stream,width,height,length,bpp,colors):

    ii        = 0
    next_line = ''

    file = open(filename, 'wt')

    file.write( str('const uint8_t %s_data[]= {\n ' % name ))

    for idx in range(0, length):
        next_line += str('0x%0.2X' % byte_stream[ii]).lower() + ","
        ii = ii + 1
        if (ii % 16 == 0 or ii == length):
            file.write(next_line)
            file.write('\n')
            next_line = ''

    file.write('};\n')
    file.write('\n')

    file.write( str('const UG_BMP  %s = { (void *)%s_data,%d /* width*/ ,%d /* height */,BMP_%s,BMP_%s };\n' % (name,name,width,height,bpp,colors) ))

def c_stream(image,width,height,bpp,colors):

    ii = 0
    byte_stream = {}

    for y_idx in range(0, height):
        for x_idx in range(0, width):
            if bpp == 'BPP_16' and colors == 'RGB565':
                value565 = convert_pixel(image,x_idx,y_idx,colors)
                byte_stream[ii] = value565 & 0xFF
                byte_stream[ii+1] = (value565 >> 8) & 0xFF
                ii = ii + 2
    return byte_stream,ii

def convert(params):
    width, height, image_data = load_image(params.image, params.width, params.height)
    byte_stream,length = c_stream(image_data,width,height,params.bpp,params.colors)
    c_array(params.output,params.array,byte_stream,width,height,length,params.bpp,params.colors)

def run():

    parser = argparse.ArgumentParser(description='Convert a bitmap image to a C array for uGui')

    parser.add_argument(
            '--width',
            default=0,
            type=int,
            help='Override image width -  use 0 to keep original')

    parser.add_argument(
            '--height',
            default=0,
            type=int,
            help='Override image height -  use 0 to keep original')

    parser.add_argument(
            '--bpp',
            default='BPP_16',
            type=str,
            help='uGui bmp data type - right now only default BPP_16 supported')

    parser.add_argument(
            '--colors',
            default='RGB565',
            type=str,
            help='uGui bmp color coding - right now only default RGB565 supported')

    parser.add_argument(
            '-a', '--array',
            type=str,
            help='C array name')

    parser.add_argument(
            '-f', '--image',
            type=str,
            help='Image file to convert')

    parser.add_argument(
            '-o', '--output',
            type=str,
            help='Output file with conversion')



    params = parser.parse_args()
    convert(params)

if __name__ == '__main__':
    run()





