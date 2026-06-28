"""Unit tests for the pure parsing/geometry logic of spritesheet_collage."""

import unittest

from PIL import Image

from spritesheet_collage import (
    Geometry,
    compute_grid,
    extract_frames,
    frame_box,
    parse_collage,
    parse_frames,
    safe_prefix,
)


class ParseFramesTests(unittest.TestCase):
    def test_valid_pairs(self):
        self.assertEqual(
            parse_frames("[[0,0],[1,0],[0,1]]"), [(0, 0), (1, 0), (0, 1)]
        )

    def test_rejects_non_list(self):
        with self.assertRaises(ValueError):
            parse_frames("42")

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            parse_frames("[]")

    def test_rejects_wrong_pair_length(self):
        with self.assertRaises(ValueError):
            parse_frames("[[0,0,0]]")

    def test_rejects_non_integer(self):
        with self.assertRaises(ValueError):
            parse_frames("[[0,'a']]")

    def test_rejects_code_injection_attempt(self):
        # literal_eval must not execute arbitrary expressions.
        with self.assertRaises(ValueError):
            parse_frames("__import__('os').system('echo hi')")


class ParseCollageTests(unittest.TestCase):
    def test_valid_sequence(self):
        self.assertEqual(parse_collage("[1,2,3,2]", 3), [1, 2, 3, 2])

    def test_blank_returns_empty(self):
        self.assertEqual(parse_collage("", 4), [])
        self.assertEqual(parse_collage("   ", 4), [])

    def test_rejects_out_of_range_high(self):
        with self.assertRaises(ValueError):
            parse_collage("[1,5]", 4)

    def test_rejects_zero_or_negative(self):
        with self.assertRaises(ValueError):
            parse_collage("[0,1]", 4)

    def test_rejects_non_integer(self):
        with self.assertRaises(ValueError):
            parse_collage("[1,2.5]", 4)

    def test_rejects_too_long(self):
        with self.assertRaises(ValueError):
            parse_collage("[" + ",".join(["1"] * 5000) + "]", 1)


class ComputeGridTests(unittest.TestCase):
    def test_simple_grid(self):
        # 512x512 sheet, 64px frames, no margin/sep -> 8x8.
        self.assertEqual(compute_grid(512, 512, Geometry(64, 64)), (8, 8))

    def test_with_margin_and_separation(self):
        # 2*margin(2) + 4 frames*10 + 3 gaps*5 = 4 + 40 + 15 = 59 wide.
        geom = Geometry(frame_x=10, frame_y=10, margin_x=2, margin_y=2, sep_x=5, sep_y=5)
        self.assertEqual(compute_grid(59, 59, geom), (4, 4))

    def test_non_integer_raises(self):
        with self.assertRaises(ValueError):
            compute_grid(500, 512, Geometry(64, 64))


class FrameBoxTests(unittest.TestCase):
    def test_top_left(self):
        self.assertEqual(frame_box(0, 0, Geometry(64, 64)), (0, 0, 64, 64))

    def test_offset_cell(self):
        self.assertEqual(frame_box(2, 1, Geometry(64, 64)), (128, 64, 192, 128))

    def test_with_margin_and_separation(self):
        geom = Geometry(frame_x=10, frame_y=10, margin_x=2, margin_y=2, sep_x=5, sep_y=5)
        # margin 2 + col 1 * (10 + 5) = 17
        self.assertEqual(frame_box(1, 1, geom), (17, 17, 27, 27))


class ExtractFramesTests(unittest.TestCase):
    def setUp(self):
        # A 128x128 sheet of 64px frames -> a 2x2 grid.
        self.image = Image.new("RGB", (128, 128))
        self.geom = Geometry(64, 64)

    def test_extracts_requested_cells_in_order(self):
        frames = extract_frames(
            self.image, [(0, 0), (1, 1)], (2, 2), self.geom
        )
        self.assertEqual([f.size for f in frames], [(64, 64), (64, 64)])

    def test_column_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            extract_frames(self.image, [(2, 0)], (2, 2), self.geom)

    def test_row_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            extract_frames(self.image, [(0, 2)], (2, 2), self.geom)

    def test_negative_coordinate_raises(self):
        with self.assertRaises(ValueError):
            extract_frames(self.image, [(-1, 0)], (2, 2), self.geom)


class SafePrefixTests(unittest.TestCase):
    def test_accepts_plain_name(self):
        self.assertEqual(safe_prefix("frame"), "frame")

    def test_rejects_separator(self):
        with self.assertRaises(ValueError):
            safe_prefix("../frame")

    def test_rejects_dot_segments(self):
        with self.assertRaises(ValueError):
            safe_prefix("..")

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            safe_prefix("")


if __name__ == "__main__":
    unittest.main()
