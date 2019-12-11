from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


class PNGFormat:

    title = 'png'
    extensions = ('png',)

    @classmethod
    def size_table(cls,dataset, font):
        """function defining the height and width of columns and lines
        in the dataset"""

        column_width = 0
        line_height = 0
        space_between_columns = 5
        space_between_lines = 5
        for i in range(len(dataset.headers) - 1):
            header_size = font.getsize(str(dataset.headers[i]))
            column_width = max(column_width, header_size[0])
            line_height = max(line_height, header_size[1])
        for d in dataset:
            data_size = font.getsize(str(d[i]))
            column_width = max(column_width, data_size[0])
            line_height = max(line_height, data_size[1])

        column_width += space_between_columns
        line_height += space_between_lines
        return (column_width, line_height)

    @classmethod
    def export_set(cls, dataset):
        """Returns image representation of dataset

        :param dataset: dataset to represent
        :type dataset: tablib.core.Dataset
        """

        font = ImageFont.load_default().font
        (column_width, line_height) = PNGFormat.size_table(dataset,
                font)

        # image creation

        Image.init()
        mode = '1'
        width = column_width * len(dataset.headers)

        # we add tow lines : one for headers, another for spacing

        height = line_height * (len(dataset) + 2)
        color = 255
        img = Image.new(mode=mode, size=(width, height), color=color)
        draw = ImageDraw.Draw(img)

        # drawing on image

        for i in range(len(dataset.headers)):
            draw.text((column_width * i, 0), dataset.headers[i], 0,
                      font=font)
            for i in range(len(dataset)):
                for j in range(len(dataset[i])):
                    draw.text((dataset * j, line_height * (i + 2)),
                              str(dataset[i][j]), 0, font=font)

        # format conversion

        with BytesIO() as f:
            img.save(f, format="png")
            f.seek(0)
            img_jpg = Image.open(f)
        return img_jpg
