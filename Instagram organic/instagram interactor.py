from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import random
import xlrd
import os
import openpyxl
from datetime import datetime
from numba import jit
import tkinter as tk

HEIGHT=500
WIDTH=700



def check_like(post_link):
    likes_df = pd.read_csv(r'files/likes history.csv',sep=',')
    print(type(likes_df))
    likes_list = list(likes_df['link'])
    if post_link not in likes_list:
        return True
    else:
        return False


def dynamic_check_like(web_driver):
    btn_color = web_driver.find_element_by_class_name('ltpMr.Slqrh').find_elements_by_tag_name('button')[0].find_element_by_tag_name('svg').get_attribute('color')
    print(btn_color)
    if (btn_color == '#262626') or (btn_color == '#8e8e8e'):
        return True
    else:
        return False


def save_like(post_link, account_link):
    likes_df = pd.read_csv(r'files/likes history.csv',sep=',')
    now_dt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    new_like_df = {'link':post_link,'account':account_link,'date':now_dt}
    likes_df = likes_df.append(new_like_df, ignore_index = True)
    likes_df.to_csv(r'files/likes history.csv', index=False)

def check_follow():
    pass

def save_follow():
    pass

def start_webdriver():
    web_driver = webdriver.Chrome()
    return web_driver

def connect_to_instagram(web_driver,username,password):
    try:
        web_driver.get("https://www.instagram.com/")
        sleep(7)
        web_driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
        sleep(3)
        web_driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
        sleep(5)
        web_driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
        sleep(7)
        boolean=False
    except:
        web_driver.close()


def follow_instagram_account(web_driver,profile_link):
    #web_driver.get(profile_link)
    time_wait = random.randint(2,5)
    sleep(time_wait)
    try:
        follow_btn=web_driver.find_element_by_class_name('_5f5mN.jIbKX._6VtSN.yZn4P')
        print(follow_btn.text)
        if (follow_btn.text == 'S’abonner') or (follow_btn.text == 'Follow'):
            follow_btn.click()
            sleep(2)
        else:
            print(profile_link+' '+follow_btn.text)
    except :
        try:
            follow_btn=web_driver.find_element_by_class_name('sqdOP.L3NKy._4pI4F.y3zKF')
            print(follow_btn.text)
            if ('abonner' in follow_btn.text) or (follow_btn.text == 'Follow'):
                follow_btn.click()
                sleep(2)
            else:
                print(profile_link+' '+follow_btn.text)
        except:
            print("Follow button not found")
            pass




def get_instagram_posts(web_driver,profile_link):
    insta_posts=[]
    try:
        web_driver.get(profile_link)
        sleep(5)
        insta_links= web_driver.find_elements_by_tag_name('a')
        for link in insta_links:
            post=link.get_attribute('href')
            if '/p/' in post:
                insta_posts.append(post)
        #print(insta_posts)
    except :
        #print("Pubs are closed or doesn't exist")
        pass
    follow_probability_number = random.randint(0, 100)
    #print(follow_probability_number)
    if (follow_probability_number<20) :
        follow_instagram_account(web_driver,profile_link)
        print(profile_link + ' FOLLOWED')
    return insta_posts

def like_instagram_post(web_driver,post_link):
    try:
        web_driver.get(post_link)
        sleep(random.randint(4, 8))
        if  (dynamic_check_like(web_driver) == True) :
            try:
                heart_btn= web_driver.find_element_by_class_name('ltpMr.Slqrh').find_elements_by_tag_name('button')[0]
                heart_btn.click()
                time_wait = random.randint(4, 8)
                #print('found by xpath 1')
                sleep(time_wait)
            except :
                print('not xpath 1 like')

                try:
                    heart_btn= web_driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
                    heart_btn.click()
                    time_wait = random.randint(4, 8)
                    #print(post_link+'found by xpath 2')
                    sleep(time_wait)
                except :
                    print('not xpath 1 or 2 like '+post_link)
                    pass
    except :
        #print("publication not found")
        pass

def get_people_from_post(web_driver,post_link):
    web_driver.get(post_link)
    sleep(5)
    try:
        try:
            likers_btn=web_driver.find_element_by_class_name("zV_Nj")
            likers_btn.click()
            #print("Likers Button Found by xpath")
            try:
                # emulate click on a likes button
                sleep(4)
                web_driver.execute_script('''document.getElementsByClassName('Nm9Fw')[0].lastElementChild.click()''')
                scroll_number= random.randint(2, 10)
                for i in range (scroll_number):
                    # scroll down by 4000px to load more users who liked the post
                    web_driver.execute_script('''document.getElementsByClassName('Igw0E IwRSH eGOV_ vwCYk i0EQd')[0].firstChild.scrollBy(0, 4000);''')
                    sleep(2)
                print('scrolled...')
            except :
                #print("3 doesnt work")
                pass
        except :
            pass
        likers_list=[]
        sleep(3)
        insta_links= web_driver.find_elements_by_tag_name('a')
        #print(insta_links)
        for link in insta_links:
            class_name = link.get_attribute('class')
            #print(class_name)
            if class_name=='FPmhX notranslate MBL3Z':
                liker=link.get_attribute('href')
                likers_list.append(liker)
        if len(likers_list)>100:
            likers_list=likers_list[:100]
        return likers_list
    except :
        print("likers list is closed or doesn't exist")
        pass





