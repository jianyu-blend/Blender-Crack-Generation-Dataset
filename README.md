# BCG: synthetic masonry crack dataset

Rendered masonry scenes with automatically generated instance annotations for brick, broken
brick and crack, produced by the Blender Crack Generation (BCG) framework.

| | |
|---|---|
| Images | 4,000 |
| Size | approximately 190 MiB |
| Resolution | 128 x 128 to 640 x 640 |
| Annotation | YOLO segmentation polygons |
| Licence | `<fill in, for example CC BY 4.0>` |
| Generator code | [Blender Crack Generation Code](https://github.com/jianyu-blend/Blender-Crack-Generation-Code) |
| Dataset repository | [Blender Crack Generation Dataset](https://github.com/jianyu-blend/Blender-Crack-Generation-Dataset) |
| Archived release | `<dataset DOI — fill in, optional>` |

## Contents

```
train/images/       <base>_<n>_P.jpg     RGB render
train/labels/       <base>_<n>_P.txt     YOLO polygons, one instance per line
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

`<base>` encodes the generation condition, so the condition of any image can be recovered from
its name alone:

| Part | Values |
|---|---|
| Crack-side motion | `stay`, `translation`, `settling` |
| View range | `close`, `middle`, `far` |
| Crack-width category | `lt3mm`, `3to5mm`, `5to10mm`, `10to30mm`, `gt30mm` |

`<n>` is the camera index. Six views are rendered per wall: three primary cameras, each with a
laterally shifted paired camera at a 0.10 m offset.

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

The dataset trains any YOLO-format instance-segmentation model directly. For the acquisition
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
