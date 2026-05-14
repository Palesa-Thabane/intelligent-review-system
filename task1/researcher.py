class Researcher:
    def __init__(self, ui):
        self.ui = ui
    def submitResearchOutput(self, data):
        # 1. Researcher -> UI : submitResearchOutput(data)
        self.ui.submitResearchOutput(data)