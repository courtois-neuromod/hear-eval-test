import matplotlib.pyplot as plt
import numpy as np
import os
import json
import warnings
warnings.filterwarnings("ignore")

# TODO: this needs to be filled for each dataset
# because the score differ for each dataset, we need to define the relation for each
KEY_DATASET_SCORE = {
    'esc50-v2.0.0-full': "aggregated_scores", 'fsd50k-v1.0-full': "test"}


def plot_metric(metric_name, result_path="embeddings/soundnetbrain_hear/", figure_path="reports/figures"):

    models = ["voxels_conv4", "voxels_conv5", "voxels_noft"]
    datasets = [dataset for dataset in os.listdir(
        os.path.join(result_path, models[0], "soundnetbrain_hear"))]
    metric_results = np.zeros((len(models), len(datasets)))
    for ii, model in enumerate(models):
        for jj, dataset in enumerate(datasets):
            result_filepath = os.path.join(
                result_path, model, "soundnetbrain_hear",  dataset, "test.predicted-scores.json")
            with open(result_filepath) as f:
                data = json.load(f)
                if metric_name in data[KEY_DATASET_SCORE[dataset]]:
                    score = data[KEY_DATASET_SCORE[dataset]][metric_name]
                    msg = f"{metric_name} for {dataset} and {model}:\t{score}"
                else:
                    score = data[KEY_DATASET_SCORE[dataset]
                                 ][metric_name + "_mean"]
                    msg = f"{metric_name}_mean" + \
                        f" for {dataset} and {model}: {score}"
                print(msg)
            metric_results[ii, jj] = score

    fig, ax = plt.subplots()
    cax = ax.matshow(metric_results)
    for (i, j), z in np.ndenumerate(metric_results):
        ax.text(j, i, '{:0.3f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    fig.colorbar(cax)
    ax.xaxis.set_ticklabels([''] + datasets)
    ax.yaxis.set_ticklabels([''] + models)
    ax.set_title(
        f"{metric_name} or {metric_name}_mean for all datasets and models")
    plt.savefig(os.path.join(figure_path, "metrics.png"), bbox_inches='tight')


if __name__ == "__main__":

    root_dir = os.path.join(os.path.dirname(__file__), "..")
    results_path = os.path.join(root_dir, "embeddings", "soundnetbrain_hear")
    figure_path = os.path.join(root_dir, "reports", "figures")
    plot_metric("test_aucroc", results_path, figure_path)
