from pytube import YouTube, exceptions as pytube_exceptions
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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

playlists = ['https://www.youtube.com/playlist?list=PLHz_AreHm4dlIhETgFItQLMZ5PWXTjWb2', 'https://www.youtube.com/playlist?list=PLHz_AreHm4dnHG4o39bNKVuUAz7cSAb7q']


def get_palylists(playlists):
    data_playlists = list()
    
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options_chrome)

    for num, link in enumerate(playlists):
        driver.get(link)
        sleep(0.5)
        
        try:
            driver.find_element('xpath', '//*[@id="text"]')
            
        except NoSuchElementException:
            print(f'Playlist {num + 1}: Inválida!')
            continue
        
        else:
            name_playlist = driver.find_element('xpath', '//*[@id="text"]').get_attribute('textContent')

            count = 1
            list_videos = list()
            while True:
                try:
                    video = driver.find_element('xpath', f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-playlist-video-list-renderer/div[3]/ytd-playlist-video-renderer[{count}]/div[2]/div[1]/ytd-thumbnail/a').get_attribute('href')
                    
                except NoSuchElementException:
                    break
                    
                else:
                    list_videos.append('https://www.youtube.com' + video)
                    count += 1
            
            
            data_playlists.append([name_playlist, list_videos])
               
    
    return data_playlists


clear_os()
print('Seja Bem-Vindo ao PyTube')
print('By: Arthur Speziali')
sleep(1)
print('\nEste programa baixa vídeos de uma playlist do youtube usando a biblioteca "pytube", então tenha uma conexão com a internet.')
sleep(2)
clear_os()

if platform.system() == 'Windows':
    bar = '\\'
    
else:
    bar = '/'

print('Digite o link para a pasta "Pai" das playlist:\n')
while True:
    pathe = input('> ').strip()
    
    if pathe[-1] != bar:
        pathe = pathe + bar
    
    #Verificando se o caminho esta correto, tentando abrir ele: 
    try:
        with open(pathe + 'cache', 'w', encoding='utf-8') as v_path:
            clear_os()
            break
            
    except:
        print('\nCaminho mal-sucedido! Tente novamente!\n')


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
        video.download(output_path=pathe)
        
    except AttributeError:
        video = YouTube(link).streams.get_by_resolution(resolutions[resolutions.index(resol) + resol_round])
        
    else:
        clear_os()
        print('Video baixado com êxito!')    
        break