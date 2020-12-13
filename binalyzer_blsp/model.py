"""
    binalyzer_blsp.model
    ~~~~~~~~~~~~~~~~~~~~

    This module implements models used for binary file representation.
"""


class BinalyzerSymbolInformationNode(object):

    def __init__(self):
        self.id = 'data0'
        self.name = 'WASM FPGA App 0'
        self.visible = True
        self.parent = None
        self.children = []
        self.busy = 0
        self.iconClass: 'variable'
        self.selected: False
        self.expanded: False
