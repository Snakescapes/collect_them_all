import requests
import os
import tkinter.ttk as ttk
from tkinter import *
from PIL import Image, ImageTk
from bs4 import BeautifulSoup


def write_to_textbox(message):
    text.insert('end', message + '\n')
    text.update()


def run_script():
    number_of_comics_to_download = int(entry.get())

    res = requests.get('http://explosm.net/comics/')
    res.raise_for_status()
    comics_downloaded = 0

    while comics_downloaded < number_of_comics_to_download:
        soup = BeautifulSoup(res.text, 'html.parser')
        current_comic_number = int(soup.button['data-slug'].split('-')[1])
        comic_tag = soup.select('#main-comic')[0]
        comic_url = 'http:' + comic_tag.get('src')
        current_comic_file = requests.get(comic_url)
        comic_basename = os.path.basename(comic_url).split('.')[0]

        message = f'Downloading comic_{current_comic_number}_{comic_basename}'
        write_to_textbox(message)
        print(f'Downloading comic_{current_comic_number}_{comic_basename}')

        if not os.path.exists('collect_them_all/cyanide_and_happiness'):
            os.makedirs('collect_them_all/cyanide_and_happiness')

        with open(os.path.join(f'{current_dir}/collect_them_all/cyanide_and_happiness',
                               f"comic_{current_comic_number}_{comic_basename}.png"), 'wb') as file:
            for chunk in current_comic_file.iter_content(100000):
                file.write(chunk)

        message = 'Download complete!'
        write_to_textbox(message)
        print('Download complete!')
        comics_downloaded += 1

        prev = soup.find(attrs={'title': 'Oldest comic'})

        if 'disabled' not in prev['class']:
            previous_comic_url = soup.select('.nav-previous')[0]['href']
            previous_comic_num = previous_comic_url.split('/')[2]
        else:
            break

        res = requests.get(f'http://explosm.net/comics/{previous_comic_num}')
        res.raise_for_status()

    message = f'Job complete! {comics_downloaded} comics downloaded successfully!'
    write_to_textbox(message)
    print(f'Job complete! {comics_downloaded} comics downloaded successfully!')
    message = 'Close this window to open the download directory!'
    write_to_textbox(message)
    print('Close this window to open the download directory!')


def configure_layout(app):
    app.configure(background="light gray")
    app.geometry("800x600")
    app.grid_rowconfigure(4, weight=1)
    app.grid_columnconfigure(0, weight=1)


def configure_static_elements(app):
    label = Label(app, text='How many comics would you like to download?', bg='light gray', pady=20)
    label.grid(row=1, column=0)
    global entry
    entry = Entry(app, bg='sky blue')
    entry.grid(row=2, column=0, pady=20, sticky=N+S)
    button_submit = Button(app, text='Download!', command=run_script, pady=10)
    button_submit.grid(row=3, column=0)
    global text
    yScroll = Scrollbar(orient=VERTICAL)
    yScroll.grid(row=4, column=0, sticky='NSE')
    text = Listbox(app, height=5, width=100, yscrollcommand=yScroll.set)
    text.grid(row=4, column=0, columnspan=2, sticky='n')
    yScroll['command'] = text.yview


    # scrollb = ttk.Scrollbar(command=text.yview)
    # scrollb.grid(row=4, column=0, sticky='E')
    # text['yscrollcommand'] = scrollb.set


def configure_image():
    load = Image.open('collect_them_all/resume.png')
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W+E+N+S)


current_dir = os.getcwd()
app = Tk()

configure_layout(app)
configure_static_elements(app)
configure_image()

app.mainloop()


# res = requests.get('http://explosm.net/comics/')
# res.raise_for_status()
# number_of_comics_to_download = int(input('How many comics would you like to download? '))
# comics_downloaded = 0
# while comics_downloaded < number_of_comics_to_download:
#     soup = BeautifulSoup(res.text, 'html.parser')
#     current_comic_number = int(soup.button['data-slug'].split('-')[1])
#     comic_tag = soup.select('#main-comic')[0]
#     comic_url = 'http:' + comic_tag.get('src')
#     current_comic_file = requests.get(comic_url)
#     comic_basename = os.path.basename(comic_url).split('.')[0]
#
#     print(f'Downloading comic_{current_comic_number}_{comic_basename}')
#
#     if not os.path.exists('collect_them_all/cyanide_and_happiness'):
#         os.makedirs('collect_them_all/cyanide_and_happiness')
#
#     with open(os.path.join(f'{current_dir}/collect_them_all/cyanide_and_happiness', f"comic_{current_comic_number}_{comic_basename}.png"), 'wb') as file:
#         for chunk in current_comic_file.iter_content(100000):
#             file.write(chunk)
#     print('Download complete!')
#     comics_downloaded += 1
#
#     prev = soup.find(attrs={'title': 'Oldest comic'})
#
#     if 'disabled' not in prev['class']:
#         previous_comic_url = soup.select('.nav-previous')[0]['href']
#         previous_comic_num = previous_comic_url.split('/')[2]
#     else:
#         break
#
#     res = requests.get(f'http://explosm.net/comics/{previous_comic_num}')
#     res.raise_for_status()
#
# print(f'Job complete! {comics_downloaded} comics downloaded successfully!')

os.startfile(f'{current_dir}/collect_them_all/cyanide_and_happiness')
