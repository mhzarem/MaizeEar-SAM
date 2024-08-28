# MaizeEar-SAM: Zero-Shot Maize Ear Phenotyping

Iowa State University, [AIRA](https://aiira.iastate.edu/) 

![Workflow](Figures/WorkFlow.png)

Our research primarily focuses on extracting the number of kernels per row from raw images of
maize ears. Our workflow begins with extracting the maize ear from the raw image. We
then input this extracted image into the Segment Anything Model (SAM) to identify kernel masks.
After obtaining these masks, we refine them to create a graph of nodes. From this graph, we
determine the shortest path from bottom to top, which is the representative row of maize ear.
Finally, we count the number of kernels in this row and report it as the number of kernels per row
trait. Based on a sample of approximately 150 maize ears selected to represent the entire dataset, we
achieved an R-squared value of around 0.87 for this feature, suggesting that our pipeline
can accurately count the number of kernels per row.

## Getting Started

``python setup.py``

pip install git+https://github.com/facebookresearch/segment-anything.git

pip install opencv-python pycocotools matplotlib onnxruntime onnx

``conda env create -f evn.yml``
