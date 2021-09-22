# 네이버 크롤러 Version 1.0

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import shutil


class Searcher:
    def naver(self):
        print("="*80)
        print(f'{"네이버크롤러 version 1.0": ^65}')
        print("="*80)
        # 검색어 입력받기
        while True:
            self.search = input("검색어를 입력해주세요. > ")
            print('='*80)
            if self.search == '':
                print("크롤링할 검색어를 입력해주세요.")
                print('='*80)
                continue
            else:
                break

        # 크롬으로 네이버 연결
        path = "C:\python_temp\chromedriver_win32\chromedriver.exe"
        self.driver = webdriver.Chrome(path)
        self.driver.get("https://www.naver.com")

        # 전체화면으로 변환
        self.driver.maximize_window()
        time.sleep(1)

        # 검색어 입력 후 검색버튼 클릭
        element = self.driver.find_element_by_class_name("input_text")
        element.send_keys(self.search)
        self.driver.find_element_by_class_name("btn_submit").click()
        time.sleep(1)


class Crawler(Searcher):
    # 동일 저장리스트
    no2 = []
    title2 = []
    content2 = []
    # 카페와 블로그만 동일
    writer2 = []
    dates2 = []
    # 다른 저장리스트들
    sources = []
    dic2 = []
    s_title2 = []
    ###### 블로그 #######

    def blog(self):
        pass
    ###### 뉴스 #######

    def news(self):
        pass
    ###### 카페 #######

    def cafe(self):
        global no2
        global writer2
        global title2
        global content2
        global dates2

        # 리스트 비우기
        self.no2.clear()
        self.writer2.clear()
        self.title2.clear()
        self.content2.clear()
        self.dates2.clear()
        time.sleep(2)

        # 페이지 링크 가져오기
        full_html = self.driver.page_source
        # 페이지 해석
        soup = BeautifulSoup(full_html, 'html.parser')
        # VIEW카테고리에 카페글로 가기
        self.driver.find_element_by_link_text("VIEW").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("카페").click()
        time.sleep(1)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            div = soup.find("div", class_="api_subject_bx")
            data_list = div.select('ul > li')
        except AttributeError:
            print("정보가 없습니다.")
            print("="*80)
        else:
            # 크롤링할 개수 입력받기
            self.save_num = int(input("크롤링할 글 개수를 입력해주세요: "))
            print('\n')

            # 개수만큼 스크롤 내리기
            body = self.driver.find_element_by_css_selector('body')
            while len(data_list) < self.save_num:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                div = soup.find("div", class_="api_subject_bx")
                data_list = div.select('ul > li')

            # 시작시간
            s_time = time.time()
            # 반복문으로 입력받은 개수만큼 정보 추출하기
            no = 1
            for i in data_list:
                if no <= self.save_num:
                    try:
                        title = i.find(
                            'a', class_="api_txt_lines total_tit").get_text().strip()
                        content = i.find(
                            'div', class_="api_txt_lines dsc_txt").get_text().strip()
                        dates = i.find(
                            'span', class_="sub_time sub_txt").get_text().strip()
                        writer = i.find(
                            'a', class_="sub_txt sub_name").get_text().strip()
                    except AttributeError:
                        title = '제목이 없습니다.'
                        self.title2.append(title)
                        print("2) 게시글 제목:", title)
                        content = '내용이 없습니다.'
                        self.content2.append(content)
                        print("3) 게시글 요약내용:", content)
                        print('\n')
                    else:
                        self.no2.append(no)
                        print("1) 글 번호:", no)
                        self.title2.append(title)
                        print("2) 게시글 제목:", title)
                        self.content2.append(content)
                        print("3) 게시글 요약내용:", content)
                        self.dates2.append(dates)
                        print("4) 게시글 작성날짜:", dates)
                        self.writer2.append(writer)
                        print("5) 카페명:", writer)
                        print('\n')
                        no += 1
                else:
                    break
            time.sleep(2)
            print(f"""크롤링이 완료되었습니다.\n크롤링된 글의 개수는 {len(self.no2)}입니다.\n""")

            # 작업시간 표시
            e_time = time.time()
            t_time = e_time-s_time
            print('='*80)
            print('출력에 걸린시간은 %s초 입니다' % round(t_time, 1))
            print('='*80)

            # 통합페이지로 돌아가기
            self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(2)
            self.driver.find_element_by_xpath(
                '//*[@id="lnb"]/div[1]/div/ul/li[1]/a').click()

    ###### 카페 텍스트 저장 #######
    def cafe_text(self):
        global no2
        global writer2
        global title2
        global content2
        global dates2

        # 페이지 링크 가져오기
        full_html = self.driver.page_source
        # 페이지 해석
        soup = BeautifulSoup(full_html, 'html.parser')
        # VIEW카테고리에 카페글로 가기
        self.driver.find_element_by_link_text("VIEW").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("카페").click()
        time.sleep(1)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            div = soup.find("div", class_="api_subject_bx")
            data_list = div.select('ul > li')
        except AttributeError:
            print("정보가 없습니다.")
        else:
            # 개수만큼 스크롤 내리기
            body = self.driver.find_element_by_css_selector('body')
            while len(data_list) < self.save_num:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                div = soup.find("div", class_="api_subject_bx")
                data_list = div.select('ul > li')

            # 반복문으로 개수만큼 정보 추출하기
            no = 1
            for i in data_list:
                if no <= self.save_num:
                    try:
                        title = i.find(
                            'a', class_="api_txt_lines total_tit").get_text().strip()
                        content = i.find(
                            'div', class_="api_txt_lines dsc_txt").get_text().strip()
                        dates = i.find(
                            'span', class_="sub_time sub_txt").get_text().strip()
                        writer = i.find(
                            'a', class_="sub_txt sub_name").get_text().strip()
                    except AttributeError:
                        title = '제목이 없습니다.'
                        print("2) 게시글 제목:", title)
                        content = '내용이 없습니다.'
                        print("3) 게시글 요약내용:", content)
                        print('\n')
                    else:
                        print("1) 글 번호:", no)
                        print("2) 게시글 제목:", title)
                        print("3) 게시글 요약내용:", content)
                        print("4) 게시글 작성날짜:", dates)
                        print("5) 카페명:", writer)
                        print('\n')
                        no += 1
                else:
                    break
            time.sleep(2)

            # 통합페이지로 돌아가기
            self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(2)
            self.driver.find_element_by_xpath(
                '//*[@id="lnb"]/div[1]/div/ul/li[1]/a').click()

    ###### 백과사전 #######
    def know(self):
        pass
    ###### 어학사전 #######

    def lan_dic(self):
        pass


