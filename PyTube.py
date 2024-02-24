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

#playlists = ['https://www.youtube.com/playlist?list=PLHz_AreHm4dlIhETgFItQLMZ5PWXTjWb2', 'https://www.youtube.com/playlist?list=PLHz_AreHm4dnHG4o39bNKVuUAz7cSAb7q']


def get_playlists(playlists):
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
            print(f'\nPlaylist {num + 1}: Inválida!')
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
                    list_videos.append(video)
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
    
print('Digite se prefere abrir um arquivo, ou digitar manualmente as playlists: [F/M]\n')
while True:
    opção = input('> ').strip().lower()
    
    if opção != 'f' and opção != 'm':
        print('\nOpção inválida, tente novamente!\n')
        
    else:
        clear_os()
        break
    
if opção == 'm':
    print('Digite cada playlist em cada linha (Só vamos considerar as playlists válidas), para encerrar o loop, digite "0":')
    
    playlists = list()
    while True:
        play = input('\n> ').strip()
        
        if play == '0' and len(play) > 0:
            break
        
        else:
            playlists.append(play)
            

elif opção == 'f':
    print('Digite o caminho até o arquivo com o link das playlists:\n')
    
    while True:
        pathe = input('> ').strip()
    
        #Verificando se o caminho esta correto, tentando abrir ele: 
        try:
            with open(pathe, encoding='utf-8') as v_path:
                playlists = v_path.read().split('\n')
                
                for i in playlists:
                    if i == '':
                        playlists.remove(i)
                        
                break
                
        except FileNotFoundError:
            print('\nCaminho mal-sucedido! Tente novamente!\n')

clear_os()
print('Encontrando os vídeos... Aguarde!')
output_playlists = get_playlists(playlists)
clear_os()

print('Digite o link para a pasta "Pai" das playlist:\n')
while True:
    folder = input('> ').strip()
    
    if folder[-1] != bar:
        folder = folder + bar
    
    try:
        with open(folder + 'logs.txt', 'w', encoding='utf-8') as v_path:
            clear_os()
            break
            
    except FileNotFoundError:
        print('\nCaminho mal-sucedido! Tente novamente!\n')
        
        
print('Digite a resolução (720p), e no fim, coloque um + para indicar que se não conter a resolução, vai pegar a próxima mais alta:\n')
resolutions = ('144p', '240p', '360p', '480p', '720p')
while True:
    resol = input('> ')
    
    resol_round = -1
    if '+' in resol and not '720p' in resol:
        resol_round = 1
        resol = resol.replace('+', '')
        
    elif '144p' in resol:
        resol_round = 1
            
    if resol in resolutions:
        break
    
    else:
        print('\nResolução inválida, minímo de 140 e máximo de 1080.\n')

clear_os()
print('Baixando os vídeos, Aguarde...')
download_count = video_count = 0
for play in output_playlists:
    son_folder = folder + play[0] + bar
    
    print(f'\nPlaylist "{play[0]}":\n')
    
    try:
        os.mkdir(son_folder)
        
    except FileExistsError:
        os.rename(son_folder, son_folder[:-1] + '.old')
        os.mkdir(son_folder)
        

    for num, video in enumerate(play[1]):
        video_count += 1
        
        try:
            YouTube(video).streams.get_lowest_resolution()
            
        except pytube_exceptions.MembersOnly:
            print(f'Vídeo número {num + 1}: Somente para membros')
            
            with open(folder + 'logs.txt', 'a') as logs:
                logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Somente para membros\n')
            
        except pytube_exceptions.VideoPrivate:
            print(f'Vídeo número {num + 1}: Vídeo privado')
            
            with open(folder + 'logs.txt', 'a') as logs:
                logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Vídeo privado\n')
            
        except pytube_exceptions.LiveStreamError:
            print(f'Vídeo número {num + 1}: Vídeo é uma live')
            
            with open(folder + 'logs.txt', 'a') as logs:
                logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Vídeo é uma live\n')
            
        except pytube_exceptions.AgeRestrictedError:
            print(f'Vídeo número {num + 1}: Restrição de ídade')
            
            with open(folder + 'logs.txt', 'a') as logs:
                logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Restrição de ídade\n')
            
        except pytube_exceptions.VideoUnavailable:
            print(f'Vídeo número {num + 1}: Indisponível')
            
            with open(folder + 'logs.txt', 'a') as logs:
                logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Vídeo Indisponível\n')
            
        except pytube_exceptions.RegexMatchError:
            print(f'Vídeo número {num + 1}: Link inválido')
            
            with open(folder + 'logs.txt', 'a') as logs:
                logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Link inválido')

        else:
            video_download = YouTube(video).streams.get_by_resolution(resol)

            for i in range(6):
                try:
                    video_download.download(output_path=son_folder)
                    
                except AttributeError:
                    print('Nao')
                    resol = resolutions[resolutions.index(resol) + resol_round]
                    video_download = YouTube(video).streams.get_by_resolution(resol)
                    
                else:
                    print(f'Vídeo número {num + 1}: Baixado com êxito')
                    
                    with open(folder + 'logs.txt', 'a') as logs:
                        logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Baixado com êxito\n')       
                    
                    download_count += 1
                    break
            
            else:
                print(f'\nVídeo número {num + 1}: Erro inesperado no download.')
                    
                with open(folder + 'logs.txt', 'a') as logs:
                    logs.write(f'Playlist "{play[0]}": Vídeo número {num + 1}: Erro inesperado no download.\n')       
        
clear_os()
print(f'De {video_count} vídeos, {download_count} foram baixados com êxito.')