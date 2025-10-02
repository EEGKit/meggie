"""Contains save epochs action handling."""

import os

from PyQt5 import QtWidgets

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.filemanager import homepath

from meggie.mainwindow.dynamic import Action

from meggie.actions.epochs_save.controller.epochs import save_channel_averages
from meggie.actions.epochs_save.controller.epochs import save_all_channels

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class SaveEpochs(Action):
    """Saves epochs items to csv files"""

    def run(self, params={}):
        try:
            selected_name = self.data["outputs"]["epochs"][0]
        except IndexError:
            return

        # validate times
        time_arrays = []
        for subject in self.experiment.subjects.values():
            epochs = subject.epochs.get(selected_name)
            if not epochs:
                continue
            time_arrays.append(epochs.content.times)

        assert_arrays_same(time_arrays, "Times do not match")

        def option_handler(selected_option):

            default_filename = (
                selected_name + "_all_subjects_channel_averages_epochs.csv"
                if selected_option == "channel_averages"
                else selected_name + "_all_subjects_all_channels_epochs.csv"
            )
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.window,
                "Save Epochs to CSV",
                os.path.join(homepath(), default_filename),
                "CSV Files (*.csv);;All Files (*)",
            )
            if not filepath:
                return

            epochs = self.experiment.active_subject.epochs.get(selected_name)
            bstart = epochs.params.get("bstart")
            bend = epochs.params.get("bend")

            params = {
                "name": selected_name,
                "output_option": selected_option,
                "channel_groups": self.experiment.channel_groups,
                "filepath": filepath,
                "bstart": bstart,
                "bend": bend,
            }

            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = OutputOptions(self.window, handler=option_handler)
        dialog.show()

    def handler(self, subject, params):
        """ """
        if params["output_option"] == "channel_averages":
            save_channel_averages(
                self.experiment,
                params["name"],
                params["channel_groups"],
                params["filepath"],
                params["bstart"],
                params["bend"],
                do_meanwhile=self.window.update_ui,
            )
        else:
            save_all_channels(
                self.experiment,
                params["name"],
                params["filepath"],
                params["bstart"],
                params["bend"],
                do_meanwhile=self.window.update_ui,
            )