class SaveMenu(Crawler):
    # c:\ezen_ai\2021-09-15-16-21-가을 여행-view.txt로 저장되었습니다.
    def save_folder(self):
        while True:
            if self.save_re == 0:
                try:
                    self.f_dir = input(
                        "수집된 데이터를 저장할 폴더명을 입력해주세요.\n(예: c:\ezen_python_data\\) > ")
                except OSError:
                    print("파일명을 제대로 써주세요.")
                    print("="*80)
                    continue
                else:
                    print("="*80)
                    try:
                        os.makedirs(self.f_dir)
                    except OSError:
                        while True:
                            save_again = input("해당 폴더명이 이미 존재합니다. 폴더명을 다시 입력하시겠습니까?\
                            \n[메뉴] Y : 폴더명 다시 입력 / M : 존재하는 폴더에 저장 / D: 존재하는 폴더 삭제 > ")
                            print("="*80)
                            if save_again.upper() == "Y":
                                break
                            elif save_again.upper() == "M":
                                while True:
                                    save_again2 = input(
                                        "이미 존재하는 폴더명에 저장하시겠습니까?(Y/N) > ")
                                    if save_again2.upper() == "Y":
                                        self.save_re += 1
                                        return os.chdir(self.f_dir)
                                        break
                                    elif save_again2.upper() == "N":
                                        print("존재하는 폴더에 저장하기를 선택하지 않으셨습니다.")
                                        print("="*80)
                                        break
                                    else:
                                        print("(Y/N)로 입력해주시길 바랍니다.")
                                        continue
                            elif save_again.upper() == "D":
                                try:
                                    os.rmdir(self.f_dir)
                                except OSError:
                                    while True:
                                        have = input(
                                            "해당 폴더에 있는 파일까지 모두 삭제하시겠습니까?(Y/N) > ")
                                        if have.upper() == "Y":
                                            try:
                                                shutil.rmtree(self.f_dir)
                                            except OSError:
                                                mag = '[WinError 32] 다른 프로세스가 파일을 사용 중이기 때문에 프로세스가 액세스 할 수 없습니다'
                                                break
                                            else:
                                                time.sleep(1)
                                                print(
                                                    f"{self.f_dir}폴더를 삭제하였습니다.")
                                                print("="*80)
                                                break
                                        elif have.upper() == "N":
                                            break
                                        else:
                                            print("(Y/N)로 입력해주시길 바랍니다.")
                                            continue
                                break
                            else:
                                print("(Y /M /D)만 입력해주시길 바랍니다.")
                                continue
                    else:
                        os.chdir(self.f_dir)
                        self.save_re += 1
                        break
            else:
                while True:
                    dir_again = input("이전에 요청하신 저장폴더에 계속 저장하시겠습니까?(Y/N) > ")
                    if dir_again.upper() == "Y":
                        self.save_re += 1
                        return os.chdir(self.f_dir)
                        break
                    elif dir_again.upper() == "N":
                        self.save_re = 0
                        break
                    else:
                        print("(Y/N)로 입력해주시길 바랍니다.")
                        continue

    def save_txt(self, searchType):
        try:
            if self.cnt >= 1:
                Crawler.know_text()
            else:
                Crawler.know()
        except:
            pass

        now = time.localtime()
        f_name = "%04d-%02d-%02d-%02d-%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
        searchMenu = {"1": "블로그", "2": "뉴스",
                      "3": "카페", "4": "지식백과", "5": "어학사전"}
        for key, value in searchMenu.items():
            if int(key) == searchType:
                ff_name = self.f_dir+f_name+"-"+self.search+"-"+value+".txt"
            else:
                pass
        orig_stdout = sys.stdout
        f = open(ff_name, 'a', encoding='utf-8')
        sys.stdout = f

        if searchType == 1:
            self.blog()
        elif searchType == 2:
            self.news()
        elif searchType == 3:
            self.cafe_text()
        elif searchType == 4:
            self.know_text()
        elif searchType == 5:
            self.lan_dic()
        else:
            print("숫자를 제대로 입력해주세요.")

        sys.stdout = orig_stdout
        f.close()
        print('txt 파일 저장 경로 : %s' % ff_name)
        print("="*80)
        pass

    def save_csv(self, searchType):
        now = time.localtime()
        f_name = "%04d-%02d-%02d-%02d-%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
        searchMenu = {"1": "블로그", "2": "뉴스",
                      "3": "카페", "4": "지식백과", "5": "어학사전"}
        for key, value in searchMenu.items():
            if int(key) == searchType:
                fc_name = self.f_dir+f_name+"-"+self.search+"-"+value+".csv"
            else:
                pass

        #### 블로그 ####
        if searchType == 1:
            pass
        #### 뉴스 ####
        elif searchType == 2:
            pass
        #### 카페 ####
        elif searchType == 3:
            data = pd.DataFrame()
            data['번호'] = self.no2
            data['제목'] = self.title2
            data['내용'] = self.content2
            data['작성일'] = self.dates2
            data['카페명'] = self.writer2
            data.to_excel(fx_name)
            print('xls 파일 저장 경로 : %s' % fx_name)
            print("="*80)
        #### 지식백과 ####
        elif searchType == 4:
            pass
        #### 어학사전 ####
        elif searchType == 5:
            pass

    def save_xls(self, searchType):
        now = time.localtime()
        f_name = "%04d-%02d-%02d-%02d-%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
        searchMenu = {"1": "블로그", "2": "뉴스",
                      "3": "카페", "4": "지식백과", "5": "어학사전"}
        for key, value in searchMenu.items():
            if int(key) == searchType:
                fx_name = self.f_dir+f_name+"-"+self.search+"-"+value+".xls"
            else:
                pass

        #### 블로그 ####
        if searchType == 1:
            pass
        #### 뉴스 ####
        elif searchType == 2:
            pass
        #### 카페 ####
        elif searchType == 3:
            data = pd.DataFrame()
            data['번호'] = self.no2
            data['제목'] = self.title2
            data['내용'] = self.content2
            data['작성일'] = self.dates2
            data['카페명'] = self.writer2
            data.to_excel(fx_name)
            print('xls 파일 저장 경로 : %s' % fx_name)
            print("="*80)
        #### 지식백과 ####
        elif searchType == 4:
            pass
        #### 어학사전 ####
        elif searchType == 5:
            pass