def interact_from_competition(web_driver, competition_list, maximum_likes):
    ###Interaction logic------------------
    print('start interaction')
    likesCount = 0

    for competitor in competition_list:
        sleep(1)
        competitor_link = 'https://www.instagram.com/'+competitor+'/'
        print(competitor_link)
        competitor_posts = get_instagram_posts(web_driver, competitor_link)
        print(competitor_posts)
        for post in competitor_posts:
            sleep(3)
            prospects = get_people_from_post(web_driver, post)
            for prospect in prospects[-20:]:
                prospect_posts = get_instagram_posts(web_driver,prospect)
                for post in prospect_posts:
                    like_probability_number = random.randint(0, 100)
                    if likesCount<int(maximum_likes):
                        if like_probability_number<60 :
                            print('will like')
                            ##  ---   use save_like for future analytical purpose   ---    ##
                            #save_like(post, prospect)
                            like_instagram_post(web_driver,post)
                            likesCount+=1
                            print(likesCount)
                            sleep(2)
                            web_driver.get(prospect)
                            sleep(2)
                    else:
                        print('maximum likes reached')
                        web_driver.close()




def interact_from_hashtags ():
    pass


def run_bot(username,password,competitors_string,maximum_likes):
    web_driver = start_webdriver()
    connect_to_instagram(web_driver,username,password)
    competition_list=competitors_string.split(',')
    print(competition_list)
    interact_from_competition(web_driver,competition_list,maximum_likes)
    web_driver.close()



root = tk.Tk()
root.title("Instagram Sponsoring Amplifier Bot")
root.iconbitmap("files/logo.ico")

canvas=tk.Canvas(root, height=HEIGHT , width=WIDTH )
canvas.pack()


#background_label=tk.Label(root,bg=background_image)
#background_label.place(relwidth=1, relheight=1)

welcome = tk.Label(root, text="Welcome to Instagram sponsoring amplifier bot", bg='yellow')
welcome.pack()

frame=tk.Frame(root, bg='#99ceff',bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.8, anchor='n')

button = tk.Button(frame, text="Run Bot", bg="gray", font=40, command=lambda:run_bot(username.get(),password.get(),competitors.get(),maximum_likes.get()))
button.place(relx=0.1, rely=0.9,relwidth=0.9, relheight=0.1)

username_label = tk.Label(frame, text="username:", bg='#99ceff', font=('modern',15), anchor='nw', justify='left')
username_label.place(relx=0.1, rely=0.05,relwidth=0.5, relheight=0.1)

username=tk.Entry(frame, font=40 )
username.place(relx=0.1, rely=0.15,relwidth=0.5, relheight=0.1)

password_label = tk.Label(frame, text="password:", font=('modern',15),bg='#99ceff', anchor='nw', justify='left')
password_label.place(relx=0.1, rely=0.25,relwidth=0.5, relheight=0.1)

password=tk.Entry(frame,show="*", font=40 )
password.place(relx=0.1, rely=0.35,relwidth=0.5, relheight=0.1)

competitors_label = tk.Label(frame, text="competitors:", bg='#99ceff', font=('modern',15), anchor='nw', justify='left')
competitors_label.place(relx=0.1, rely=0.45,relwidth=0.5, relheight=0.1)

competitors=tk.Entry(frame, font=40 )
competitors.place(relx=0.1, rely=0.55,relwidth=0.9, relheight=0.1)

maximum_likes_label = tk.Label(frame, text="maximum likes:", bg='#99ceff', font=('modern',15), anchor='nw', justify='left')
maximum_likes_label.place(relx=0.1, rely=0.65,relwidth=0.5, relheight=0.1)

maximum_likes=tk.Entry(frame, font=40 )
maximum_likes.place(relx=0.1, rely=0.75,relwidth=0.9, relheight=0.1)

#lower_frame= tk.Frame(root,bg='#99ceff',bd=5)
#lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

#label = tk.Label(lower_frame, font=('modern',20), anchor='nw', justify='left')
#label.place(relx=0, rely=0,relwidth=1, relheight=1)

root.mainloop()
