# Training demo assets

| File | Content | Use |
| --- | --- | --- |
| `pr-training-diff.png` | The diff of PR #16 in duytq5/active-learning-operation. The PR adds `configs/trainings/2026-10-18-rocole-v2.yaml`: rocole, dataset version 2, timm_classifier with the version 1 settings, base_model null. | The training demo: an ML engineer starts a training job with one PR. |
| `pr-training-diff-annotated.png` | The same diff with 4 numbered boxes and notes. Made by `diagrams/pr_training.py`. | The slide version of the image above. |
| `start-training-runs.png` | The GitHub Actions list. The top run is `start-training` #6 from the merge of PR #17 (commit ac271f8). It passed in 26 s. | The training demo: the merge starts the training job. |
| `start-training-runs-annotated.png` | The same image with 3 numbered boxes in time order (CI on PR #17, CI on main, start-training #6) and notes. Made by `diagrams/start_training.py`. | The slide version of the image above. |
| `mlflow-run.png` | The MLflow run page of training 340ea3ff: metrics, parameters, tags and the registered model rocole-fastvit v3. | The training demo: what the ML engineer sees after training. |
| `mlflow-run-annotated.png` | The same page without the sidebar, with 5 numbered boxes and notes. Made by `diagrams/mlflow_run.py`. | The slide version of the image above. |