class Run(SaveMenu):

    def save_run(self, searchType):
        if not len(self.no2):
            while self.done > 0:
                try:
                    question = input(
                        "저장할 정보가 없습니다. 다른 메뉴로 크롤링 하시겠습니까?(Y/N) > ")
                except ValueError:
                    print("(Y/N)를 입력해주세요.")
                    print("="*80)
                    continue
                else:
                    if question.upper() == "Y":
                        break
                    elif question.upper() == "N":
                        while True:
                            try:
                                self.new = int(
                                    input("새로운 검색어로 검색하시겠습니까?(1:예/ 2:아니오) > "))
                            except ValueError:
                                print("숫자를 입력해주세요.")
                                print("="*80)
                                continue
                            else:
                                if self.new == 1:
                                    self.new = 1
                                    self.done = 0
                                    break
                                elif self.new == 2:
                                    self.new = 2
                                    self.done = 0
                                    break
                                else:
                                    print("숫자만 입력해주시길 바랍니다.")
                                    continue
                    else:
                        print("(Y/N)만 입력해주세요.")
                        print("="*80)
                        continue
        else:
            self.save_done = 1
            while self.save_done > 0:
                try:
                    save_q = input("추출된 데이터를 파일로 저장하시겠습니까?(Y/N) > ")
                except ValueError:
                    print("(Y/N)를 입력해주세요.")
                    print("="*80)
                    continue
                else:
                    if save_q.upper() == "Y":
                        saveType = 1
                        self.save_re = 0
                        while True:
                            try:
                                saveType = int(
                                    input("""[메뉴] 1.txt 2.csv 3.xls (종료: 0)\n메뉴를 선택해주세요 > """))
                            except ValueError:
                                print("메뉴를 입력해주세요.")
                                print("="*80)
                                continue
                            else:
                                print("="*80)
                                if saveType == 1:
                                    self.save_folder()
                                    self.save_txt(searchType)
                                    self.save_re += 1
                                elif saveType == 2:
                                    self.save_folder()
                                    self.save_csv(searchType)
                                    self.save_re += 1
                                elif saveType == 3:
                                    self.save_folder()
                                    self.save_xls(searchType)
                                    self.save_re += 1
                                elif saveType == 0:
                                    self.save_done = 0
                                    self.save_re += 0
                                    print("저장 프로그램을 종료합니다.")
                                    print("="*80)
                                    break
                                else:
                                    print("숫자를 제대로 입력해주세요.")
                                    print("="*80)
                                    continue
                    elif save_q.upper() == "N":
                        print("저장 프로그램을 종료합니다.")
                        print("="*80)
                        break
                    else:
                        print("(Y/N)만 입력해주세요.")
                        continue

    def run(self):
        self.new = 1
        self.done = 1
        self.save_done = 1
        while True:
            # 네이버크롤러 시작
            if self.new == 1:
                self.naver()
                self.done = 1
            else:
                print("네이버크롤러 version 1.0를 종료합니다.")
                print("웹 브라우저를 종료하겠습니다.")
                print("="*80)
                self.driver.close()
                break
            while self.done > 0:
                # 메뉴 선택하여 크롤링 하기
                try:
                    searchType = int(
                        input("""[메뉴] 1.블로그 2.뉴스 3.카페 4.지식백과 5.어학사전 (종료: 0)\n메뉴를 선택해주세요 > """))
                except ValueError:
                    print("메뉴를 선택해주세요.")
                    print("="*80)
                    continue
                else:
                    print("="*80)
                    #### 블로그 크롤링 ####
                    if searchType == 1:
                        self.blog()
                        self.save_run(searchType)

                    #### 뉴스 크롤링 ####
                    elif searchType == 2:
                        self.news()
                        self.save_run(searchType)

                    #### 카페 크롤링 ####
                    elif searchType == 3:
                        self.cafe()
                        self.save_run(searchType)

                    #### 백과사전 크롤링 ####
                    elif searchType == 4:
                        self.know()
                        self.save_run(searchType)

                    #### 어학사전 크롤링 ####
                    elif searchType == 5:
                        self.lan_dic()
                        self.save_run(searchType)

                    #### 크롤링 종료 ####
                    elif searchType == 0:
                        while True:
                            try:
                                self.new = int(
                                    input("새로운 검색어로 검색하시겠습니까?(1:예/ 2:아니오) > "))
                            except ValueError:
                                print("숫자를 입력해주세요.")
                                print("="*80)
                                continue
                            else:
                                if self.new == 1:
                                    self.new = 1
                                    self.done = 0
                                    break
                                elif self.new == 2:
                                    self.new = 2
                                    self.done = 0
                                    print("="*80)
                                    break
                                else:
                                    print("숫자만 입력해주시길 바랍니다.")
                                    continue
                    else:
                        print("숫자를 제대로 입력해주세요.")
                        print("="*80)
                        continue
