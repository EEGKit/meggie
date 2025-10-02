from meggie.utilities.testing import BaseTestAction
from meggie.actions.epochs_save import SaveEpochs
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestEpochsSaveAllChannels(BaseTestAction):
    def test_epochs_save_all_channels(self):

        data = {"outputs": {"epochs": ["Epochs"]}}

        self.run_action(
            action_name="epochs_save",
            handler=SaveEpochs,
            data=data,
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
