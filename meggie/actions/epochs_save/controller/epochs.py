"""Contains controlling logic for the epochs implementation."""

import logging

import numpy as np

import meggie.utilities.filemanager as filemanager

from meggie.utilities.formats import format_floats
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.threading import threaded


def _average_epochs_to_channel_groups(data, info, ch_names, channel_groups):
    """Averages epochs data to channel groups."""
    all_averaged_data = []
    for epoch_data in data:
        data_labels, averaged_data = average_to_channel_groups(
            epoch_data, info, ch_names, channel_groups
        )
        all_averaged_data.append(averaged_data)
    return data_labels, np.array(all_averaged_data)


@threaded
def save_all_channels(experiment, selected_name, path, bstart, bend):
    """Saves all channels of epochs item to a csv file."""
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        epochs = subject.epochs.get(selected_name)
        if not epochs:
            continue

        mne_epochs = epochs.content.copy()
        if bstart and bend:
            mne_epochs.apply_baseline((bstart, bend))

        column_names = format_floats(mne_epochs.times)

        for epoch_idx, epoch_data in enumerate(mne_epochs.get_data()):
            for ch_idx, ch_name in enumerate(mne_epochs.ch_names):
                if ch_name in mne_epochs.info["bads"]:
                    continue
                csv_data.append(epoch_data[ch_idx].tolist())

                row_desc = (subject.name, epoch_idx, ch_name)
                row_descs.append(row_desc)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)


@threaded
def save_channel_averages(
    experiment, selected_name, channel_groups, path, bstart, bend
):
    """Saves channel averages of epochs item to a csv file."""
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        epochs = subject.epochs.get(selected_name)
        if not epochs:
            continue

        mne_epochs = epochs.content.copy()
        mne_epochs.load_data()
        if bstart and bend:
            mne_epochs.apply_baseline((bstart, bend))

        mne_epochs.drop_channels(mne_epochs.info["bads"])

        data_labels, averaged_data = _average_epochs_to_channel_groups(
            mne_epochs.get_data(), mne_epochs.info, mne_epochs.ch_names, channel_groups
        )

        column_names = format_floats(mne_epochs.times)

        for epoch_idx, epoch_data in enumerate(averaged_data):
            for ch_idx, (ch_type, area) in enumerate(data_labels):
                csv_data.append(epoch_data[ch_idx].tolist())
                row_desc = (subject.name, epoch_idx, ch_type, area)
                row_descs.append(row_desc)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)
