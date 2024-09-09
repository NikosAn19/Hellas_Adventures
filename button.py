import pygame 

# klasi gia koumpia
class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		# pairnei thesi kersora
		pos = pygame.mouse.get_pos()

		# koitame an einai o kersoras panw sto koumpi kai kanei klik
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# apotiposi koumpiou
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

# klasi koumpiou me keimeno
class ButtonText():
	def __init__(self, x, y, image=None, scale=0.5, text='', font_size=20):
		self.clicked = False
		self.text = text
		self.font = pygame.font.Font(None, font_size)
		self.image = None
		self.rect = pygame.Rect(x, y, 0, 0)
		self.scale = 1
		self.selected = False
		self.visible = True

		if image:
			width = image.get_width()
			height = image.get_height()
			self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
			self.rect = self.image.get_rect()
		elif text:
			self.rect = pygame.Rect(x, y, 0, 0)
			self.update_text_rect()

		self.rect.topleft = (x, y)

	def set_text(self, new_text):
		self.text = new_text
		self.update_text_rect()

	def set_image(self, new_image):
		width = new_image.get_width()
		height = new_image.get_height()
		self.image = pygame.transform.scale(new_image, (int(width * self.scale), int(height * self.scale)))
		self.rect = self.image.get_rect(topleft=self.rect.topleft)

	def set_visible(self, visible):
		self.visible = visible

	def update_text_rect(self):
		text_surface = self.font.render(self.text, True, (255, 255, 255))
		self.rect.size = text_surface.get_size()

	def draw(self, surface):
		action = False
		if not self.visible:
			return False

		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		# apotipwsi pliktrou analoga me ton tupo
		if self.image:
			surface.blit(self.image, (self.rect.x, self.rect.y))
		elif self.text:
			text_surface = self.font.render(self.text, True, (255, 255, 255))
			surface.blit(text_surface, (self.rect.x, self.rect.y))

		return action

# koumpia pou xrisimopoiountai ws placeholders gia ta grammata
class ButtonLetter():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.visible = True
		self.x = x
		self.y = y

	def draw(self, surface):
		if not self.visible:
			return False
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, self.rect)

		return action

	def set_visible(self, visible):
		self.visible = visible

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def set_image(self, new_image):
		width = new_image.get_width()
		height = new_image.get_height()
		self.image = pygame.transform.scale(new_image, (int(width * self.scale), int(height * self.scale)))
		self.rect = self.image.get_rect(topleft=self.rect.topleft)

