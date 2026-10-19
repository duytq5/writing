# Operator demo assets

| File | Content | Use |
| --- | --- | --- |
| `pr-round-diff.png` | The diff of PR #12 in duytq5/active-learning-operation. The PR adds `configs/rounds/2026-10-18-rocole-third.yaml`: entropy, k 10, model `rocole-fastvit/2`, no training. Every field has its default value and a comment (commit 2f92f88). | The Operator demo: an operator opens a labeling round with one PR. |
| `start-round-runs.png` | The GitHub Actions list of `start-round` runs. The top run is the merge of PR #12 (commit 3493b74). It passed in 25 s. | The Operator demo: the merge starts the round. |
| `start-round-runs-annotated.png` | The same image with the PR #12 run in an orange box and a note. Made by `diagrams/start_round.py`. | The slide version of the image above. |
| `label-studio-projects.png` | The Label Studio page that lists the projects. | The Operator demo: the round's project appears in Label Studio. |
