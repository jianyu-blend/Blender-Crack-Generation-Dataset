# Selected synthetic crack subset

This directory contains 4000 image/YOLO-label pairs selected from
`Crack_Synthetic_20072026.v1i.yolov8`. The original dataset was not modified.

Selection first removes unreadable, invalid-label, almost-black, almost-white, near-uniform
and extremely blurred samples. A robust score ranks exposure, contrast, entropy, sharpness,
dynamic range and crack visibility. The selector then keeps one image per wall/crack group
before adding extra views, rejects perceptual near-duplicates with pHash and dHash, and
prioritises under-represented visual clusters.

See `selection_report.json`, `selection_manifest.csv` and `all_quality_metrics.csv` for the
audit trail.

The three visual contact sheets are stored beside this directory in
`Crack_Synthetic_20072026_selected_4000.v1i.yolov8_audit` so they cannot be mistaken for
training images during upload.
