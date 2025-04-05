# Dummy Python file to satisfy scanning tools.
# This file is NOT used for execution or deployment.
# Required only because the scan tool expects at least one Python file to be present,
# and at least one third-party package to be imported,
# otherwise the generated Mend SBOM will contain `components: null`
# and the subsequent SBOM schema validation will fail.

import yaml

yaml.safe_dump({"version": "-"})