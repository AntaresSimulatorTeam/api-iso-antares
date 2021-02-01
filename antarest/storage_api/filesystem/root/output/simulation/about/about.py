from antarest.storage_api.filesystem.config.model import Config
from antarest.storage_api.filesystem.folder_node import FolderNode
from antarest.storage_api.filesystem.inode import TREE
from antarest.storage_api.filesystem.root.output.simulation.about.areas import (
    OutputSimulationAboutAreas,
)
from antarest.storage_api.filesystem.root.output.simulation.about.comments import (
    OutputSimulationAboutComments,
)
from antarest.storage_api.filesystem.root.output.simulation.about.links import (
    OutputSimulationAboutLinks,
)
from antarest.storage_api.filesystem.root.output.simulation.about.parameters import (
    OutputSimulationAboutParameters,
)
from antarest.storage_api.filesystem.root.output.simulation.about.study import (
    OutputSimulationAboutStudy,
)


class OutputSimulationAbout(FolderNode):
    def build(self, config: Config) -> TREE:
        children: TREE = {
            "areas": OutputSimulationAboutAreas(config.next_file("areas.txt")),
            "comments": OutputSimulationAboutComments(
                config.next_file("comments.txt")
            ),
            "links": OutputSimulationAboutLinks(config.next_file("links.txt")),
            # TODO "map": OutputSimulationAboutMap(config.next_file("map")),
            "study": OutputSimulationAboutStudy(config.next_file("study.ini")),
            "parameters": OutputSimulationAboutParameters(
                config.next_file("parameters.ini")
            ),
        }
        return children