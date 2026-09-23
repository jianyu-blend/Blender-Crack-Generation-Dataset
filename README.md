# BCG: synthetic masonry crack dataset

Rendered masonry scenes with automatically generated instance annotations for brick, broken
brick and crack, produced by the Blender Crack Generation (BCG) framework.

| | |
|---|---|
| Images | 4,000 |
| Size | approximately 190 MiB |
| Resolution | 128 x 128 to 640 x 640 |
| Annotation | YOLO segmentation polygons |
| Licence | CC BY 4.0 |
| Generator code | [Blender Crack Generation Code](https://github.com/jianyu-blend/Blender-Crack-Generation-Code) |
| Dataset repository | [Blender Crack Generation Dataset](https://github.com/jianyu-blend/Blender-Crack-Generation-Dataset) |

## Examples

<table>
  <tr>
    <td><img src="examples/generated_light_brick.jpg" alt="Light brick wall" width="140" height="140"></td>
    <td><img src="examples/generated_grey_brick.jpg" alt="Grey brick wall" width="140" height="140"></td>
    <td><img src="examples/generated_weathered_red_brick.jpg" alt="Weathered red brick wall" width="140" height="140"></td>
    <td><img src="examples/generated_dark_oblique.jpg" alt="Oblique view of dark brick wall" width="140" height="140"></td>
    <td><img src="examples/generated_red_oblique.jpg" alt="Oblique view of red brick wall" width="140" height="140"></td>
    <td><img src="examples/generated_blue_oblique.jpg" alt="Oblique view of blue-grey brick wall" width="140" height="140"></td>
  </tr>
</table>

## Contents

```
train/images/       <base>_<n>_P.jpg     RGB render
train/labels/       <base>_<n>_P.txt     YOLO polygons, one instance per line
examples/           six representative RGB previews
data.yaml           class names, in the order below
```

| Class id | Name | Meaning |
|---|---|---|
| 0 | brick | An intact masonry unit |
| 1 | broken_brick | A unit the crack path passes through |
| 2 | crack | The crack opening |

Mortar and background carry no annotation. Each label line is
`class_id x1 y1 x2 y2 ... xn yn`, with coordinates normalised to [0, 1].

The rendered label masks used to produce these polygons are not part of the release; the
polygons are the annotation. The converter that turns a label render into polygons is
`masks_to_yolo_polygons.py` in the code repository.

## Filenames

Each image and its label use the same filename stem. The `.rf.<hash>` suffix was added during
the YOLO export. Filenames identify pairs but should not be treated as generation metadata.

Cracks narrower than 3 mm carry no Boolean geometry; they come from the procedural material
textures. Images in every width group may therefore also contain texture-based cracks below
3 mm.

## How the data was produced

Each scene is built from a procedural masonry layout, a crack path sampled under a
layout-conditioned probability map learned from real annotation masks, and Boolean crack
geometry subtracted from the brick and mortar meshes. Wall geometry, material appearance,
lighting, camera pose and crack morphology are randomised per scene. The RGB pass and the label
pass share the scene state and the camera, so the two outputs are aligned by construction.

The generator is in the code repository above.

## Generating your own data

Users are encouraged to generate their own synthetic images with the BCG pipeline, especially
when additional samples or different scene distributions are required. The complete generation
code and step-by-step instructions are available in the
[Blender Crack Generation Code repository](https://github.com/jianyu-blend/Blender-Crack-Generation-Code).

## Using it

The repository is a synthetic training pool in YOLO segmentation format. For the acquisition
loop in the code repository, point the configuration at this directory:

```yaml
downstream:
  synthetic_pool: /path/to/bcg-dataset
```

## Real images

The real masonry images used to develop the generator and to evaluate the downstream models
come from MCrack1300 and are not redistributed here.

> Ye, Z., Lovell, L., Faramarzi, A. and Ninic, J. (2024). SAM-based instance segmentation
> models for the automation of structural damage detection. *Advanced Engineering Informatics*
> 62, 102826. [doi:10.1016/j.aei.2024.102826](https://doi.org/10.1016/j.aei.2024.102826) ·
> [arXiv:2401.15266](https://arxiv.org/abs/2401.15266)
