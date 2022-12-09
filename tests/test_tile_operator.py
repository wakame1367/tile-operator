import os

import numpy as np
from PIL import Image

from tile_operator.operate import TileOperate


def create_tile_operator_instance():
    to = TileOperate(
        tile_url="https://tile.openstreetmap.jp/{z}/{x}/{y}.png",
        file_path="tests/data/test.geojson",
        zoom_level=18,
    )
    return to


def test_tile_coordinates():
    to = create_tile_operator_instance()
    assert to.tile_coords_to_latlon(0, 0) == (-180.0, 85.0511287798066)


def test_bbox():
    to = create_tile_operator_instance()
    bbox = to.bbox.bounds()
    assert bbox[0] == 141.347
    assert bbox[1] == 43.066
    assert bbox[2] == 141.354
    assert bbox[3] == 43.070


def test_tile_list():
    to = create_tile_operator_instance()
    tile_list = to.get_tile_list()
    assert tile_list[0] == (233997, 96254)
    assert tile_list[-1] == (234002, 96258)
    assert len(tile_list) == 30


def test_tile_download():
    to = create_tile_operator_instance()
    tile_list = to.get_tile_list()

    to.download_tile(*tile_list[0])
    assert os.path.exists("./output/18/233997/96254.png")

    test_image = Image.open("./tests/data/96254.png")
    test_array = np.array(test_image, dtype=np.uint8)
    downloaded = Image.open("./output/18/233997/96254.png")
    downloaded_array = np.array(downloaded, dtype=np.uint8)

    np.testing.assert_array_equal(test_array, downloaded_array)

    os.remove("./output/18/233997/96254.png")
