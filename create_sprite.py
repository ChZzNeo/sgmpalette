import argparse
import os
from PIL import Image, ImageChops, ImageMath

def create_sprite(name, width=-1, differentiator='RGB', fallback=False):
    '''
    Generates a palettized image from input images in the same folder.
    The inputs can be: raw image, base colors, color map, and detail layer
                   or: shadows, highlights, color map, and detail layer.
    Parameters:
    - name
      base name of input files
    - width
      <0: downscale such that diagonal is ~666 (preserve size if original diagonal is <666)
      =0: preserve size
      >0: resize to specified width
    - differentiator
      ='R': only consider the red channel when making the color map
      ='RGB': differentiate all colors when making the color map
    - fallback
      True: run with color map in palette mode
      False: run normally with color map unmodified
    '''
    area = Image.open(name + '_area.png').convert('RGBA') # color map
    if fallback:
        area = area.convert('P').convert('RGBA')
    line = Image.open(name + '_line.png').convert('RGBA') # detail layer
    try:
        shadow = Image.open(name + '_shadow.png').convert('RGBA')
        highlight = Image.open(name + '_highlight.png').convert('RGBA')
    except:
        raw = Image.open(name + '_raw.png').convert('RGBA') # raw image
        base = Image.open(name + '_base.png').convert('RGBA') # base colors
        shadow = ImageChops.subtract(base, raw)
        highlight = ImageChops.subtract(raw, base)
    
    if differentiator == 'R':
        r = area.getchannel(0).convert('L')
    elif differentiator == 'RGB':
        copy = Image.new('RGB', area.size)
        copy.paste(area, mask=area) # paste removes color info in transparent areas
        data = copy.getdata()
        colors1 = {(a, b, c, 0) for a, b, c in data} - {(0, 0, 0, 0)}
        colors2 = set()
        colormap = {0: (0, 0, 0)}
        while len(colors1) > 0 and len(colormap) < 256:
            for a, b, c, d in colors1:
                if a not in colormap:
                    colormap[a] = ((a - d) % 256, b, c)
                else:
                    colors2.add(((a + 1) % 256, b, c, d + 1))
            colors1 = colors2.copy()
            colors2.clear()
        if len(colors1):
            print('Color limit exceeded; colors excluded:', colors1)
            print('Trying again with color map in palette mode.')
            return create_sprite(name, width, differentiator, True)
        colormapinverse = {colormap[i]: i for i in colormap}
        rdata = [colormapinverse[i] for i in data]
        r = Image.new('L', area.size)
        r.putdata(rdata)
    else:
        print('Unsupported differentiator:', differentiator)
        return

    g = ImageMath.eval('convert(0xff - line, "L")', line=line.getchannel(3).convert('L'))
    b = ImageMath.eval(
        'convert(0xff - (area > 0) * (shadow * (0xff - 0x33) / 0x80) + (area > 0) * ((highlight - 0x33) * 0x33 / 0x40), "L")',
        area=area.convert('L'),
        shadow=shadow.convert('L'),
        highlight=highlight.convert('L')
    )

    if width < 0:
        diagonal = 666
        area_diagonal = (area.width ** 2 + area.height ** 2) ** 0.5
        width = min(area.width, int(area.width * diagonal / area_diagonal))
    newsize = tuple(int(x * width / area.width) for x in area.size)

    rgb = Image.merge('RGB', (
        r if width == 0 else r.resize(newsize, Image.NEAREST),
        g if width == 0 else g.resize(newsize), # set resample to Image.NEAREST if area has gaps
        b if width == 0 else b.resize(newsize)
    ))

    path = 'sprite/custom' + name + '.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rgb.save(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, help='base name')
    parser.add_argument('-w', '--width', type=int, default=-1, help='width (px)')
    parser.add_argument('-d', '--differentiator', type=str, default='RGB', help='differentiator (R or RGB)')
    args = parser.parse_args()
    create_sprite(args.name, args.width, args.differentiator)
