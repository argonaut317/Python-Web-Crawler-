from selenium import webdriver
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
from time import sleep
import shutil
import requests
import os


class App:
    def __init__(self, username='test_account_shreya12', password='@testrun',target_user='test_account_shreya12',path='E:/pics'):

        self.username = username
        self.password = password
        self.target_user = target_user
        self.error = False
        self.path = path
        self.driver = webdriver.Chrome('D:/chromedriver')
        self.main_url = 'https://www.instagram.com/'
        self.driver.get(self.main_url)
        sleep(5)
        self.log_in()
        if self.error is False:
            self.close_dialogue_box()
            self.open_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
        self.downloading_images()

        input('stop for now')
        sleep(3)
        self.driver.close()

    def write_captions_to_excel_file(self,images,caption_path):
        print('writing to excel')
        workbook = Workbook(os.path.join(caption_path, 'captions.xlsx'))
        #workbook = Workbook(caption_path,'/captions.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row,0,'Image Name')
        worksheet.write(row,1,'Captions')
        row+=1
        for index,image in enumerate(images):
            filename = 'image_'+str(index)+'.jpg'
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption exists'
            worksheet.write(row,0,filename)
            worksheet.write(row,1,caption)
            row+=1
        workbook.close()


    def download_captions(self,images):
        captions_folder_path = os.path.join(self.path,'captions')
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        self.write_captions_to_excel_file(images,captions_folder_path)
        '''for index,image in enumerate(images):
            try:
                caption = image['alt']
            except KeyError:
                caption = 'No caption available for this image'
                print('No caption exists')
            print(image['alt'])
            file_name ='caption_'+str(index) + '.txt'
            file_path = os.path.join(captions_folder_path,file_name)
            link = image['src']
            with open(file_path,'wb') as file:
                file.write(str('link:'+str(link)+'\n'+'caption:'+caption).encode())'''








    def downloading_images(self):
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        all_images = soup.find_all('img')
        self.download_captions(all_images)
        print('length of all images : ',len(all_images))
        for index,image in enumerate(all_images):
            file_name = 'image_'+str(index)+'.jpg'
            #image_path = self.path + '/' + file_name
            print(image['src'])
            image_path = os.path.join(self.path,file_name)
            link=image['src']
            response = requests.get(link,stream=True)
            try:
                with open(image_path,'wb') as file:
                    shutil.copyfileobj(response.raw,file)

            except Exception as e:
                print(e)
                print('Could not download image number',index)
                print('Image link-->',link)

    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath('//input[@class="XTCLo x3qfX "]')
            search_bar.send_keys(self.target_user)
            target_profile_user = self.main_url+self.target_user+'/'
            self.driver.get(target_profile_user)
            sleep(3)
        except Exception as e:
            print('unable to find search tab')
            self.error =True

    def scroll_down(self):
        try:
            no_of_posts = self.driver.find_element_by_xpath('//span[@class="g47SY "]')
            no_of_posts =str(no_of_posts.text).replace(',','')
            self.no_of_posts = int(no_of_posts)
            if self.no_of_posts>12:
                no_of_scrolls = int(self.no_of_posts/12)+3
                try:
                    for value in range(no_of_scrolls):
                        print(value)
                        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                        sleep(1)
                except Exception as e:
                    print(e)
                    print('Some error occurred while scrolling down')
                    self.error = True
        except Exception as e:
            print('could not find number of posts while scrolling down')
            self.error = True



    def close_dialogue_box(self):
        try:
            sleep(3)
            close_btn = self.driver.find_element_by_xpath('//button[@class="aOOlW   HoLwm "]')
            close_btn.click()
            sleep(1)

        except Exception as e:
            pass

    def close_settings_window_if_there(self):
        try:
            self.driver.switch_to_window(self.driver.windows_handles[1])
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
        except Exception as e:
            pass



    def log_in(self,):
        try:
            log_in_button=self.driver.find_element_by_xpath('//*[contains(@href,"accounts/login/?")]')
            log_in_button.click()
            sleep(2)
            try:
                user_name_input = self.driver.find_element_by_xpath('//input[@name="username"]')
                user_name_input.send_keys(self.username)
                sleep(1)
                password_element = self.driver.find_element_by_xpath('//input[@name="password"]')
                password_element.send_keys(self.password)
                sleep(2)
                self.driver.find_element_by_xpath('//*[@type="submit"]').click()
                sleep(6)
            except Exception as e:
                self.error = True
                print('cannot find username input or password input')
        except Exception as e:
            self.error = True
            print('unable to find login button')







if __name__ == '__main__':

    app = App()
