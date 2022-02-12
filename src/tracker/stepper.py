class Stepper:
    
    def __init__(self) -> None:
        self.current_pos = 0 #angle (rad) from angle origin
        pass

	def setPos(self) -> None:
		self.current_pos = 0
	
	def getPos(self) -> None:
		return self.current_pos

	def Step(self, x, clk_wise=True) -> None: #x=number of steps
		#actuate motor function here
		self.getPos()

	def MoveTo(self, a) -> None: #a=angle in rads
		pass #self.getPos() - a (convert into steps and then Step that many)