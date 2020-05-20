import pygame

protag = pygame.Rect(10, 10, 45, 45)

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT:
          protag.move_ip(10,0)
      if event.key == pygame.K_LEFT:
          protag.move_ip(-10,0)
      if event.key == pygame.K_UP:
          protag.move_ip(0,-10)
      if event.key == pygame.K_DOWN:
          protag.move_ip(0,10)
