# Execution verification

The current course build is undergoing native execution validation. A previous
repository's saved results do not validate this build.

The [expected results](../expected/README.md) describe the fixed training dataset.
The [machine-readable status](verification.json) records whether the current five
notebooks have completed two independent full runs. The release runner clears
all notebook outputs, uses fresh Python kernels and restores each daily handoff
before testing the following day.

The final record will identify the actual host, package versions, notebook code
hashes and observed engine reports. Google Colab hosting is reported separately
from local or GitHub Actions execution.
