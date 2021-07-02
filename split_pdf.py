'''Split PDF.'''

import argparse
import logging

from PyPDF2 import PdfFileWriter, PdfFileReader

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('split_pdf')


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'pdf_file',
        type=str,
        help='pdf file to split',
    )
    parser.add_argument(
        'split_points_str',
        type=str,
        help='Comma seperate split points',
    )
    return parser.parse_args()


def _split_pdf():
    args = _get_args()
    pdf_file = args.pdf_file
    split_points_str = args.split_points_str
    split_points = list(map(
        lambda point_str: (int)(point_str),
        split_points_str.split(','),
    ))

    log.info('Splitting "{pdf_file}" at pages {split_points_str}'.format(
        pdf_file=pdf_file,
        split_points_str=', '.join(split_points_str),
    ))
    base_name = pdf_file[:-4]

    reader = PdfFileReader(open(pdf_file, 'rb'))

    n_split_points = len(split_points)
    for i_split_points in range(0, n_split_points - 1):
        i1, i2 = split_points[i_split_points:i_split_points + 2]
        writer = PdfFileWriter()

        for i_page in range(i1 - 1, i2 - 1):
            page = reader.getPage(i_page)
            writer.addPage(page)

        i2_minus = i2 - 1
        split_pdf_file = '{base_name}.pages{i1}-{i2_minus}.pdf'.format(
            base_name=base_name,
            i1=i1,
            i2_minus=i2_minus,
        )
        writer.write(open(split_pdf_file, 'wb'))
        log.info('Wrote pages {i1} to {i2_minus} to "{split_pdf_file}"'.format(
            i1=i1,
            i2_minus=i2_minus,
            split_pdf_file=split_pdf_file,
        ))


if __name__ == '__main__':
    _split_pdf()
