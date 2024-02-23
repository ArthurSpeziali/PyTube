from pytube import YouTube, exceptions as pytube_exceptions
from playwright.sync_api import sync_playwright
from time import sleep
import os, platform

#Função que limpa o terminal de acordo com o OS:
def clear_os():
    
    #Se for Windows, ele limpa o terminal com "cls":
    if platform.system() == 'Windows': 
        os.system('cls')
    
    #Se for Linux ou Mac, limpa o terminal com "clear":
    else:
        os.system('clear')


clear_os()
print('Seja Bem-Vindo ao PyTube')
print('By: Arthur Speziali')
sleep(1)
print('\nEste programa baixa vídeos de uma playlist do youtube usando a biblioteca "pytube", então tenha uma conexão com a internet.')
sleep(2)
clear_os()

print('Digite o link da playlist do youtube:\n')
while True:
    link = input('> ').strip()
    
    try:
        YouTube(link).streams.get_lowest_resolution()
        
    except  pytube_exceptions.VideoUnavailable:
        print('\nVídeo indisponível, tente outro!\n')
        
    except pytube_exceptions.RegexMatchError:
        print('\nLink inválido, tente outro!\n')

    else:
        break
    
clear_os()
print('Digite a resolução (720p), e no fim, coloque um + para indicar que se não conter a resolução, vai pegar a próxima mais alta:\n')
while True:
    resol = input('> ')
    
    resol_round = -1
    if '+' in resol and not '144p' in resol:
        resol_round = 1
        resol = resol.replace('+', '')
        
    resolutions = ('144p', '240p', '360p', '480p', '720p', '1080p')
    if resol in resolutions:
        break
    
    else:
        print('\nResolução inválida, minímo de 140 e máximo de 1080.\n')
    
clear_os()
print('Baixando vídeo...')
video = YouTube(link).streams.get_by_resolution(resol)

while True:
    try:
        video.download()
        
    except AttributeError:
        video = YouTube(link).streams.get_by_resolution(resolutions[resolutions.index(resol) + resol_round])
        
    else:
        clear_os()
        print('Video baixado com êxito!')    
        break